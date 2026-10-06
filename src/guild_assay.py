"""Generate the revised material-quality analysis and convergence studies."""
from pathlib import Path
from dataclasses import asdict
import json,csv
import revised_analysis as model

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/guild_assay'
B_MATERIALS=model.B_MATERIALS


def material(name,quality='B'):
    return next(m for m in (B_MATERIALS if quality=='B' else model.MATERIALS) if m.name==name)


def check(row,case,quality='B',gust=20.,pressure_path='wall_only'):
    return model.evaluate(material(row['material'],quality),row['diameter_mm'],row['nominal_t_mm'],case,quality,gust,pressure_path)


def score(old_pass,penalty):
    if old_pass:return 1.
    return .7 if penalty <= .1 else .4 if penalty <= .25 else 0.


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    original=json.loads((ROOT/'data/original/design.json').read_text())
    cases={}
    for name,original_key in [('primary','selected'),('transfer','transfer_selected')]:
        winners,rows=model.optimise(B_MATERIALS,name)
        fine,_=model.optimise(B_MATERIALS,name,diameter_step=.1,wall_step=.001)
        clean,_=model.optimise(model.MATERIALS,name,quality='A')
        selected=min(winners,key=lambda r:r['shell_mass'])
        metal=min((r for r in winners if not material(r['material']).composite),key=lambda r:r['shell_mass'])
        old=original[original_key]
        rechecked=check(old,name)
        clean_old=check(old,name,quality='A')
        penalty=selected['shell_mass']/old['shell_mass']-1
        cases[name]=dict(original=old,clean_original=clean_old,degraded_original=rechecked,
            selected=selected,metal_alternative=metal,winners=winners,fine_winners=fine,clean_winners=clean,
            fixed_diameter_aluminium=model.minimum_wall(B_MATERIALS[0],old['diameter_mm'],name),
            mass_penalty_kg=selected['shell_mass']-old['shell_mass'],mass_penalty_fraction=penalty,
            material_integrity_score=score(rechecked['passes'],penalty),
            unchanged_failure_mode=rechecked['governing']==clean_old['governing'])
        keys=['material','diameter_mm','nominal_t_mm','shell_mass','governing','utilisation','passes']
        with (OUT/f'{name}_trade_study.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');writer.writeheader()
            writer.writerows({key:row[key] for key in keys} for row in rows)
        print(name,[(r['material'],r['diameter_mm'],r['nominal_t_mm'],round(r['shell_mass'],6)) for r in winners],flush=True)
    sensitivities=[]
    for case,c in cases.items():
        for geometry,row in [('original',c['original']),('selected',c['selected']),('metal',c['metal_alternative'])]:
            for quality in ['A','B']:
                for gust in [20.,22.,24.]:
                    r=check(row,case,quality,gust)
                    sensitivities.append(dict(case=case,geometry=geometry,quality=quality,gust_velocity=gust,
                        utilisations=r['utilisations'],margins=r['margins'],passes=r['passes'],governing=r['governing'],
                        status=('OUTSIDE DOMAIN' if not all(r['applicability'].values()) else 'PASS' if r['passes'] else 'FAIL')))
    pressure=[]
    for case,c in cases.items():
        for row in [c['selected'],c['metal_alternative']]:
            pressure.append(dict(case=case,material=row['material'],closed_end=check(row,case,pressure_path='closed_end')))
    # Operating thresholds at fixed geometry, not assumed manufacturing allowances.
    thresholds=[]
    for case,c in cases.items():
        for label,row in [('selected',c['selected']),('metal',c['metal_alternative'])]:
            lo,hi=20.,100.
            for _ in range(60):
                mid=(lo+hi)/2
                if check(row,case,gust=mid)['passes']:lo=mid
                else:hi=mid
            low_t,high_t=.1*row['nominal_t_mm'],row['nominal_t_mm']
            for _ in range(60):
                mid=(low_t+high_t)/2
                trial=dict(row,nominal_t_mm=mid)
                if check(trial,case)['passes']:high_t=mid
                else:low_t=mid
            thresholds.append(dict(case=case,design=label,maximum_gust_m_s=lo,
                minimum_actual_wall_mm=high_t,maximum_wall_loss_mm=row['nominal_t_mm']-high_t))
    cross_check=check(cases['transfer']['selected'],'primary')
    result=dict(revision='C',model='pressure-supported local geometric-energy bound',
        design_basis=dict(length_m=1.5,maximum_OD_mm=300,load_factor=1.1,diameter_grid_mm=1,wall_grid_mm=.01,
            refinement_diameter_mm=.1,refinement_wall_mm=.001,pressure_path='wall_only'),
        materials=[dict(**asdict(m),knockdown=model.knockdown(m)) for m in B_MATERIALS],
        cases=cases,sensitivities=sensitivities,closed_end_checks=pressure,thresholds=thresholds,
        transfer_design_under_primary=cross_check,
        scope='Homogeneous metal or supplied effective-QI cylindrical shell, ideal simply supported rigid end rings; no FEA.',
        excluded_inputs=['End-ring and connection design and mass','Product-form stress-strain and thickness-tolerance data','Ply-level laminate architecture'],
        applicability='Analytical design acceptance is confined to the stated homogeneous-shell and ideal-interface model. Empirical validation of a manufactured assembly is not claimed.')
    (OUT/'response.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':main()
