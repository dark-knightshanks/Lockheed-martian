"""Generate the technical solution from independently verified numerical results."""
from pathlib import Path
import json,re,textwrap,html,hashlib,tempfile,os
os.environ.setdefault("MPLCONFIGDIR",str(Path(tempfile.gettempdir())/"drakkar-matplotlib"))
from matplotlib import rc_context
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image
from matplotlib.path import Path as MathPath
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted,PageBreak,KeepTogether,Flowable
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports'

def md_table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])

class Equation(Flowable):
    """Draw a mathematical expression as vector outlines, with an equation number."""
    def __init__(self, expression, number):
        super().__init__()
        self.outline=TextPath((0,0),'$'+expression.replace(r'\frac',r'\dfrac')+'$',size=11.5,
                              prop=FontProperties(math_fontfamily='stix'))
        self.bounds=self.outline.get_extents()
        self.number=number
        self.spaceBefore=2
        self.spaceAfter=4
    def wrap(self, width, height):
        self.width=width
        self.scale=min(1,(width-38)/self.bounds.width)
        self.height=self.bounds.height*self.scale+4
        return self.width,self.height
    def draw(self):
        c=self.canv;c.saveState()
        c.setFillColor(colors.HexColor('#18242d'))
        c.translate(8-self.bounds.x0*self.scale,2-self.bounds.y0*self.scale)
        c.scale(self.scale,self.scale)
        path=c.beginPath();last=(0.,0.)
        for points,code in self.outline.iter_segments():
            if code==MathPath.MOVETO:path.moveTo(*points);last=tuple(points)
            elif code==MathPath.LINETO:path.lineTo(*points);last=tuple(points)
            elif code==MathPath.CURVE3:
                x,y,u,v=points
                path.curveTo(last[0]+2*(x-last[0])/3,last[1]+2*(y-last[1])/3,
                             u+2*(x-u)/3,v+2*(y-v)/3,u,v)
                last=(u,v)
            elif code==MathPath.CURVE4:path.curveTo(*points);last=tuple(points[-2:])
            elif code==MathPath.CLOSEPOLY:path.close()
        c.drawPath(path,fill=1,stroke=0);c.restoreState()
        c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#526575'))
        c.drawRightString(self.width,self.height/2-3,f'({self.number})')


def pdf(markdown,path,title):
    styles=getSampleStyleSheet()
    for name,size,leading in [('BodyText',9.0,11.5),('Heading1',19,23),('Heading2',11,14),('Heading3',10,13)]:
        styles[name].fontName='Helvetica-Bold' if 'Heading' in name else 'Helvetica'
        styles[name].keepWithNext=bool('Heading' in name)
        styles[name].fontSize=size;styles[name].leading=leading;styles[name].spaceAfter=5
        styles[name].textColor=colors.HexColor('#193b50') if 'Heading' in name else colors.HexColor('#18242d')
    styles['BodyText'].allowWidows=0
    styles['BodyText'].allowOrphans=0
    styles.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=8,leading=10))
    styles.add(ParagraphStyle(name='Eq',fontName='Courier',fontSize=7.6,leading=10,spaceAfter=6))
    flow=[];lines=markdown.splitlines();i=0;equation_number=0
    scratch=tempfile.TemporaryDirectory(prefix='drakkar-inline-')
    inline_cache={}
    def inline(s):
        expressions=[]
        def capture(match):
            expression=match.group(1)
            if expression not in inline_cache:
                path=Path(scratch.name)/f'{len(inline_cache)}.png'
                with rc_context({'savefig.transparent':True}):
                    math_to_image('$'+expression+'$',path,prop=FontProperties(size=9,math_fontfamily='stix'),dpi=240,format='png')
                with Image.open(path) as im:width,height=im.size
                inline_cache[expression]=f'<img src="{path}" width="{width*72/240:.3f}" height="{height*72/240:.3f}" valign="-3"/>'
            expressions.append(inline_cache[expression])
            return f'MATHPLACEHOLDER{len(expressions)-1}TOKEN'
        s=re.sub(r'\$([^$]+)\$',capture,s)
        s=html.escape(s)
        s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
        s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
        s=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',s)
        s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1',s)
        for n,expression in enumerate(expressions):s=s.replace(f'MATHPLACEHOLDER{n}TOKEN',expression)
        return s
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line=='<!-- PAGE -->':flow.append(PageBreak());i+=1;continue
        if line=='$$':
            equations=[]
            while i<len(lines) and lines[i]=='$$':
                formula=[];i+=1
                while lines[i]!='$$':formula.append(lines[i]);i+=1
                equation_number+=1
                equations.append(Equation(' '.join(formula),equation_number));i+=1
                while i<len(lines) and not lines[i].strip():i+=1
            flow.append(KeepTogether(equations));continue
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
            if len(rows[0])==8:weights=[1.85,.75,.6,1.15,1.4,.8,.8,.45]
            widths=[width*w/sum(weights) for w in weights]
            tab=Table([[Paragraph(inline(c),styles['Cell']) for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
            tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eef3')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#cbd7df'))]))
            flow.extend([KeepTogether([tab]) if len(rows)<=8 else tab,Spacer(1,7)]);continue
        if line.startswith('## 4. '):flow.append(PageBreak())
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));flow.append(Paragraph(inline(line[level:].strip()),styles['Heading'+str(min(level,3))]));i+=1;continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','<!--','- ','$$')) and not re.match(r'^\d+\.',lines[i]):
            paragraph.append(lines[i]);i+=1
        body=Paragraph(inline(' '.join(paragraph)),styles['BodyText'])
        next_content=next((line for line in lines[i:] if line.strip()),'')
        body.keepWithNext=next_content=='$$'
        flow.append(body)
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526575'))
        canvas.drawString(44,23,'DRAKKAR | Structural solution')
        canvas.drawRightString(A4[0]-44,23,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=33,bottomMargin=60,title=title,author='Lockheed Martian, VJTI')
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)
    scratch.cleanup()


def main():
    d=json.loads((ROOT/'data/solution.json').read_text())
    v=json.loads((ROOT/'data/verification.json').read_text())
    assert v['checks_passed']
    assert v['input_sha256']==hashlib.sha256((ROOT/'data/solution.json').read_bytes()).hexdigest(), 'Run verify.py after solve.py'
    selected=d['selected'];t=d['thresholds'];cases=d['load_cases']
    table=md_table(['Material',r'$E$ / GPa',r'$\nu$',r'$\rho$ / kg m$^{-3}$',r'$\sigma_y$ / $X_c$ / MPa',r'$Y_t$ / MPa',r'$S$ / MPa',r'$k$'],[
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
    method,references=(ROOT/'docs/METHOD.md').read_text().split('## 9. Sources and equation provenance',1)
    report+=method.replace('# Analytical Method Specification','# Governing Equations and Applicability',1)
    report+='\n<!-- PAGE -->\n# Numerical Evaluation and Verification\n\n'
    report+='## Selected geometry under both load cases\n\n'
    quantities=[
        ('Outer diameter',r'$D$','mm',lambda r:r['diameter_mm']),
        ('Wall thickness',r'$t$','mm',lambda r:r['nominal_t_mm']),
        ('Area',r'$A$',r'$\mathrm{mm}^2$',lambda r:r['section']['A']*1e6),
        ('Second moment of area',r'$I$',r'$\mathrm{mm}^4$',lambda r:r['section']['I']*1e12),
        ('Axial force',r'$P$','N',lambda r:r['applied']['P']),
        ('Internal pressure',r'$p$','MPa',lambda r:r['applied']['p']/1e6),
        ('First-order moment',r'$M_0$',r'$\mathrm{N\,m}$',lambda r:r['applied']['first_order_M']),
        ('Amplified moment',r'$M_{\max}$',r'$\mathrm{N\,m}$',lambda r:r['applied']['M']),
        ('External shear',r'$V$','N',lambda r:r['applied']['V']),
        ('Secondary shear',r'$V_{\mathrm{secondary}}$','N',lambda r:r['applied']['secondary_shear']),
        ('Euler load',r'$P_E$','N',lambda r:r['pcr']),
        ('Axial stress',r'$P/A$','MPa',lambda r:r['compression_terms']['axial']/1e6),
        ('Bending stress',r'$M_{\max}r_o/I$','MPa',lambda r:r['compression_terms']['bending']/1e6),
        ('Peak shear stress',r'$s_0$','MPa',lambda r:r['compression_terms']['peak_shear']/1e6),
        ('Hoop tension lower bound',r'$h$','MPa',lambda r:r['compression_terms']['hoop_lower']/1e6),
        ('Effective compression',r'$C_{\mathrm{eff}}$','MPa',lambda r:r['effective_compression']/1e6),
        ('Critical stress',r'$\sigma_{\mathrm{cr}}$','MPa',lambda r:r['critical_axial_stress']/1e6),
        ('Normal allowable',r'$\sigma_{\mathrm{allow}}$','MPa',lambda r:r['normal_allowable']/1e6),
        ('Critical angle',r'$\theta_{\mathrm{crit}}$',r'$^{\circ}$',lambda r:r['critical_angle_deg']),
        ('Brazier moment',r'$M_{\mathrm{Brazier}}$',r'$\mathrm{N\,m}$',lambda r:r['brazier_moment']),
    ]
    report+=md_table(['Quantity','Symbol','Unit','Primary','Transfer'],[
        [name,symbol,unit,f"{value(cases['primary']):.6f}",f"{value(cases['transfer']):.6f}"]
        for name,symbol,unit,value in quantities])+'\n\n'
    report+='## Search convergence\n\n'
    report+=f'''The transfer-load search contains {v['feasible_diameter_material_pairs']} feasible material/diameter pairs. A refined grid of 0.1 mm diameter and 0.001 mm wall checks numerical resolution. The largest nominal-grid mass excess over the refined material minimum is {100*v['maximum_nominal_grid_mass_excess']:.6f}%. The selected dimensions remain those of the declared nominal grid. The search record in `data/trade_study.csv` and the refinement data in `data/solution.json` support this single design selection; they are not additional design submissions.

## Gust and thickness sensitivity

'''
    report+=md_table(['Load case','Gust m/s','Local U','Strength U','Pass'],[
        [r['case'],f"{r['gust_m_s']:g}",f"{r['result']['utilisations']['local_shell']:.6f}",f"{r['result']['utilisations']['strength']:.6f}",'PASS' if r['result']['passes'] else 'FAIL'] for r in d['sensitivities']])+'\n\n'
    report+=f'''<!-- PAGE -->

At fixed selected geometry the calculated transfer-case gust boundary is {t['maximum_gust_m_s']:.6f} m/s. At the specified 20 m/s gust, the minimum actual wall is {t['minimum_actual_wall_mm']:.6f} mm; the difference from nominal wall is {t['maximum_wall_loss_mm']:.6f} mm. These are model acceptance boundaries, not prescribed production tolerances. Only the aerodynamic loading changes with gust; thrust and internal pressure remain fixed.

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
    references=references.strip().replace('4. The pressure-supported','\nDerivation note: The pressure-supported')
    report+='\n## References\n\n'+references+'\n'
    report=report.replace('moment M + V L','moment $M+VL$')
    report=report.replace('U is demand/capacity and MS = 1/U - 1.',r'$U$ is demand/capacity and $\mathrm{MS}=1/U-1$.')
    OUT.mkdir(exist_ok=True)
    (OUT/'Solution.md').write_text(report)
    pdf(report,OUT/'Solution.pdf','Drakkar Thrust Barrel: Structural Solution')
    print('Generated reports/Solution.pdf and its Markdown source')
if __name__=='__main__':main()
