"""Analytical sizing of the Drakkar shell. SI units; see docs/METHOD.md."""
from dataclasses import dataclass
import math

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
    Material('Aluminium 7075-T6', 71.7e9, .33, 2810, 402e6),
    Material('Titanium Ti-6Al-4V', 113.8e9, .31, 4430, 704e6),
    Material('Steel 4130', 205e9, .29, 7850, 368e6),
    Material('Magnesium AZ31B', 45e9, .35, 1770, 176e6),
    Material('Carbon/Epoxy QI', 52.3e9, .30, 1600, Xc=480e6, Yt=400e6, S=160e6),
    Material('Glass/Epoxy QI', 23.8e9, .30, 1900, Xc=240e6, Yt=200e6, S=80e6),
    Material('Aramid/Epoxy QI', 33.3e9, .34, 1400, Xc=160e6, Yt=240e6, S=64e6),
)
LENGTH = 1.5
FACTOR = 1.1

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

def metal_strength(material,s,t,P,M,p,V,pressure_path):
    """Exact circumferential von Mises maximum."""
    relief=p*math.pi*s['ri']**2/s['A'] if pressure_path=='closed_end' else 0.
    a=-P/s['A']+relief; b=M*s['ro']/s['I']; h=p*s['ro']/t
    tau=V/(math.pi*s['r']*t)
    def index(c):
        x=a+b*c
        return (x*x+h*h-x*h+3*tau*tau*(1-c*c))/material.yield_stress**2
    value,c=quadratic_maximum(index,-1.,1.)
    return dict(utilisation=math.sqrt(value),index=value,theta_deg=math.degrees(math.acos(c)),
        axial=a+b*c,hoop=h,shear=tau*math.sqrt(max(0.,1-c*c)),criterion='von Mises',case=pressure_path)

def knockdown(material):
    return .50 if material.composite else .40


def beam_envelope(P, moment, E, I, length=LENGTH):
    """Uniform first-order moment majorant; simple-supported beam-column."""
    pcr = math.pi**2 * E * I / length**2
    if P >= pcr:
        return None
    beta = length/2 * math.sqrt(P/(E*I))
    amplified = moment / math.cos(beta)
    secondary_shear = moment * math.sqrt(P/(E*I)) * math.tan(beta)
    return amplified, secondary_shear, pcr


def compression_bound(axial, bending, shear, hoop):
    """Maximum of a - b*c + (s^2/h)*(1-c^2), c=cos(theta).

    h>0 is required. Completion of the square bounds the Donnell geometric
    energy of the combined axial, bending, shear and tensile hoop resultants.
    """
    if hoop <= 0:
        raise ValueError('Pressure-supported bound requires positive hoop tension')
    return quadratic_maximum(lambda c: axial-bending*c+shear**2/hoop*(1-c*c), -1., 1.)


def composite_envelope(material,s,t,P,M,p,V,pressure_path):
    """Upper bound for every PSD quadratic criterion with given uniaxial limits.

    If Q is PSD with diag(Q)=1, z^T Q z <= (sum(abs(z)))^2.
    Circumferential extrema are solved analytically on each stress-sign interval.
    """
    relief=p*math.pi*s['ri']**2/s['A'] if pressure_path=='closed_end' else 0.
    a=-P/s['A']+relief; b=M*s['ro']/s['I']; h=p*s['ro']/t
    tau=V/(math.pi*s['r']*t)
    bounds=[-1.,1.]
    if b and -1 < -a/b < 1:bounds.insert(1,-a/b)
    options=[]
    for left,right in zip(bounds,bounds[1:]):
        sign=1 if a+b*(left+right)/2>=0 else -1
        allowable=material.Yt if sign>0 else material.Xc
        B=sign*b/allowable; C=tau/material.S
        critical=B/math.hypot(B,C) if B or C else 0.
        for c in [left,right,max(left,min(right,critical))]:
            value=sign*(a+b*c)/allowable+h/material.Yt+C*math.sqrt(max(0.,1-c*c))
            options.append((value,c))
    value,c=max(options)
    return dict(utilisation=value,index=value*value,theta_deg=math.degrees(math.acos(c)),
        axial=a+b*c,hoop=h,shear=tau*math.sqrt(max(0.,1-c*c)),
        criterion='PSD quadratic envelope',case=pressure_path)


def evaluate(material, diameter_mm, wall_mm, case='primary', gust=20., pressure_path='wall_only'):
    D=diameter_mm/1000; t=wall_mm/1000
    if D <= 0 or t <= 0 or 2*t >= D:
        raise ValueError('Require D>0 and 0<t<D/2')
    if case not in ('primary','transfer') or pressure_path not in ('wall_only','closed_end'):
        raise ValueError('Invalid analysis case, pressure load path')
    s=section(D,t); loads=flight_loads(gust)
    P=FACTOR*loads['F']; p=FACTOR*loads['p']; V=FACTOR*loads['V']
    first=FACTOR*(loads['M']+(loads['V']*LENGTH if case=='transfer' else 0))
    beam=beam_envelope(P,first,material.E,s['I'])
    if beam is None:
        return dict(passes=False, reason='Euler instability', material=material.name,
                    diameter_mm=diameter_mm,nominal_t_mm=wall_mm)
    moment,secondary_shear,pcr=beam
    total_shear=V+secondary_shear
    # Pressure support is used only to bound transverse shear. No empirical
    # pressure improvement to the axial shell critical stress is taken.
    hoop=p*s['ri']/t  # inner-radius value is a lower membrane-tension bound
    axial=P/s['A']; bending=moment*s['ro']/s['I']; shear=total_shear/(math.pi*s['r']*t)
    effective,cosine=compression_bound(axial,bending,shear,hoop)
    k=knockdown(material)
    critical=k*material.E*t/(s['r']*math.sqrt(3*(1-material.nu**2)))
    normal_limit=min(material.Xc,material.Yt) if material.composite else material.yield_stress
    elastic_capacity=critical <= normal_limit
    if material.composite:
        strength=composite_envelope(material,s,t,P,moment,p,total_shear,pressure_path)
    else:
        strength=metal_strength(material,s,t,P,moment,p,total_shear,pressure_path)
    brazier=.987*material.E*s['r']*t*t/math.sqrt(1-material.nu**2)
    utils=dict(strength=strength['utilisation'],Euler=P/pcr,local_shell=effective/critical,ovalisation=moment/brazier)
    governing=max(utils,key=utils.get)
    valid=10 <= s['r']/t < 1500 and elastic_capacity
    return dict(material=material.name,case=case,diameter_mm=diameter_mm,nominal_t_mm=wall_mm,
        shell_mass=s['A']*LENGTH*material.density,passes=valid and max(utils.values())<=1,
        applicability=dict(thin_shell=10 <= s['r']/t < 1500,elastic_capacity=elastic_capacity),
        utilisation=utils[governing],governing=governing,utilisations=utils,
        margins={key:(1/value-1 if value else None) for key,value in utils.items()},
        section=s,knockdown=k,critical_axial_stress=critical,normal_allowable=normal_limit,
        effective_compression=effective,critical_angle_deg=math.degrees(math.acos(cosine)),
        compression_terms=dict(axial=axial,bending=bending,peak_shear=shear,hoop_lower=hoop),
        applied=dict(P=P,V=V,secondary_shear=secondary_shear,total_shear=total_shear,p=p,first_order_M=first,M=moment),
        pcr=pcr,brazier_moment=brazier,strength_state=strength,pressure_path=pressure_path,
        basis=dict(length=LENGTH,load_factor=FACTOR,gust_velocity=gust),mass_scope='uniform shell',
        analysis_scope='prescribed course model; local Donnell energy bound and global beam-column checks')


def maximum_wall(material,D):
    """Thin-shell and elastic-capacity domain upper bound, in mm."""
    allowable=min(material.Xc,material.Yt) if material.composite else material.yield_stress
    ratio=allowable*math.sqrt(3*(1-material.nu**2))/(knockdown(material)*material.E)
    return min(D/21,ratio*D/(2+ratio))


def minimum_wall(material,D,case='primary',step=.01):
    # All utilisations decrease with increasing wall over the admitted domain.
    # Independent exhaustive-grid comparisons verify the integer bisection.
    upper=math.floor(maximum_wall(material,D)/step+1e-10)
    if upper < 1 or not evaluate(material,D,upper*step,case)['passes']:
        return None
    lo,hi=1,upper
    while lo < hi:
        mid=(lo+hi)//2
        if evaluate(material,D,mid*step,case)['passes']:hi=mid
        else:lo=mid+1
    return evaluate(material,D,lo*step,case)


def optimise(materials,case='primary',diameter_step=1.,wall_step=.01):
    rows=[]; winners=[]
    for material in materials:
        candidates=[]
        for i in range(1,round(300/diameter_step)+1):
            D=i*diameter_step
            row=minimum_wall(material,D,case,wall_step)
            if row is not None:candidates.append(row);rows.append(row)
        if not candidates:
            raise RuntimeError(f'No feasible design for {material.name}: {case}')
        winners.append(min(candidates,key=lambda row:row['shell_mass']))
    return winners,rows
