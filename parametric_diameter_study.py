"""Transparent analytical monocoque trade study. SI internally; no FEA.

Results are conditional on the documented course design basis, not certification.
Run `python3 parametric_diameter_study.py` to regenerate JSON/CSV. Standard library only.
"""
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import csv
import json
import math

ROOT = Path(__file__).resolve().parent

@dataclass(frozen=True)
class Material:
    name: str
    E: float
    nu: float
    density: float
    yield_stress: float = 0.0
    Xc: float = 0.0
    Yt: float = 0.0
    S: float = 0.0

    @property
    def composite(self):
        return self.yield_stress == 0

MATERIALS = (
    Material('Aluminium 7075-T6', 71.7e9, .33, 2810, 503e6),
    Material('Titanium Ti-6Al-4V', 113.8e9, .31, 4430, 880e6),
    Material('Steel 4130', 205e9, .29, 7850, 460e6),
    Material('Magnesium AZ31B', 45e9, .35, 1770, 220e6),
    Material('Carbon/Epoxy QI', 55e9, .30, 1600, Xc=600e6, Yt=500e6, S=200e6),
    Material('Glass/Epoxy QI', 25e9, .30, 1900, Xc=300e6, Yt=250e6, S=100e6),
    Material('Aramid/Epoxy QI', 35e9, .34, 1400, Xc=200e6, Yt=300e6, S=80e6),
)

@dataclass(frozen=True)
class Basis:
    length: float = 1.5
    load_factor: float = 1.5
    thickness_retention: float = .95
    kdf_cap: float = .35
    moment_case: str = 'brief'
    initial_bow: float = .0015  # assumed L/1000, stress-free sinusoidal bow
    diameter_min_mm: int = 40  # declared search boundary, NOT a brief requirement
    diameter_max_mm: int = 300


def flight_loads():
    q = .5 * 1.225 * 200**2
    alpha = math.atan(20 / 200)
    f = q * 2 * alpha * .1
    return dict(q=q, alpha=alpha, f=f, F=30000., p=300000., V=f*3, M=f*3**2/2)

LOADS = flight_loads()


def section(diameter, thickness):
    ro = diameter/2
    ri = ro-thickness
    return dict(ro=ro, ri=ri, r=(ro+ri)/2,
                A=math.pi*(ro**2-ri**2), I=math.pi/4*(ro**4-ri**4))


def moment_envelope(basis):
    return LOADS['M'] + (LOADS['V']*basis.length if basis.moment_case == 'transfer' else 0)


def amplified_moment(P, M, E, I, length, bow=0):
    """Pinned beam, uniform first-order moment envelope plus sinusoidal bow.

    secant is exact for equal end-couple moment magnitude. Using the uniform
    envelope bounds a same-sign first-order moment diagram within this beam model.
    The bow contribution is exact for its assumed first sinusoidal mode.
    """
    pcr = math.pi**2*E*I/length**2
    if P >= pcr:
        return math.inf, pcr
    amplification = 1/math.cos(.5*length*math.sqrt(P/(E*I)))
    return M*amplification + P*bow/(1-P/pcr), pcr


def quadratic_maximum(fn, left, right):
    """Exact maximum of a quadratic on an interval, from three values."""
    mid = (left+right)/2
    yl, ym, yr = fn(left), fn(mid), fn(right)
    # map interval to z in [-1,1]
    a = (yl+yr)/2-ym
    b = (yr-yl)/2
    choices = [(yl, left), (yr, right)]
    if a < 0:
        z = -b/(2*a)
        if -1 < z < 1:
            c = mid+z*(right-left)/2
            choices.append((fn(c), c))
    return max(choices)


def strength_envelope(mat, s, t, P, M, pressure, shear):
    """Co-located stresses, exact angular maximum for each pressure load path.

    Hoop p*ro/t intentionally upper-bounds mean/inner-radius membrane stress.
    Outer-fibre bending M*ro/I is conservative relative to midsurface stress.
    Composite FI uses sign-dependent QI *surrogate* allowables and positive
    normal-stress cross term; this is not a ply-resolved failure calculation.
    """
    b = M*s['ro']/s['I']
    tau = shear/(math.pi*s['r']*t)
    outputs = []
    for name, pp, relief in [('wall_only', pressure, 0.),
                             ('closed_end', pressure, pressure*math.pi*s['ri']**2/s['A']),
                             ('unpressurised', 0., 0.)]:
        a = -P/s['A']+relief
        hoop = pp*s['ro']/t
        def index(c):
            axial = a+b*c
            shear2 = tau*tau*(1-c*c)
            if not mat.composite:
                return (axial*axial+hoop*hoop-axial*hoop+3*shear2)/mat.yield_stress**2
            X = mat.Xc if axial < 0 else mat.Yt
            return (axial/X)**2+(hoop/mat.Yt)**2+abs(axial*hoop)/(X*mat.Yt)+shear2/mat.S**2
        bounds = [-1., 1.]
        if b and -1 < -a/b < 1:
            bounds.insert(1, -a/b)
        val, c = max(quadratic_maximum(index, l, r) for l, r in zip(bounds, bounds[1:]))
        outputs.append(dict(case=name, index=val, utilisation=math.sqrt(val),
                            theta_deg=math.degrees(math.acos(c)),
                            axial=a+b*c, hoop=hoop, shear=tau*math.sqrt(max(0.,1-c*c))))
    return max(outputs, key=lambda x: x['utilisation']), outputs


def shell_check(mat, diameter, nominal_t, basis=Basis()):
    t = nominal_t*basis.thickness_retention
    s = section(diameter, t)
    P = basis.load_factor*LOADS['F']
    V = basis.load_factor*LOADS['V']
    pressure = basis.load_factor*LOADS['p']
    M, pcr = amplified_moment(P, basis.load_factor*moment_envelope(basis), mat.E,
                              s['I'], basis.length, basis.initial_bow)
    if not math.isfinite(M):
        return dict(passes=False, reason='Euler', utilisation=math.inf)
    phi = math.sqrt(s['r']/t)/16
    gx = min(basis.kdf_cap, 1-.901*(1-math.exp(-phi)))
    gb = min(basis.kdf_cap, 1-.731*(1-math.exp(-phi)))
    classical = mat.E/math.sqrt(3*(1-mat.nu**2))*t/s['r']
    # Avoid claiming elastic capacities beyond available material strength.
    normal_limit = mat.Xc if mat.composite else mat.yield_stress
    sxcr = min(gx*classical, normal_limit)
    sbcr = min(gb*classical, normal_limit)
    # NASA SP-8007 Eq 34/35 moderately-long cylinder shear capacity.
    # max transverse shear used as a conservative uniform-shear SURROGATE.
    taucr = .747*.67*mat.E*(t/s['r'])**1.25/math.sqrt(basis.length/s['r'])
    taucr = min(taucr, mat.S if mat.composite else mat.yield_stress/math.sqrt(3))
    Z = basis.length**2/(s['r']*t)*math.sqrt(1-mat.nu**2)
    gz = .67**(4/3)*Z
    shear_range_ok = 50 < gz < 78*(s['r']/t)**2*(1-mat.nu**2)
    axial_ratio = (P/s['A'])/sxcr
    bending_ratio = (M*s['ro']/s['I'])/sbcr
    shear_ratio = (V/(math.pi*s['r']*t))/taucr
    interaction = axial_ratio+bending_ratio+shear_ratio
    # Eq 16 ideal Brazier limit, with an ADDITIONAL assumed project reduction.
    brazier = .987*mat.E*s['r']*t*t/math.sqrt(1-mat.nu**2)
    oval_ratio = M/(basis.kdf_cap*brazier)
    strength, states = strength_envelope(mat, s, t, P, M, pressure, V)
    utilisations = dict(strength=strength['utilisation'], Euler=P/pcr,
                        shell_interaction=interaction, ovalisation=oval_ratio)
    governing = max(utilisations, key=utilisations.get)
    validity = shear_range_ok and s['r']/t >= 10 and s['r']/t < 1500
    nominal = section(diameter, nominal_t)
    return dict(material=mat.name, diameter_mm=diameter*1000, nominal_t_mm=nominal_t*1000,
                minimum_t_mm=t*1000, shell_mass=nominal['A']*basis.length*mat.density,
                utilisation=utilisations[governing], governing=governing,
                passes=validity and max(utilisations.values()) <= 1., validity=validity,
                utilisations=utilisations, margins={k:1/v-1 for k,v in utilisations.items()},
                applied=dict(P=P,V=V,p=pressure,M=M,first_order_M=basis.load_factor*moment_envelope(basis)),
                section=s, pcr=pcr, gx=gx, gb=gb, sigma_axial_cr=sxcr, sigma_bending_cr=sbcr,
                tau_cr=taucr, classical_brazier=brazier,
                ratios=dict(compression=axial_ratio,bending=bending_ratio,shear=shear_ratio),
                strength_state=strength, strength_states=states,
                r_over_t=s['r']/t, L_over_r=basis.length/s['r'], shear_gZ=gz)


def end_connection(mat, shell, basis=Basis()):
    """All-metal integral inward flanges: analytical connection sizing envelope.

    Equally spaced through bolts, both flanges included in bolt grip; external
    mating flange mass excluded. No friction/preload strength credit. Fitted
    shanks assumed. Ti-6Al-4V bolts are custom material-envelope fasteners, NOT a
    claim about commercial bolt grade. Prying multiplier 2 is an explicit
    assumption requiring a detailed joint check outside this classroom model.
    """
    if mat.composite:
        return None  # no adhesive/interlaminar/bearing allowables in brief
    ro = shell['diameter_mm']/2000
    tn = shell['nominal_t_mm']/1000
    design = shell['applied']
    best = None
    for bolt_d in [.004, .005, .006, .008, .010]:
        hole = bolt_d+.0005
        for width_ratio in [3., 3.25, 3.5, 3.75, 4.]:
            width = width_ratio*bolt_d
            rb = ro-width/2
            rin = ro-width
            if rin <= 0 or width <= 1.5*tn:
                continue
            for n in range(8,65):
                pitch = 2*math.pi*rb/n
                if 2*rb*math.sin(math.pi/n) < 3*bolt_d:
                    continue
                # No beneficial thrust compression credited to bolt tension.
                # Opposite flange sector also checked for full thrust compression.
                end_p = design['p']*math.pi*shell['section']['ri']**2
                Q = end_p/n + 2*design['M']/(n*rb)
                tension = 2*Q  # explicit prying envelope
                flange_force = max(tension, design['P']/n + 2*design['M']/(n*rb))
                shear = 2*design['V']/n  # nonuniform distribution allowance
                core_area = math.pi*(.75*bolt_d)**2/4  # conservative specified min core
                bolt_vm = math.sqrt((tension/core_area)**2+3*(shear/core_area)**2)
                if bolt_vm > 880e6:
                    continue
                for fi in range(8,61):
                    tf = fi*.0005
                    te = tf*basis.thickness_retention
                    ligament = pitch-hole
                    lever = ro-rb
                    bend = 6*flange_force*lever/(ligament*te*te)
                    transverse = flange_force/(ligament*te)
                    flange_vm = math.sqrt(bend*bend+3*transverse*transverse)
                    bearing = shear/(hole*te)
                    pullthrough = tension/(math.pi*(1.8*bolt_d)*te)
                    # root concentration envelope, assuming machined filleted flange
                    root = 1.5*flange_vm
                    washer_area=math.pi*((1.1*bolt_d)**2-(hole/2)**2)
                    strip_area=.5*math.pi*(.75*bolt_d)*(.7*bolt_d)
                    utils=dict(bolt=bolt_vm/880e6, flange=root/mat.yield_stress,
                               washer_bearing=tension/(washer_area*mat.yield_stress),
                               thread_strip=tension/(strip_area*(880e6/math.sqrt(3))),
                               bearing=bearing/mat.yield_stress,
                               pullthrough=pullthrough/(mat.yield_stress/math.sqrt(3)))
                    if max(utils.values()) > 1:
                        continue
                    # Base shell spans entire 1500 mm. Count only flange addition.
                    # Ignore removed holes for conservative mass; both end rings included.
                    ring_extra = 2*math.pi*((ro-tn)**2-rin**2)*tf*mat.density
                    # Two 20mm tapered root bands: additional thickness avg 0.5*t.
                    band_length=.020
                    band_extra=2*math.pi*((ro-tn)**2-(ro-1.5*tn)**2)*band_length*mat.density
                    # Bolt mass: shank grip + equivalent head/nut + two washers.
                    grip=2*tf+.004
                    shank=math.pi*bolt_d**2/4*grip
                    head_nut=2*math.pi*(.9*bolt_d)**2*(.7*bolt_d)
                    washers=2*math.pi*((1.1*bolt_d)**2-(hole/2)**2)*(.2*bolt_d)
                    bolts_mass=2*n*(shank+head_nut+washers)*4430
                    total=shell['shell_mass']+ring_extra+band_extra+bolts_mass
                    candidate=dict(bolt_material="Titanium Ti-6Al-4V",bolts_per_end=n,bolt_d_mm=bolt_d*1000,
                        hole_mm=hole*1000,bolt_circle_mm=2*rb*1000,
                        flange_width_mm=width*1000,flange_t_mm=tf*1000,
                        flange_bore_mm=2*rin*1000,root_band_mm=20.,
                        ring_extra_mass=ring_extra,root_band_extra_mass=band_extra,
                        fastener_mass=bolts_mass,total_mass=total,
                        bolt_tension=tension,bolt_shear=shear,
                        utilisations=utils,margins={k:1/v-1 for k,v in utils.items()},
                        rigidity_indicator=(tf*width**3/12)/((tn**3/(12*(1-mat.nu**2)))*math.sqrt(ro*tn)))
                    if best is None or total < best['total_mass']:
                        best=candidate
                    break
    return best


def minimum_shell(mat, diameter, basis):
    # Metals: 0.05mm machining increments, >=0.8mm. Composites: 8-ply
    # symmetric balanced QI blocks, 0.125mm assumed cured ply -> 1mm increments.
    step = .001 if mat.composite else .00005
    start = 1 if mat.composite else 16
    for k in range(start, int(.008/step)+1):
        result=shell_check(mat,diameter,k*step,basis)
        if result['passes']:
            return result
    return None


def optimise_at_diameter(mat, diameter, basis):
    first=minimum_shell(mat,diameter,basis)
    if first is None:
        return None
    if mat.composite:
        first.update(connection=None, objective_mass=first['shell_mass'],
                     mass_scope='shell only; interface unresolved')
        return first
    best=None
    start=round(first['nominal_t_mm']/.05)
    for k in range(start,161):
        nominal_t=k*.00005
        mass=section(diameter,nominal_t)['A']*basis.length*mat.density
        # Monotonically increasing shell mass is a lower bound on assembly mass.
        if best and mass >= best['objective_mass']:
            break
        x=first if k==start else shell_check(mat,diameter,nominal_t,basis)
        if not x['passes']:
            continue
        joint=end_connection(mat,x,basis)
        if joint:
            x.update(connection=joint,objective_mass=joint['total_mass'],
                     mass_scope='barrel + integral flanges + modelled fasteners')
            if best is None or x['objective_mass'] < best['objective_mass']:
                best=x
    return best


def trade(basis):
    rows=[]
    winners=[]
    for mat in MATERIALS:
        candidates=[]
        for d in range(basis.diameter_min_mm,basis.diameter_max_mm+1):
            result=optimise_at_diameter(mat,d/1000,basis)
            if result:
                rows.append(result)
                candidates.append(result)
        if candidates:
            winners.append(min(candidates,key=lambda x:x['objective_mass']))
    return winners,rows


def main():
    out=ROOT/'results'
    out.mkdir(exist_ok=True)
    basis=Basis()
    winners, rows=trade(basis)
    metals=[x for x in winners if x['connection']]
    selected=min(metals,key=lambda x:x['objective_mass'])
    material=next(m for m in MATERIALS if m.name==selected['material'])
    # Select separately for the conservative physical-transfer envelope.
    robust_basis=replace(basis,moment_case='transfer')
    robust_winners,robust_rows=trade(robust_basis)
    robust=min((x for x in robust_winners if x['connection']),key=lambda x:x['objective_mass'])
    sensitivities=[]
    for factor in [1.25,1.5,2.0]:
        for cap in [.2,.35,.5]:
            b=replace(basis,load_factor=factor,kdf_cap=cap)
            # Reoptimise selected metal, not all materials, for transparent sensitivity.
            candidates=[]
            for d in range(basis.diameter_min_mm,basis.diameter_max_mm+1,2):
                x=optimise_at_diameter(material,d/1000,b)
                if x:
                    candidates.append((x['objective_mass'],d,x['nominal_t_mm']))
            mass,d,t=min(candidates)
            fixed=shell_check(material,selected['diameter_mm']/1000,selected['nominal_t_mm']/1000,b)
            sensitivities.append(dict(load_factor=factor,kdf_cap=cap,total_mass=mass,diameter_mm=d,nominal_t_mm=t,
                                      original_shell_utilisation=fixed['utilisation']))
    payload=dict(basis=asdict(basis),loads=LOADS,materials=[asdict(m) for m in MATERIALS],
                 winners=winners,selected=selected,transfer_basis=asdict(robust_basis),
                 transfer_winners=robust_winners,transfer_selected=robust,
                 sensitivities=sensitivities)
    (out/'design.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    for name,data in [('trade_study.csv',rows),('transfer_trade_study.csv',robust_rows)]:
        keys=['material','diameter_mm','nominal_t_mm','minimum_t_mm','shell_mass','objective_mass','mass_scope','governing','utilisation']
        with (out/name).open('w',newline='') as fp:
            writer=csv.DictWriter(fp,fieldnames=keys,lineterminator="\n");writer.writeheader()
            writer.writerows({k:r[k] for k in keys} for r in data)
    print('Brief optimum within stated all-metal family:',selected['material'],selected['diameter_mm'],selected['nominal_t_mm'],selected['objective_mass'])
    print('Transfer-envelope optimum:',robust['material'],robust['diameter_mm'],robust['nominal_t_mm'],robust['objective_mass'])
    print('Wrote results/design.json and two trade CSV files')

if __name__ == '__main__':
    main()
