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
    load_multiplier: float = 1.1  # adopted proportional design load factor
    required_safety_factor: float | None = 1.1  # team choice, not specified by brief
    moment_case: str = 'brief'
    pressure_path: str = 'wall_only'  # brief specifies wall pressure, not end thrust
    diameter_min_mm: int = 1  # numerical search resolution, not a requirement
    diameter_max_mm: int = 300
    thickness_step_mm: float = .01  # numerical resolution, not manufacturing tolerance
    shell_knockdown: float | None = None  # None retains the Revision A model
    gust_velocity: float = 20.0


def flight_loads(gust_velocity=20.0):
    q = .5 * 1.225 * 200**2
    alpha = math.atan(gust_velocity / 200)
    f = q * 2 * alpha * .1
    return dict(q=q, alpha=alpha, f=f, F=30000., p=300000., V=f*3, M=f*3**2/2)

LOADS = flight_loads()


def section(diameter, thickness):
    ro = diameter/2
    ri = ro-thickness
    return dict(ro=ro, ri=ri, r=(ro+ri)/2,
                A=math.pi*(ro**2-ri**2), I=math.pi/4*(ro**4-ri**4))


def moment_envelope(basis):
    loads = flight_loads(basis.gust_velocity)
    return loads['M'] + (loads['V']*basis.length if basis.moment_case == 'transfer' else 0)


def amplified_moment(P, M, E, I, length):
    """Pinned beam, uniform first-order moment envelope.

    secant is exact for equal end-couple moment magnitude. Using the uniform
    envelope bounds a same-sign first-order moment diagram within this beam model.
    """
    pcr = math.pi**2*E*I/length**2
    if P >= pcr:
        return math.inf, pcr
    amplification = 1/math.cos(.5*length*math.sqrt(P/(E*I)))
    return M*amplification, pcr


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


def strength_envelope(mat, s, t, P, M, pressure, shear, pressure_path="wall_only"):
    """Co-located stresses, exact angular maximum for each pressure load path.

    Hoop p*ro/t intentionally upper-bounds mean/inner-radius membrane stress.
    Outer-fibre bending M*ro/I is conservative relative to midsurface stress.
    Composite FI uses sign-dependent QI *surrogate* allowables and zero
    normal-stress cross term; this is not a ply-resolved failure calculation.
    """
    b = M*s['ro']/s['I']
    tau = shear/(math.pi*s['r']*t)
    outputs = []
    relief = pressure*math.pi*s["ri"]**2/s["A"] if pressure_path == "closed_end" else 0.
    for name, pp, relief in [(pressure_path, pressure, relief)]:
        a = -P/s['A']+relief
        hoop = pp*s['ro']/t
        def index(c):
            axial = a+b*c
            shear2 = tau*tau*(1-c*c)
            if not mat.composite:
                return (axial*axial+hoop*hoop-axial*hoop+3*shear2)/mat.yield_stress**2
            X = mat.Xc if axial < 0 else mat.Yt
            return (axial/X)**2+(hoop/mat.Yt)**2+shear2/mat.S**2
        bounds = [-1., 1.]
        if b and -1 < -a/b < 1:
            bounds.insert(1, -a/b)
        val, c = max(quadratic_maximum(index, l, r) for l, r in zip(bounds, bounds[1:]))
        outputs.append(dict(case=name, index=val, utilisation=math.sqrt(val),
                            theta_deg=math.degrees(math.acos(c)),
                            axial=a+b*c, hoop=hoop, shear=tau*math.sqrt(max(0.,1-c*c))))
    return max(outputs, key=lambda x: x['utilisation']), outputs


def shell_check(mat, diameter, nominal_t, basis=Basis()):
    t = nominal_t
    s = section(diameter, t)
    loads = flight_loads(basis.gust_velocity)
    P = basis.load_multiplier*loads['F']
    V = basis.load_multiplier*loads['V']
    pressure = basis.load_multiplier*loads['p']
    M, pcr = amplified_moment(P, basis.load_multiplier*moment_envelope(basis), mat.E,
                              s['I'], basis.length)
    if not math.isfinite(M):
        return dict(passes=False, reason='Euler', utilisation=math.inf)
    phi = math.sqrt(s['r']/t)/16
    gx = 1-.901*(1-math.exp(-phi))
    gb = 1-.731*(1-math.exp(-phi))
    if basis.shell_knockdown is not None:
        gx = gb = basis.shell_knockdown
    classical = mat.E/math.sqrt(3*(1-mat.nu**2))*t/s['r']
    # Declared course screening approximation, NOT an inelastic buckling solution.
    normal_limit = mat.Xc if mat.composite else mat.yield_stress
    sxcr = min(gx*classical, normal_limit)
    sbcr = min(gb*classical, normal_limit)
    # NASA SP-8007 Eq 34/35 moderately-long cylinder shear capacity.
    # Peak transverse shear used as a provisional SURROGATE; conservatism unproven.
    # Assay interpretation: prescribed k replaces the shear reduction too;
    # it is not multiplied into an already knocked-down capacity.
    shear_reduction = .67 if basis.shell_knockdown is None else basis.shell_knockdown
    taucr = .747*shear_reduction*mat.E*(t/s['r'])**1.25/math.sqrt(basis.length/s['r'])
    taucr = min(taucr, mat.S if mat.composite else mat.yield_stress/math.sqrt(3))
    Z = basis.length**2/(s['r']*t)*math.sqrt(1-mat.nu**2)
    gz = shear_reduction**(4/3)*Z
    shear_range_ok = 50 < gz < 78*(s['r']/t)**2*(1-mat.nu**2)
    axial_ratio = (P/s['A'])/sxcr
    bending_ratio = (M*s['ro']/s['I'])/sbcr
    shear_ratio = (V/(math.pi*s['r']*t))/taucr
    interaction = axial_ratio+bending_ratio+shear_ratio
    # Eq 16 ideal Brazier diagnostic; unpressurised reference capacity.
    brazier = .987*mat.E*s['r']*t*t/math.sqrt(1-mat.nu**2)
    oval_ratio = M/brazier
    strength, states = strength_envelope(mat, s, t, P, M, pressure, V, basis.pressure_path)
    utilisations = dict(strength=strength['utilisation'], Euler=P/pcr,
                        shell_interaction=interaction, ovalisation=oval_ratio)
    governing = max(utilisations, key=utilisations.get)
    validity = shear_range_ok and s['r']/t >= 10 and s['r']/t < 1500
    assumption_flags = ['transverse_shear_surrogate', 'linear_local_interaction',
                        'ideal_brazier_without_end_ring_model']
    if s['r']/t and basis.length/s['r'] > 5:
        assumption_flags.append('long_shell_correlation_extrapolation')
    if max(gx, gb)*classical > normal_limit:
        assumption_flags.append('material_strength_cap_active')
    if mat.composite:
        assumption_flags.append('equivalent_QI_failure_model')
    nominal = section(diameter, nominal_t)
    return dict(material=mat.name, diameter_mm=diameter*1000, nominal_t_mm=nominal_t*1000,
                minimum_t_mm=t*1000, shell_mass=nominal['A']*basis.length*mat.density,
                utilisation=utilisations[governing], governing=governing,
                passes=validity and max(utilisations.values()) <= 1., validity=validity,
                assumption_flags=assumption_flags, structural_verification="incomplete",
                utilisations=utilisations, margins={k:1/v-1 for k,v in utilisations.items()},
                applied=dict(P=P,V=V,p=pressure,M=M,first_order_M=basis.load_multiplier*moment_envelope(basis)),
                section=s, pcr=pcr, gx=gx, gb=gb, sigma_axial_cr=sxcr, sigma_bending_cr=sbcr,
                tau_cr=taucr, classical_brazier=brazier,
                ratios=dict(compression=axial_ratio,bending=bending_ratio,shear=shear_ratio),
                strength_state=strength, strength_states=states,
                r_over_t=s['r']/t, L_over_r=basis.length/s['r'], shear_gZ=gz)


def minimum_shell(mat, diameter, basis):
    # Same numerical grid for every material. No specified ply thickness or
    # manufacturing minimum; manufacturing and actual laminate remain unresolved.
    step = basis.thickness_step_mm/1000
    for k in range(1, math.floor((diameter/21)/step)+1):
        result = shell_check(mat, diameter, k*step, basis)
        if result['passes']:
            result.update(connection=None, assembly_mass=None,
                          objective_mass=result['shell_mass'], mass_scope='shell only',
                          competition_compliance='unresolved',
                          screening_status='equivalent-QI screen' if mat.composite else 'metal shell screen')
            return result
    return None


def trade(basis, materials=MATERIALS):
    rows=[]; winners=[]
    for mat in materials:
        candidates=[]
        for d in range(basis.diameter_min_mm,basis.diameter_max_mm+1):
            result=minimum_shell(mat,d/1000,basis)
            if result:
                rows.append(result); candidates.append(result)
        if candidates:
            winners.append(min(candidates,key=lambda x:x['shell_mass']))
    return winners,rows


def main():
    out=ROOT.parent/'data/original';out.mkdir(exist_ok=True)
    basis=Basis()
    winners,rows=trade(basis)
    metal_names={m.name for m in MATERIALS if not m.composite}
    selected=min((x for x in winners if x['material'] in metal_names),key=lambda x:x['shell_mass'])
    transfer_basis=replace(basis,moment_case='transfer')
    transfer_winners,transfer_rows=trade(transfer_basis)
    transfer_selected=min((x for x in transfer_winners if x['material'] in metal_names),key=lambda x:x['shell_mass'])
    # Explicit scenarios; reported separately from the design load factor.
    sensitivities=[]
    for multiplier in [1.,1.1,1.25,1.5,2.]:
        ws,_=trade(replace(basis,load_multiplier=multiplier)) if multiplier!=basis.load_multiplier else (winners,rows)
        sensitivities.extend(dict(load_multiplier=multiplier,material=x['material'],
                                 diameter_mm=x['diameter_mm'],nominal_t_mm=x['nominal_t_mm'],
                                 shell_mass=x['shell_mass']) for x in ws)
    # End pressure transfer is unspecified. A separate strength-only scenario
    # shows its effect without pressure-stabilised buckling credit.
    pressure_scenarios=[]
    for x in winners:
        mat=next(m for m in MATERIALS if m.name==x['material'])
        alt=shell_check(mat,x['diameter_mm']/1000,x['nominal_t_mm']/1000,
                        replace(basis,pressure_path='closed_end'))
        pressure_scenarios.append(dict(material=mat.name,wall_only_strength=x['utilisations']['strength'],
                                       closed_end_strength=alt['utilisations']['strength']))
    payload=dict(basis=asdict(basis),loads=LOADS,materials=[asdict(m) for m in MATERIALS],
                 status='factor-1.1 conditional shell screening; competition compliance unresolved',
                 assumption_register='docs/DESIGN_ASSUMPTIONS.md',
                 safety_factor_source='Adopted design load multiplier; applied once to F, M, V and p',
                 assembly_mass=None,required_safety_factor=basis.required_safety_factor,
                 removed_assumptions=['1.5 mandatory load factor','5% thickness loss','1.5 mm bow',
                   '0.35 shell cap','0.35 Brazier multiplier','unpressurised load case',
                   'assumed bolt/flange joint','0.125 mm ply and 8-ply thickness grid',
                   '0.8 mm minimum metal wall','positive composite cross term'],
                 unresolved=['instructor acceptance of team factor 1.1','inelastic shell buckling capacity',
                   'transverse-shear capacity and combined-load validation','long-shell interaction',
                   'ring/connection geometry and mass',
                   'manufacturing process and tolerances','composite laminate and interaction data',
                   'pressure end-load path','pressure-stabilised combined buckling validation'],
                 winners=winners,selected=selected,transfer_basis=asdict(transfer_basis),
                 transfer_winners=transfer_winners,transfer_selected=transfer_selected,
                 sensitivities=sensitivities,pressure_scenarios=pressure_scenarios)
    (out/'design.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    for name,data in [('trade_study.csv',rows),('transfer_trade_study.csv',transfer_rows)]:
        keys=['material','diameter_mm','nominal_t_mm','shell_mass','mass_scope','governing','utilisation','competition_compliance']
        with (out/name).open('w',newline='') as fp:
            writer=csv.DictWriter(fp,fieldnames=keys,lineterminator="\n");writer.writeheader()
            writer.writerows({k:r[k] for k in keys} for r in data)
    print(payload['status'])
    for x in winners:
        print(x['material'],x['diameter_mm'],x['nominal_t_mm'],x['shell_mass'])

if __name__=='__main__':
    main()
