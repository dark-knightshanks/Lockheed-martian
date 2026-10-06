"""Generate the technical solution from independently verified numerical results."""
from pathlib import Path
import json,re,textwrap,html,hashlib
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted,PageBreak,KeepTogether
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports'

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
            flow.extend([KeepTogether([tab]) if len(rows)<=8 else tab,Spacer(1,7)]);continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));flow.append(Paragraph(inline(line[level:].strip()),styles['Heading'+str(min(level,3))]));i+=1;continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','<!--','- ')) and not re.match(r'^\d+\.',lines[i]):
            paragraph.append(lines[i]);i+=1
        flow.append(Paragraph(inline(' '.join(paragraph)),styles['BodyText']))
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526575'))
        canvas.drawString(44,23,'DRAKKAR | Structural solution')
        canvas.drawRightString(A4[0]-44,23,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=33,bottomMargin=60,title=title,author='Lockheed Martian, VJTI')
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)


def main():
    d=json.loads((ROOT/'data/solution.json').read_text())
    v=json.loads((ROOT/'data/verification.json').read_text())
    assert v['checks_passed']
    assert v['input_sha256']==hashlib.sha256((ROOT/'data/solution.json').read_bytes()).hexdigest(), 'Run verify.py after solve.py'
    selected=d['selected'];t=d['thresholds'];cases=d['load_cases']
    table=md_table(['Material','E GPa','nu','Density kg/m3','Yield / Xc MPa','Yt MPa','S MPa','k'],[
        [m['name'],f"{m['E']/1e9:g}",m['nu'],m['density'],f"{(m['yield_stress'] or m['Xc'])/1e6:g}",f"{m['Yt']/1e6:g}" if m['Yt'] else '-',f"{m['S']/1e6:g}" if m['S'] else '-',m['knockdown']] for m in d['materials']])
    margins=md_table(['Check','Primary U','Primary MS %','Transfer U','Transfer MS %'],[
        [key,f"{cases['primary']['utilisations'][key]:.9f}",f"{100*cases['primary']['margins'][key]:+.4f}",f"{cases['transfer']['utilisations'][key]:.9f}",f"{100*cases['transfer']['margins'][key]:+.4f}"] for key in ['strength','Euler','local_shell','ovalisation']])
    report=f'''# Drakkar Thrust Barrel: Structural Solution

Aircraft Structures R5ME3203T, VJTI Mumbai. Lockheed Martian.
Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).

## Selected design

Material: **{selected['material']}**. Length: **1500 mm**. Outer diameter: **{selected['diameter_mm']:.1f} mm**. Uniform wall: **{selected['nominal_t_mm']:.3f} mm**. Shell mass: **{selected['shell_mass']:.9f} kg**.

The same geometry passes the prescribed primary moment and the transfer moment M + V L under the supplied B-basis material properties. The governing check is local shell stability under the transfer load case. Selection minimises shell mass over the seven permitted homogeneous material families on a 1 mm diameter / 0.01 mm wall grid.

## Material data

{table}

Values follow the material-quality notice. Yield applies to metals; Xc, Yt and S apply to the effective-QI composites. Density and Poisson ratio follow the assignment. QI properties describe a homogeneous effective continuum; they do not specify a laminate stacking sequence.

## Acceptance results

{margins}

U is demand/capacity and MS = 1/U - 1. All four U values are at most one, and the thin-shell and elastic-capacity gates pass. The proportional design load factor is 1.1. Numerical margins refer to that design load, not an additional nonlinear load multiplier.

The result covers the uniform shell with ideal simply supported rigid end rings. Ring and connection mass, manufactured laminate qualification, joint stiffness and nonlinear coupled global/local collapse are outside the supplied model. These are system-boundary exclusions, not zero-valued physical quantities.

<!-- PAGE -->
'''
    report+=(ROOT/'docs/METHOD.md').read_text().replace('# Analytical Method Specification','# Governing Equations and Applicability',1)
    report+='\n<!-- PAGE -->\n# Numerical Evaluation and Verification\n\n'
    report+='## Selected geometry under both load cases\n\n'
    for case,row in cases.items():
        s=row['section'];a=row['applied'];c=row['compression_terms']
        report+=f'''### {case.capitalize()} load case

```
D = {row['diameter_mm']:.6f} mm; t = {row['nominal_t_mm']:.6f} mm
A = {s['A']*1e6:.9f} mm^2; I = {s['I']*1e12:.9f} mm^4
P = {a['P']:.6f} N; p = {a['p']/1e6:.6f} MPa
M_first = {a['first_order_M']:.9f} N m; M_max = {a['M']:.9f} N m
V_external = {a['V']:.9f} N; V_secondary = {a['secondary_shear']:.9f} N
P_Euler = {row['pcr']:.9f} N
P/A = {c['axial']/1e6:.9f} MPa; M r_o/I = {c['bending']/1e6:.9f} MPa
Peak shear = {c['peak_shear']/1e6:.9f} MPa
Hoop tension lower bound = {c['hoop_lower']/1e6:.9f} MPa
C_eff = {row['effective_compression']/1e6:.9f} MPa
sigma_cr = {row['critical_axial_stress']/1e6:.9f} MPa
Normal allowable = {row['normal_allowable']/1e6:.9f} MPa
C_eff maximum angle = {row['critical_angle_deg']:.6f} deg
M_Brazier = {row['brazier_moment']:.9f} N m
```

'''
    report+='## Search convergence\n\n'
    report+=f'''The transfer-load search contains {v['feasible_diameter_material_pairs']} feasible material/diameter pairs. A refined grid of 0.1 mm diameter and 0.001 mm wall checks numerical resolution. The largest nominal-grid mass excess over the refined material minimum is {100*v['maximum_nominal_grid_mass_excess']:.6f}%. The selected dimensions remain those of the declared nominal grid. The search record in `data/trade_study.csv` and the refinement data in `data/solution.json` support this single design selection; they are not additional design submissions.

## Gust and thickness sensitivity

'''
    report+=md_table(['Load case','Gust m/s','Local U','Strength U','Pass'],[
        [r['case'],f"{r['gust_m_s']:g}",f"{r['result']['utilisations']['local_shell']:.6f}",f"{r['result']['utilisations']['strength']:.6f}",'PASS' if r['result']['passes'] else 'FAIL'] for r in d['sensitivities']])+'\n\n'
    report+=f'''At fixed selected geometry the calculated transfer-case gust boundary is {t['maximum_gust_m_s']:.6f} m/s. At the specified 20 m/s gust, the minimum actual wall is {t['minimum_actual_wall_mm']:.6f} mm; the difference from nominal wall is {t['maximum_wall_loss_mm']:.6f} mm. These are model acceptance boundaries, not prescribed production tolerances. Only the aerodynamic loading changes with gust; thrust and internal pressure remain fixed.

Closed-end thrust is checked as a strength sensitivity using the same geometry. Primary and transfer strength utilisations are {d['closed_end_strength']['primary']['utilisation']:.9f} and {d['closed_end_strength']['transfer']['utilisation']:.9f}, respectively. The main stability calculation does not credit axial pressure-thrust relief.

## Independent numerical verification

An independent implementation in N, mm and MPa verifies {v['verified_cases']} calculation records, including material-search minima, refinement results, both selected-geometry load cases and gust scenarios. It imports no analysis functions. A {v['angular_samples_per_case']}-point circumferential scan checks the analytical stress maxima; a 2000-term Fourier series checks the beam-column moment. Maximum absolute utilisation discrepancy is {v['maximum_utilisation_absolute_difference']:.9e}; maximum relative Fourier moment discrepancy is {v['maximum_fourier_relative_difference']:.9e}. Saved nominal material minima also match the full CSV sweep.

The unit suite checks energy and composite-interaction inequalities, analytical extrema, beam response, material properties, gust isolation, elastic-domain rejection, bisection against direct enumeration and saved-design consistency. Agreement verifies the stated equations and implementation; it does not constitute experimental validation.

## Reproduction

Python >= 3.10. The calculation and verification require only the standard library. Report generation requires the dependency in `requirements.txt`.

```sh
python3 src/solve.py
python3 src/verify.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
.venv/bin/python src/report.py
```

The report is generated from the numerical dataset. A SHA-256 check prevents report generation from using a verification record for different solution data.
'''
    OUT.mkdir(exist_ok=True)
    (OUT/'Solution.md').write_text(report)
    pdf(report,OUT/'Solution.pdf','Drakkar Thrust Barrel: Structural Solution')
    print('Generated reports/Solution.pdf and its Markdown source')
if __name__=='__main__':main()
