"""Independent N/mm/MPa arithmetic audit; does not import the design model.

Verifies saved numbers, not empirical applicability or competition compliance.
A Fourier-series beam solution checks the secant formula independently; angular
sampling checks the reported strength extrema. No FEA is used.
"""
from pathlib import Path
import csv
import json
import math

ROOT=Path(__file__).resolve().parent
MATS={
 'Aluminium 7075-T6':(71700,.33,2810,503,0,0,0),
 'Titanium Ti-6Al-4V':(113800,.31,4430,880,0,0,0),
 'Steel 4130':(205000,.29,7850,460,0,0,0),
 'Magnesium AZ31B':(45000,.35,1770,220,0,0,0),
 'Carbon/Epoxy QI':(55000,.30,1600,0,600,500,200),
 'Glass/Epoxy QI':(25000,.30,1900,0,300,250,100),
 'Aramid/Epoxy QI':(35000,.34,1400,0,200,300,80),
}
Q=.5*1.225*200**2
ALPHA=math.atan2(20,200)
LINE_LOAD=Q*2*ALPHA*.1
V0=LINE_LOAD*3
M0=LINE_LOAD*3**2/2

def calculate(name,D,t,multiplier=1.,transfer=False):
    E,nu,rho,sy,Xc,Yt,S=MATS[name]
    L=1500.;di=D-2*t;r=(D+di)/4
    A=math.pi*t*(D-t)
    I=A*(D*D+di*di)/16
    P=30000*multiplier;V=V0*multiplier;p=.3*multiplier
    moment0=(M0+(V0*1.5 if transfer else 0))*1000*multiplier
    Pcr=math.pi**2*E*I/L**2
    beta=math.pi/2*math.sqrt(P/Pcr)
    moment=moment0/math.cos(beta)
    # EI*y'' + P*y = -M0 with y(0)=y(L)=0: sine series, midpoint.
    def fourier(terms):
        return sum(4*moment0*(-1)**k/((2*k+1)*math.pi*(E*I*((2*k+1)*math.pi/L)**2-P)) for k in range(terms))
    mid_deflection=fourier(1000)
    series_moment=moment0+P*mid_deflection
    series_error=abs(series_moment/moment-1)
    assert series_error<1e-8,(name,series_error)
    axial=P/A;bending=moment*D/(2*I);hoop=p*D/(2*t);shear=2*V/A
    strength=-1;angle=0;index=-1
    for i in range(7200):
        a=i*math.pi/3600;sx=-axial+bending*math.cos(a);tau=shear*math.sin(a)
        if sy:
            value=math.sqrt(sx*sx+hoop*hoop-sx*hoop+3*tau*tau)/sy
        else:
            value=math.sqrt((sx/(Xc if sx<0 else Yt))**2+(hoop/Yt)**2+(tau/S)**2)
        if value>strength:strength=value;angle=math.degrees(a);index=value*value
    phi=math.sqrt(r/t)/16
    gx=.099+.901*math.exp(-phi);gb=.269+.731*math.exp(-phi)
    classic=E*t/(r*math.sqrt(3*(1-nu*nu)))
    raw_x=gx*classic;raw_b=gb*classic;normal=sy or Xc
    cap_x=min(raw_x,normal);cap_b=min(raw_b,normal)
    tau_cr=min(.747*.67*E*(t/r)**1.25*math.sqrt(r/L),sy/math.sqrt(3) if sy else S)
    ratios=[axial/cap_x,bending/cap_b,shear/tau_cr]
    brazier=.987*E*r*t*t/math.sqrt(1-nu*nu)
    Z=L*L*math.sqrt(1-nu*nu)/(r*t);gZ=.67**(4/3)*Z;upper=78*(r/t)**2*(1-nu*nu)
    assert 50<gZ<upper
    utils=dict(strength=strength,Euler=P/Pcr,shell_interaction=sum(ratios),ovalisation=moment/brazier)
    return dict(material=name,D=D,t=t,di=di,r=r,A=A,I=I,E=E,nu=nu,rho=rho,sy=sy,Xc=Xc,Yt=Yt,S=S,
        multiplier=multiplier,transfer=transfer,mass=A*L*rho/1e9,P=P,V=V,p=p,M0=moment0,M=moment,
        Pcr=Pcr,beta=beta,amplification=moment/moment0,deflection=mid_deflection,series_error=series_error,
        axial=axial,bending=bending,hoop=hoop,shear=shear,angle=angle,FI=index,
        phi=phi,gx=gx,gb=gb,classic=classic,raw_x=raw_x,raw_b=raw_b,cap_x=cap_x,cap_b=cap_b,
        tau_cr=tau_cr,ratios=ratios,brazier=brazier,Z=Z,gZ=gZ,gZ_upper=upper,
        utilisations=utils,screen_pass=max(utils.values())<=1)

def close(a,b,label):
    assert math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-9),(label,a,b)

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows])

def worked(c):
    u=c['utilisations'];a,b,h=c['ratios']
    strength=(f"sqrt[(-{c['axial']+c['bending']:.6f})^2 + ({c['hoop']:.6f})^2 - (-{c['axial']+c['bending']:.6f})*({c['hoop']:.6f})] / {c['sy']:g}" if c['sy'] else
      f"sqrt[((-{c['axial']+c['bending']:.6f})/{c['Xc']:g})^2 + ({c['hoop']:.6f}/{c['Yt']:g})^2]")
    # All stored finalists attain the worst material criterion at theta = 180 deg.
    assert abs(c['angle']-180)<.051,c['angle']
    return f'''### {c['material']} - {'transfer' if c['transfer'] else 'brief'}, multiplier {c['multiplier']:g}

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = {c['E']:g}; nu = {c['nu']:g}; density = {c['rho']:g} kg/m^3
D = {c['D']:.3f}; t = {c['t']:.3f}; L = 1500
Di = D - 2t = {c['di']:.6f}
r = (D + Di)/4 = {c['r']:.6f}
A = pi*t*(D-t) = {c['A']:.9f}
I = A*(D^2+Di^2)/16 = {c['I']:.9f}
m = A*1500*density/10^9 = {c['mass']:.9f} kg

P = {c['P']:.6f}; V = {c['V']:.6f}; p = {c['p']:.6f}
M0 = {c['M0']:.6f}
Pcr = pi^2*E*I/1500^2 = {c['Pcr']:.6f}
beta = (pi/2)*sqrt(P/Pcr) = {c['beta']:.9f}
M = M0/cos(beta) = {c['M']:.6f}
amplification = {c['amplification']:.9f}
Midpoint beam deflection from Fourier check = {c['deflection']:.6f} mm
Euler U = P/Pcr = {u['Euler']:.9f}

Compression stress P/A = {c['axial']:.6f}
Bending stress M*(D/2)/I = {c['bending']:.6f}
Hoop stress p*(D/2)/t = {c['hoop']:.6f}
Peak transverse shear 2V/A = {c['shear']:.6f}
sx(theta) = -{c['axial']:.6f} + {c['bending']:.6f}*cos(theta)
tau(theta) = {c['shear']:.6f}*sin(theta)
Worst material angle = {c['angle']:.2f} deg
Material utilisation = {strength}
                    = {u['strength']:.9f}
Squared material utilisation = {c['FI']:.9f}

r/t = {c['r']/c['t']:.6f}; L/r = {1500/c['r']:.6f}
phi = sqrt(r/t)/16 = {c['phi']:.9f}
gx = 1-0.901*(1-exp(-phi)) = {c['gx']:.9f}
gb = 1-0.731*(1-exp(-phi)) = {c['gb']:.9f}
classical = E*(t/r)/sqrt(3*(1-nu^2)) = {c['classic']:.6f}
raw axial buckling stress = gx*classical = {c['raw_x']:.6f}
raw bending buckling stress = gb*classical = {c['raw_b']:.6f}
Code's capped axial / bending capacities = {c['cap_x']:.6f} / {c['cap_b']:.6f}
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = {c['Z']:.6f}
gamma_s^(3/4) = 0.67; gamma_s*Z = {c['gZ']:.6f}
Moderate-length torsion range: 50 < gamma_s*Z < {c['gZ_upper']:.6f}
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = {c['tau_cr']:.6f}
Code's local interaction = compression + bending + shear ratios
                        = {a:.9f} + {b:.9f} + {h:.9f}
                        = {u['shell_interaction']:.9f}
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = {c['brazier']:.6f}
U_oval = M/M_Brazier = {u['ovalisation']:.9f}
Numerical screen passes: {c['screen_pass']}
Competition compliance: NOT established by this calculation
```
'''

def main():
    data_dir = ROOT.parent / 'data/original'
    data=json.loads((data_dir/'design.json').read_text());audited=[];errors=[]
    for field,value in [('q',Q),('alpha',ALPHA),('f',LINE_LOAD),('F',30000),('p',300000),('V',V0),('M',M0)]:close(value,data['loads'][field],field)
    for group,transfer in [('winners',False),('transfer_winners',True)]:
        for row in data[group]:
            c=calculate(row['material'],row['diameter_mm'],row['nominal_t_mm'],multiplier=data['basis']['load_multiplier'],transfer=transfer)
            for key,value in c['utilisations'].items():close(value,row['utilisations'][key],(row['material'],key))
            close(c['A'],row['section']['A']*1e6,'area');close(c['I'],row['section']['I']*1e12,'I')
            close(c['mass'],row['shell_mass'],'mass');close(c['M'],row['applied']['M']*1000,'moment')
            close(c['Pcr'],row['pcr'],'Euler');close(c['tau_cr'],row['tau_cr']/1e6,'tau_cr')
            close(c['brazier'],row['classical_brazier']*1000,'Brazier')
            for key in ['gx','gb']:close(c[key],row[key],key)
            audited.append(c)
    factor_cases=[]
    for row in data['sensitivities']:
        c=calculate(row['material'],row['diameter_mm'],row['nominal_t_mm'],row['load_multiplier'])
        close(c['mass'],row['shell_mass'],'scenario mass');assert c['screen_pass'],row
        errors.append(c['series_error'])
        if row['load_multiplier']==1.5:factor_cases.append(c)
    # Check recorded material minima against the entire saved diameter sweeps.
    # This checks consistency of saved optimisation outputs, not a new global search.
    for file,group in [('trade_study.csv','winners'),('transfer_trade_study.csv','transfer_winners')]:
        rows=list(csv.DictReader((data_dir/file).open()))
        for row in data[group]:
            best=min((r for r in rows if r['material']==row['material']),key=lambda x:float(x['shell_mass']))
            close(float(best['shell_mass']),row['shell_mass'],'CSV minimum')
    s=audited[0];overloaded=calculate(s['material'],s['D'],s['t'],1.5)
    summary=table(['Material','D mm','t mm','kg shell','Strength U','Euler U','Local U','Oval U'],[
        [c['material'],f"{c['D']:.0f}",f"{c['t']:.2f}",f"{c['mass']:.6f}"]+[f'{v:.6f}' for v in c['utilisations'].values()] for c in audited[:7]])
    text=f'''# Revision A calculation verification

**Verdict: the audited arithmetic reproduces the Revision A model. A complete structural pass is NOT verified.** The model has unresolved applicability issues, and the Revision A selected shell is a factor-{data['basis']['load_multiplier']} result, not a factor-1.5 design.

This audit independently uses N/mm/MPa rather than the production model's SI units. It does not import the production calculation functions. Section properties use factored diameter formulas; material failure uses 7,200 angular samples. A 1,000-term analytical sine-series solution of EI*y'' + P*y = -M0 independently checks the secant beam moment. No FEA is used. Largest relative moment difference across the 35 load-scenario checks: {max(errors):.3e}.

Scope: 14 stored baseline/transfer finalists checked against their detailed outputs; 35 load-scenario candidate masses and numerical passes rechecked; saved CSV minima compared with JSON. This is not a proof of an unrestricted global optimum or a fresh exhaustive search over every possible architecture.

## 1. Load derivation

```text
q = 0.5*1.225*200^2 = {Q:.6f} N/m^2
alpha = atan(20/200) = {ALPHA:.12f} rad
f = q*2*alpha*0.1 = {LINE_LOAD:.9f} N/m
V = f*3 = {V0:.9f} N
M = f*3^2/2 = {M0:.9f} N m
F = 30000 N
p = 0.3 MPa = 0.3 N/mm^2
Separate transfer scenario: M+V*1.5 = {M0+V0*1.5:.9f} N m
```

## 2. All-material factor-1.1 results

{summary}

U <= 1 means a pass of the implemented numerical screen only. All masses exclude rings and connections. QI candidates are equivalent-material screens, not established ply-level laminate designs.

## 3. Verification findings

- **Safety-factor distinction:** the saved baseline multiplier is 1.1, adopted by the team. The factor 1.5 is a sensitivity case only. Keeping D = {s["D"]:.0f} mm and t = {s["t"]:.2f} mm while multiplying all loads by 1.5 gives strength U = {overloaded['utilisations']['strength']:.6f}, local U = {overloaded['utilisations']['shell_interaction']:.6f}, oval U = {overloaded['utilisations']['ovalisation']:.6f}: numerical FAIL.
- **Elastic/plastic capacity issue:** the selected aluminium elastic bending-buckling prediction is {s['raw_b']:.6f} MPa, compared with the supplied {s['sy']:.0f} MPa yield. The code caps predicted capacities at yield when exceeded. That reproduces the code but is not the tangent/secant-modulus plasticity treatment described by NASA. Stress-strain/proportional-limit data or an appropriately justified alternative are needed. A cap cannot establish conservative inelastic capacity.
- **Long-shell applicability:** L/r = {1500/s['r']:.6f}. NASA warns about its axial correlation beyond L/r = 5 and calls for global/local interaction assessment. A separate Euler check plus secant amplification does not prove that coupled shell-column instability is covered.
- **Transverse-shear surrogate:** the imported shear capacity is for torsion. The sum of compression, bending and peak transverse-shear ratios is not demonstrated to be an exact or validated combined-load criterion for this barrel. The Air Force manual distinguishes transverse shear and torsion.
- **Pressure and ovalisation:** pressure enters strength. Buckling/ovalisation benefits are omitted; the ideal Brazier diagnostic does not solve the full pressurised finite-length response.
- **Composite failure:** a diagonal quadratic equation and QI tensile equivalence are declared choices. Uniaxial allowables alone do not verify the selected interaction coefficients or ply failure.
- **Output terminology:** JSON `validity: true` only tests the coded geometry/shear-formula ranges. It does not establish the long-shell, inelastic or composite applicability conditions above. `passes: true` is explicitly only a screen; competition compliance remains unresolved.
- **Missing assembly:** no ring/connection/manufacturing mass is established; 1.1 is the adopted team factor, not an instructor-specified value.

These findings prevent a claim that the Revision A establishes complete assembly compliance, despite numerical agreement. This audit verifies the archived Revision A numerical dataset. Revision C is specified in docs/METHOD.md.

## 4. Fully substituted factor-1.1 calculations

'''
    text+='\n'.join(worked(c) for c in audited[:7])
    text+='\n## 5. Fully substituted transfer-moment calculations\n\n'+'\n'.join(worked(c) for c in audited[7:])
    text+='\n## 6. Illustrative 1.5-times-load candidates - not an assigned course requirement\n\n'+'\n'.join(worked(c) for c in factor_cases)
    text+='\n## 7. Current selected shell tested at 1.5 times loads\n\n'+worked(overloaded)
    text+='''\n## 8. Sources and reproduction

- Assignment sections 3-7: input loads, material properties and required methods.
- [NASA SP-8007 Rev 2](https://ntrs.nasa.gov/citations/20205011530): equations 7, 9-16, 34-35 and 41; printed pp. 25-26 discuss long cylinders, plasticity and ovalisation. Their use does not automatically validate this model's extra approximations.
- [Air Force beam-column methods](https://engineeringlibrary.org/reference/beam-columns-air-force-stress-manual): compression/bending coupling and boundary-dependent solutions.
- [Air Force thin pressure vessels, Table 8-5](https://engineeringlibrary.org/reference/simple-thin-pressure-vessels-air-force-stress-manual): transverse shear is distinguished from torsion in combined-load checks. A web transcription is not sufficient to resolve every printed equation; no replacement interaction has been adopted in this audit.

```sh
python3 src/verify_calculations.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
'''
    doc_path = ROOT.parent / 'docs/history' / 'BASELINE_VERIFICATION.md'
    if doc_path.parent.exists(): doc_path.write_text(text)
    print('Arithmetic audit passed: 14 detailed finalists + 35 load-scenario cases; CSV minima agree.')
    print('Max independent Fourier moment relative error:',max(errors))

if __name__=='__main__':main()
