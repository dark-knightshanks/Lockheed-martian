"""Generate one selected shell design and its supporting search/check records."""
from pathlib import Path
from dataclasses import asdict
import csv,json
import analysis as model
ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'data';out.mkdir(exist_ok=True)
    winners,rows=model.optimise(model.MATERIALS,'transfer')
    fine,_=model.optimise(model.MATERIALS,'transfer',diameter_step=.1,wall_step=.001)
    selected=min(winners,key=lambda r:r['shell_mass'])
    mat=next(m for m in model.MATERIALS if m.name==selected['material'])
    D,t=selected['diameter_mm'],selected['nominal_t_mm']
    checks={case:model.evaluate(mat,D,t,case) for case in ['primary','transfer']}
    assert all(r['passes'] for r in checks.values())
    sensitivities=[dict(case=case,gust_m_s=gust,result=model.evaluate(mat,D,t,case,gust=gust))
                   for case in checks for gust in [20.,22.,24.]]
    lo,hi=20.,100.
    for _ in range(60):
        mid=(lo+hi)/2
        if model.evaluate(mat,D,t,'transfer',gust=mid)['passes']:lo=mid
        else:hi=mid
    low_t,high_t=.1*t,t
    for _ in range(60):
        mid=(low_t+high_t)/2
        if model.evaluate(mat,D,mid,'transfer')['passes']:high_t=mid
        else:low_t=mid
    result=dict(materials=[dict(**asdict(m),knockdown=model.knockdown(m)) for m in model.MATERIALS],
        selected=selected,load_cases=checks,
        search=dict(material_minima=winners,refined_minima=fine,diameter_step_mm=1,wall_step_mm=.01,
                    refined_diameter_step_mm=.1,refined_wall_step_mm=.001),
        sensitivities=sensitivities,
        thresholds=dict(maximum_gust_m_s=lo,minimum_actual_wall_mm=high_t,maximum_wall_loss_mm=t-high_t),
        closed_end_strength={case:model.evaluate(mat,D,t,case,pressure_path='closed_end')['strength_state'] for case in checks},
        scope='Homogeneous shell with ideal rigid simply supported end rings; effective-QI scalar properties; no FEA.',
        excluded_inputs=['Ring and connection geometry and mass','Manufacturing tolerances and material stress-strain curves','Ply-level laminate architecture'])
    (out/'solution.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    keys=['material','diameter_mm','nominal_t_mm','shell_mass','governing','utilisation','passes']
    with (out/'trade_study.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');writer.writeheader()
        writer.writerows({key:r[key] for key in keys} for r in rows)
    print(f"Selected {mat.name}: {D:.1f} mm OD x {t:.3f} mm wall, {selected['shell_mass']:.9f} kg")
if __name__=='__main__':main()
