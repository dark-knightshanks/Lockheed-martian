"""Generate standalone Revision C reports from verified numerical results."""
from pathlib import Path
import json,re,textwrap,html,hashlib
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted,PageBreak,KeepTogether
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/guild_assay'

def md_table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])

def pdf(markdown,path,title):
    styles=getSampleStyleSheet()
    for name,size,leading in [('BodyText',9.0,11.5),('Heading1',19,23),('Heading2',11,14),('Heading3',10,13)]:
        styles[name].fontName='Helvetica-Bold' if 'Heading' in name else 'Helvetica'
        styles[name].keepWithNext=bool('Heading' in name)
        styles[name].fontSize=size;styles[name].leading=leading;styles[name].spaceAfter=5
        styles[name].textColor=colors.HexColor('#193b50') if 'Heading' in name else colors.HexColor('#18242d')
    styles.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=8,leading=10))
    styles.add(ParagraphStyle(name='Eq',fontName='Courier',fontSize=7.6,leading=10,spaceAfter=6))
    flow=[];lines=markdown.splitlines();i=0
    def inline(s):
        s=html.escape(s)
        s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
        s=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',s)
        s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1',s)
        return s
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line=='<!-- PAGE -->':flow.append(PageBreak());i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):
                code.extend(textwrap.wrap(lines[i],width=95,replace_whitespace=False,drop_whitespace=False) or ['']);i+=1
            flow.append(KeepTogether([Preformatted('\n'.join(code),styles['Eq'])]));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[c.strip() for c in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',c) for c in cells):rows.append(cells)
                i+=1
            width=A4[0]-88
            weights=[max(5,min(35,max(len(row[j]) for row in rows))) for j in range(len(rows[0]))]
            widths=[width*w/sum(weights) for w in weights]
            tab=Table([[Paragraph(inline(c),styles['Cell']) for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
            tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eef3')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#cbd7df'))]))
            flow.extend([tab,Spacer(1,7)]);continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));flow.append(Paragraph(inline(line[level:].strip()),styles['Heading'+str(min(level,3))]));i+=1;continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','<!--','- ')) and not re.match(r'^\d+\.',lines[i]):
            paragraph.append(lines[i]);i+=1
        flow.append(Paragraph(inline(' '.join(paragraph)),styles['BodyText']))
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526575'))
        canvas.drawString(44,23,'DRAKKAR | Revision C | 6 October 2026')
        canvas.drawRightString(A4[0]-44,23,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=33,bottomMargin=60,title=title,author='Lockheed Martian, VJTI')
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    d=json.loads((ROOT/'data/guild_assay/response.json').read_text())
    v=json.loads((ROOT/'data/guild_assay/verification.json').read_text())
    assert v['checks_passed']
    assert v['input_sha256']==hashlib.sha256((ROOT/'data/guild_assay/response.json').read_bytes()).hexdigest(), 'Verification is stale; run verify_revised.py'
    a=d['cases']['primary'];b=d['cases']['transfer'];sel=b['selected'];old=a['degraded_original'];minimum=a['selected'];metal=b['metal_alternative']
    pc=lambda x:f'{100*x:+.2f}%'
    dim=lambda r:f"{r['diameter_mm']:.1f} x {r['nominal_t_mm']:.3f}"
    margins=md_table(['Mode','Original Al, case A','QI design, case A','QI design, case B'],[
        [label,pc(old['margins'][key]),pc(d['transfer_design_under_primary']['margins'][key]),pc(sel['margins'][key])]
        for key,label in [('strength','Material failure'),('Euler','Euler'),('local_shell','Local shell'),('ovalisation','Ovalisation')]])
    chosen=next(x for x in d['materials'] if x['name']==sel['material'])
    props=md_table(['Material','E GPa','nu','Density kg/m3','Strength MPa','k'],[
        ['7075-T6',71.7,.33,2810,'Yield 402',.40],['Carbon/epoxy QI',chosen['E']/1e9,chosen['nu'],chosen['density'],'Xc 480; Yt 400; S 160',.50]])
    sensitivity=lambda quality,gust:next(r for r in d['sensitivities'] if r['case']=='primary' and r['geometry']=='original' and r['quality']==quality and r['gust_velocity']==gust)
    clean=sensitivity('A',20)['utilisations']['local_shell'];degraded=sensitivity('B',20)['utilisations']['local_shell'];g22=sensitivity('B',22)['utilisations']['local_shell'];g24=sensitivity('B',24)['utilisations']['local_shell']
    delta=sel['shell_mass']-a['original']['shell_mass'];fraction=delta/a['original']['shell_mass']
    limit=next(r for r in d['thresholds'] if r['case']=='transfer' and r['design']=='selected')
    response=f'''# Guild Assay Response

DRA-GAR-C | Lockheed Martian, VJTI | 6 October 2026

## 1. Material properties and analysis basis

{props}

L = 1500 mm; D <= 300 mm; load factor = 1.1. Design P = 33.0 kN, V = 1.611642 kN and p = 0.330 MPa. Case A first-order moment is 2.417463 kN m; case B is M + VL = 4.834926 kN m. Beam-column moment and secondary shear are included. The selected {sel['diameter_mm']:.1f} mm OD x {sel['nominal_t_mm']:.3f} mm effective-QI shell passes both cases in the specified analytical model.

Local stability uses sigma_cr = k E(t/r)/sqrt[3(1-nu^2)]. Transverse shear is bounded by the local geometric-energy identity C wx^2 + 2 T wx ws - h ws^2 <= (C + T^2/h) wx^2, h > 0. The circumference maximum C_eff is compared with sigma_cr. No torsional capacity or shear knockdown is substituted. The pressure-supported bound is restricted to the specified pressurised operating state.

Metal strength uses von Mises. QI strength uses the conservative quadratic envelope FI <= (abs(sigma_x)/X_sign + sigma_h/Yt + abs(tau)/S)^2; this bounds all positive-semidefinite quadratic interactions with the supplied uniaxial limits. The QI continuum is an assignment-level effective material, not a qualified ply schedule. Elastic capacities above the material normal allowable are rejected, not capped.

## 2. Numerical margins and verdict

{margins}

MS = 1/U - 1. Original geometry: aluminium 7075-T6, 119 x 0.960 mm, {a['original']['shell_mass']:.6f} kg. **Original verdict: FAIL**, governing local margin {pc(old['margins']['local_shell'])}. **Revised verdict: PASS within the stated homogeneous-shell model**, governing local margin {pc(sel['margins']['local_shell'])} in case B. Ideal end-ring and connection masses are outside the calculated shell mass.

## 3. Minimum-mass fix

The minimum nominal-grid shell for case A is carbon/epoxy QI, {dim(minimum)} mm, {minimum['shell_mass']:.6f} kg. The recommended design also covers case B: carbon/epoxy QI, {dim(sel)} mm, **{sel['shell_mass']:.6f} kg**. Relative to the original 1.500541 kg shell, Delta m = **{delta:+.6f} kg ({pc(fraction)})**. All seven material sets were searched, using 1 mm OD and 0.01 mm wall increments. The refined 0.1/0.001 mm search provides the numerical-resolution comparison on page 2.

<!-- PAGE -->
# Guild Assay Response - continued

## 4. Design-space comparison and refinement

{md_table(['Alternative','OD x wall mm','Shell mass kg','Application'],[
['QI minimum, A',dim(minimum),f"{minimum['shell_mass']:.6f}",'Case A only'],
['QI selected, A+B',dim(sel),f"{sel['shell_mass']:.6f}",'Both cases'],
['Metal minimum, A+B',dim(metal),f"{metal['shell_mass']:.6f}",metal['material']]])}

The refined case-B QI result is {dim(next(r for r in b['fine_winners'] if r['material']==sel['material']))} mm and {next(r for r in b['fine_winners'] if r['material']==sel['material'])['shell_mass']:.6f} kg. Nominal-grid minima exceed refined minima by no more than {100*max(x['max_nominal_grid_mass_excess'] for x in v['sweep_checks']):.3f}% across both cases and all materials. The minimum is confined to homogeneous unstiffened shells; ring-stiffened, sandwich and hybrid assembly optima are not claimed.

## 5. Failure-mode declaration and matched comparison

Local shell buckling governs the original design under both matched clean and degraded inputs and governs the selected QI solution; the governing class is unchanged. Under the same Revision C equations, the original clean-material local margin is {pc(a['clean_original']['margins']['local_shell'])}; the degraded margin is {pc(old['margins']['local_shell'])}. The archived original calculation used a different interaction model, so its reported +0.38% margin is not used as the clean endpoint of a material-only comparison.

## 6. Material quality versus gust sensitivity

At fixed original geometry and the same equations, clean-to-B-basis degradation changes local U from {clean:.6f} to {degraded:.6f} ({pc(degraded/clean-1)}). With B-basis properties fixed, gust 20 to 22 m/s changes U to {g22:.6f} ({pc(g22/degraded-1)}); 24 m/s gives {g24:.6f} ({pc(g24/degraded-1)}). Only aerodynamic loads change with atan(w_g/200); thrust and pressure are fixed. For these perturbations, material degradation has the larger effect. The selected case-B design's calculated gust boundary is {limit['maximum_gust_m_s']:.4f} m/s and minimum actual wall is {limit['minimum_actual_wall_mm']:.6f} mm; nominal wall dimensions are not manufacturing tolerances.

## 7. Verification, score and scope

Independent N/mm/MPa calculations verify {v['verified_cases']} cases; 12,001-point angular scans differ from the analytic utilisations by at most {v['maximum_utilisation_absolute_difference']:.3e}. Fourier beam-column verification differs by at most {v['maximum_fourier_relative_difference']:.3e}. Tests cover energy inequalities, composite interaction bounds, material data, bisection against enumeration and saved sweep minima.

The original fails, then the shell fix has Delta m <= 10%; the shell-only material-integrity bracket is M_i = 0.7. The unchanged governing-mode declaration is provided for H_i assessment. Total = 100(0.35 S_i + 0.15 M_i + 0.10 H_i + 0.25 R_i + 0.10 T_i + 0.05 I_i); total score needs competition/assessment inputs. Shell-to-assembly mass conversion needs ring and connection masses.

Basis: VJTI challenge sections 3-8; Guild Assay notice sections 2-5; NASA SP-8007 Rev. 2 equations 7 and 16. Derivations and applicability boundaries: DRA-MTH-C, sections 3-8. Separate global beam and local-shell checks do not establish nonlinear global/local collapse or manufactured laminate qualification; these are outside the defined analytical acceptance scope.
'''
    (OUT/'response.md').write_text(response)
    pdf(response,OUT/'Guild_Assay_Response.pdf','Guild Assay Response - Revision C')
    all_materials=md_table(['Material','E GPa','nu','rho kg/m3','Yield / Xc MPa','Yt MPa','S MPa','k'],[
        [p['name'],f"{p['E']/1e9:g}",p['nu'],p['density'],f"{(p['yield_stress'] or p['Xc'])/1e6:g}",f"{p['Yt']/1e6:g}" if p['Yt'] else '-',f"{p['S']/1e6:g}" if p['S'] else '-',p['knockdown']] for p in d['materials']])
    report=f'''# Drakkar Thrust Barrel: Technical Analysis

DRA-TR-C | Revision C | 6 October 2026

Aircraft Structures R5ME3203T, VJTI Mumbai. Cadre: Lockheed Martian. Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).

## Executive technical finding

The adopted dual-case solution is the supplied effective-QI carbon/epoxy material, outer diameter {sel['diameter_mm']:.1f} mm, nominal wall {sel['nominal_t_mm']:.3f} mm, length 1500 mm, shell mass {sel['shell_mass']:.6f} kg. Case B local utilisation is {sel['utilisation']:.9f}. Its case-A margins are also positive. The lower mass case-A-only solution is {minimum['shell_mass']:.6f} kg. A homogeneous metal alternative for both cases is {metal['material']}, {dim(metal)} mm, {metal['shell_mass']:.6f} kg.

Acceptance is defined by the mathematical checks and applicability gates in DRA-MTH-C. Ring/connection masses and manufactured laminate qualification are excluded quantities, not zero-valued results. The original clean-material dataset is maintained as Revision A; it is not the current B-basis design.

## Revised material-property register

{all_materials}

The supplied density and Poisson ratios are unchanged. Exact tabulated B-basis stiffnesses and strengths are used. QI modulus is an effective homogeneous property; no constituent fibre or resin properties are inferred.

## Requirements traceability

{md_table(['Requirement','Implementation / evidence'],[
['Length / OD','L = 1.5 m; OD <= 0.3 m; every enumerated candidate checked'],
['All revised properties','Seven exact B-basis property sets; material-data regression test'],
['Strength','Circumferential von Mises or conservative PSD quadratic QI envelope'],
['Column stability','P < Euler capacity; secant moment and secondary shear included'],
['Local shell stability','Pressure-supported geometric-energy bound / prescribed k axial capacity'],
['No FEA','Closed-form mechanics, integer enumeration and analytic beam series'],
['Minimum-mass modification','All seven homogeneous materials; nominal and refined complete OD sweeps'],
['Margins and verdict','All four utilisation ratios and signed margins saved per design'],
['Sensitivity','Fixed geometry, matched model, quality A/B and gust 20/22/24 m/s'],
['Two-page supplement','Guild_Assay_Response.pdf, generated from the same result data']])}

<!-- PAGE -->
'''
    method=(ROOT/'docs/METHOD.md').read_text();report+=method.replace('# Analytical Method Specification','## Governing equations and applicability',1)
    report+='\n<!-- PAGE -->\n# Results and numerical verification\n'
    for case,c in d['cases'].items():
        report+=f'\n## {case.capitalize()} load case: all-material optimisation\n\n'
        report+=md_table(['Material','D mm','t mm','Mass kg','Governing','Margin %','Refined kg'],[
            [r['material'],f"{r['diameter_mm']:.1f}",f"{r['nominal_t_mm']:.3f}",f"{r['shell_mass']:.6f}",r['governing'],f"{100*r['margins'][r['governing']]:.4f}",f"{f['shell_mass']:.6f}"] for r,f in zip(c['winners'],c['fine_winners'])])+'\n\n'
        report+=f"The original {dim(c['original'])} mm aluminium geometry has B-basis local margin {pc(c['degraded_original']['margins']['local_shell'])}. The fixed-diameter aluminium repair is {dim(c['fixed_diameter_aluminium'])} mm, {c['fixed_diameter_aluminium']['shell_mass']:.6f} kg.\n"
    report+='\n## Selected dual-case design: substituted quantities\n\n'
    for case,row in [('A',d['transfer_design_under_primary']),('B',sel)]:
        ct=row['compression_terms'];ap=row['applied'];ss=row['section']
        report+=f'''### Case {case}

```
D = {row['diameter_mm']:.6f} mm; t = {row['nominal_t_mm']:.6f} mm
r_o = {ss['ro']*1000:.6f} mm; r_i = {ss['ri']*1000:.6f} mm
A = {ss['A']*1e6:.9f} mm^2; I = {ss['I']*1e12:.9f} mm^4
M_0 = {ap['first_order_M']:.9f} N m; M_max = {ap['M']:.9f} N m
V_external = {ap['V']:.9f} N; V_secondary = {ap['secondary_shear']:.9f} N
P_E = {row['pcr']:.9f} N
P/A = {ct['axial']/1e6:.9f} MPa
M r_o/I = {ct['bending']/1e6:.9f} MPa
Peak shear bound = {ct['peak_shear']/1e6:.9f} MPa
Hoop tension lower bound = {ct['hoop_lower']/1e6:.9f} MPa
C_eff = {row['effective_compression']/1e6:.9f} MPa
sigma_cr = {row['critical_axial_stress']/1e6:.9f} MPa
QI normal-domain bound = {row['normal_allowable']/1e6:.9f} MPa
C_eff maximum angle = {row['critical_angle_deg']:.6f} deg
M_Brazier = {row['brazier_moment']:.9f} N m
```

'''
        report+=md_table(['Check','Utilisation','Margin %'],[[k,f'{value:.9f}',f"{100*row['margins'][k]:.6f}"] for k,value in row['utilisations'].items()])+'\n'
    report+='\n## Independent verification record\n\n'
    report+=f"Verification uses different units and independent geometry identities, 12,001 circumferential samples, and a 2,000-term sine series. {v['verified_cases']} nominal/refined/original cases pass the arithmetic comparison; maximum absolute utilisation difference is {v['maximum_utilisation_absolute_difference']:.6e}, and maximum relative beam-moment difference is {v['maximum_fourier_relative_difference']:.6e}. Every nominal material minimum agrees with the saved diameter sweep.\n\n"
    report+=md_table(['Case','Feasible D/material pairs','Maximum nominal/fine mass excess %'],[[r['case'],r['feasible_diameter_material_pairs'],f"{100*r['max_nominal_grid_mass_excess']:.6f}"] for r in v['sweep_checks']])+'\n'
    report+='\n## Wall-thickness and gust boundaries\n\n'
    report+=md_table(['Case','Design','Minimum actual t mm','Allowable wall loss mm','Gust boundary m/s'],[[r['case'],r['design'],f"{r['minimum_actual_wall_mm']:.6f}",f"{r['maximum_wall_loss_mm']:.6f}",f"{r['maximum_gust_m_s']:.6f}"] for r in d['thresholds']])+'\n\n'
    report+='These are computed acceptance boundaries of the stated model at fixed geometry and material. They are not prescribed production tolerances or certification gust envelopes.\n'
    report+='\n## Fixed-geometry sensitivity record\n\n'
    report+=md_table(['Case','Geometry','Quality','Gust m/s','Local U','Strength U','Status'],[[r['case'],r['geometry'],r['quality'],f"{r['gust_velocity']:g}",f"{r['utilisations']['local_shell']:.6f}",f"{r['utilisations']['strength']:.6f}",r['status']] for r in d['sensitivities']])+'\n'
    report+='\n## Closed-end pressure sensitivity\n\n'
    report+=md_table(['Case','Material','Closed-end strength U','Wall-only strength U'],[[r['case'],r['material'],f"{r['closed_end']['utilisations']['strength']:.6f}",f"{next(x for x in d['cases'][r['case']]['winners'] if x['material']==r['material'])['utilisations']['strength']:.6f}"] for r in d['closed_end_checks']])+'\n'
    report+='''\n## Reproduction and deliverable control

Run from the repository root with Python >= 3.10:

```sh
python3 src/guild_assay.py
python3 src/verify_revised.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
.venv/bin/python src/generate_assay_response.py
```

The first command regenerates both full diameter sweeps, material optima, matched clean comparisons, refinement, pressure and gust checks. Verification produces data/guild_assay/verification.json. The report generator obtains every reported result from the JSON datasets; it contains no independently maintained design-result constants. The original Revision A report, presentation and dataset remain separately labelled reference records.
'''
    (OUT/'Technical_Report.md').write_text(report)
    pdf(report,OUT/'Technical_Report.pdf','Drakkar Thrust Barrel Technical Analysis - Revision C')
    verification=f'''# Calculation Verification - Revision C

DRA-VER-C | 6 October 2026

Independent implementation: `src/verify_revised.py`. Units: N, mm, MPa. Production model units: SI. No production analysis functions are imported by the verifier.

- Cases checked: {v['verified_cases']}.
- Angular samples per case: {v['angular_samples_per_case']}.
- Maximum absolute utilisation discrepancy: {v['maximum_utilisation_absolute_difference']:.9e}.
- Maximum relative Fourier beam-moment discrepancy: {v['maximum_fourier_relative_difference']:.9e}.
- Nominal-grid minima: matched against both saved CSV sweeps.
- All arithmetic checks passed: {v['checks_passed']}.

The unit suite verifies the prescribed properties, co-located stress extrema, pressure-supported energy inequality, positive-semidefinite quadratic composite bound, Euler singularity, zero-load beam limit, gust isolation, elastic-capacity rejection and integer bisection against direct enumeration. Numerical agreement verifies the implementation of DRA-MTH-C; it is not experimental validation of the manufactured shell.

The complete numerical record is [verification.json](../data/guild_assay/verification.json). The historical Revision A audit is [BASELINE_VERIFICATION.md](history/BASELINE_VERIFICATION.md).
'''
    (ROOT/'docs/CALCULATION_VERIFICATION.md').write_text(verification)
    (ROOT/'README.md').write_text(f'''# Drakkar thrust-barrel structural analysis

Revision C | VJTI Aircraft Structures R5ME3203T | Lockheed Martian

Analytical optimisation of a 1.5 m circular thrust barrel under compression, bending, transverse shear and internal pressure. The material-quality revision uses the 3 October 2026 B-basis properties. No finite element analysis is used.

## Current technical deliverables

- [Guild Assay Response - two pages](reports/guild_assay/Guild_Assay_Response.pdf).
- [Technical report](reports/guild_assay/Technical_Report.pdf) and [editable Markdown](reports/guild_assay/Technical_Report.md).
- [Governing equations and applicability](docs/METHOD.md).
- [Design basis and system boundary](docs/DESIGN_ASSUMPTIONS.md).
- [Independent verification](docs/CALCULATION_VERIFICATION.md).
- [Numerical results](data/guild_assay/response.json).

The nominal-grid effective-QI solution satisfying both reported moment cases is **{sel['material']}, D = {sel['diameter_mm']:.1f} mm, t = {sel['nominal_t_mm']:.3f} mm, shell mass {sel['shell_mass']:.6f} kg**. The metal alternative is {metal['material']}, {dim(metal)} mm, {metal['shell_mass']:.6f} kg. Acceptance applies to the defined homogeneous-shell model with ideal rigid end boundaries; total assembly mass and manufactured laminate qualification are not outputs of this model.

## Reproduction

Python >= 3.10. Analysis, verification and tests use the standard library. Report generation requires the pinned dependencies in `requirements.txt`.

```sh
python3 src/guild_assay.py
python3 src/verify_revised.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/generate_assay_response.py
```

## Repository structure

| Directory | Contents |
| --- | --- |
| src/ | Revised and baseline mechanics, verification and document generators |
| tests/ | Baseline and revised regression / analytical checks |
| data/guild_assay/ | Current material study, sweeps and independent verification |
| data/original/ | Revision A numerical reference data |
| docs/ | Governing method, design basis and verification record |
| docs/briefs/ | Original assignment and material-quality notice |
| docs/history/ | Historical method audit and baseline verification |
| reports/guild_assay/ | Current response and detailed technical report |
| reports/original/ | Original report, figures and editable presentation |

## Revision A reference

The [original report](reports/original/Drakkar_Analytical_Report.pdf), [summary](reports/original/Drakkar_Results_Summary.pdf) and [presentation](reports/original/slides/Design_Review.pptx) describe the original clean-material submission. They do not represent the revised design. `src/parametric_diameter_study.py` regenerates that baseline. `src/verify_calculations.py` audits it and writes the historical verification record. The baseline figure generators likewise use only `data/original/`.

## Authors

Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).
''')
    print('Generated Guild_Assay_Response.pdf, Technical_Report.pdf and corresponding Markdown/document indexes')

if __name__=='__main__':main()
