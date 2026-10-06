"""Independent N/mm/MPa verification of Revision C saved outputs.

No import of either design engine. Uses dense angular scanning rather than
analytic angular maximisation and a Fourier beam-column solution.
"""
from pathlib import Path
import json,math,csv,hashlib
ROOT=Path(__file__).resolve().parents[1]

def calculate(properties,D,t,case,quality='B',gust=20.,pressure_path='wall_only'):
    E=properties['E']/1e6;nu=properties['nu'];density=properties['density']
    sy=properties['yield_stress']/1e6;xc=properties['Xc']/1e6;yt=properties['Yt']/1e6;S=properties['S']/1e6
    L=1500.;di=D-2*t;r=(D+di)/4;A=math.pi*t*(D-t);I=A*(D*D+di*di)/16
    k=(.4 if sy else .5) if quality=='B' else (.5 if sy else .65)
    q=24500.;f=q*2*math.atan(gust/200)*.1;V=1.1*f*3;P=33000.;p=.33
    first=1.1*f*4.5*1000*(2 if case=='transfer' else 1)
    pcr=math.pi**2*E*I/L**2;lam=math.sqrt(P/(E*I));M=first/math.cos(lam*L/2)
    shear=(V+first*lam*math.tan(lam*L/2))/(math.pi*r*t)
    a=P/A;b=M*D/(2*I);h_lower=p*di/(2*t);h_upper=p*D/(2*t)
    relief=p*math.pi*(di/2)**2/A if pressure_path=='closed_end' else 0.
    dense_local=0.;dense_strength=0.
    for i in range(12001):
        theta=math.pi*i/12000;c=math.cos(theta);sn=math.sin(theta)
        effective=a-b*c+shear**2/h_lower*sn**2
        axial=-a+relief+b*c;tau=shear*sn
        strength=math.sqrt(axial*axial+h_upper*h_upper-axial*h_upper+3*tau*tau)/sy if sy else abs(axial)/(xc if axial<0 else yt)+h_upper/yt+abs(tau)/S
        dense_local=max(dense_local,effective);dense_strength=max(dense_strength,strength)
    cr=k*E*t/r/math.sqrt(3*(1-nu*nu));brazier=.987*E*r*t*t/math.sqrt(1-nu*nu)
    displacement=sum(4*first*(-1)**j/((2*j+1)*math.pi*(E*I*((2*j+1)*math.pi/L)**2-P)) for j in range(2000))
    return dict(mass=A*L*density/1e9,area=A,inertia=I,moment=M,
        local_shell=dense_local/cr,strength=dense_strength,Euler=P/pcr,ovalisation=M/brazier,
        fourier_relative_error=abs((first+P*displacement)/M-1))


def main():
    d=json.loads((ROOT/'data/guild_assay/response.json').read_text());props={m['name']:m for m in d['materials']}
    errors=[];fourier=[];count=0;minima=[]
    for case,c in d['cases'].items():
        for row in c['winners']+c['fine_winners']+[c['degraded_original']]:
            actual=calculate(props[row['material']],row['diameter_mm'],row['nominal_t_mm'],case)
            assert math.isclose(actual['mass'],row['shell_mass'],rel_tol=1e-10)
            for key in ['strength','Euler','local_shell','ovalisation']:
                error=abs(actual[key]-row['utilisations'][key]);errors.append(error)
                assert error < 2e-7,(case,row['material'],key,error)
            fourier.append(actual['fourier_relative_error']);count+=1
        with (ROOT/f'data/guild_assay/{case}_trade_study.csv').open() as f:rows=list(csv.DictReader(f))
        for row in c['winners']:
            assert min(float(x['shell_mass']) for x in rows if x['material']==row['material'])==row['shell_mass']
        gaps=[coarse['shell_mass']/fine['shell_mass']-1 for coarse,fine in zip(c['winners'],c['fine_winners'])]
        minima.append(dict(case=case,feasible_diameter_material_pairs=len(rows),max_nominal_grid_mass_excess=max(gaps)))
    out=dict(input_sha256=hashlib.sha256((ROOT/'data/guild_assay/response.json').read_bytes()).hexdigest(),independent_units='N, mm, MPa',verified_cases=count,angular_samples_per_case=12001,
        maximum_utilisation_absolute_difference=max(errors),maximum_fourier_relative_difference=max(fourier),
        checks_passed=True,sweep_checks=minima)
    (ROOT/'data/guild_assay/verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
