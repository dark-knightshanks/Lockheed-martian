"""Export the current checked results as printable PDFs and a shareable ZIP."""
from pathlib import Path
import hashlib
import html
import json
import re
import textwrap
import zipfile
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Preformatted, KeepTogether, PageBreak

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
PDF = OUT / 'pdf'
WIDTH = A4[0] - 80
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Body', fontName='Helvetica', fontSize=9, leading=13, spaceAfter=7))
styles.add(ParagraphStyle('Cell', fontName='Helvetica', fontSize=7.5, leading=10))
styles.add(ParagraphStyle('CodeBlock', fontName='Courier', fontSize=7, leading=10, backColor=colors.HexColor('#f1f5f8'), borderPadding=6, spaceAfter=10))
for name in ['Title', 'Heading1', 'Heading2', 'Heading3']:
    styles[name].textColor = colors.HexColor('#174d65')
    styles[name].spaceBefore = 12
    styles[name].keepWithNext = True
styles['Title'].alignment = TA_LEFT
styles['Title'].fontSize = 23
styles['Title'].leading = 28

def inline(s):
    s = s.replace('—','-').replace('–','-').replace('≤','<=').replace('≥','>=').replace('×','x')
    s = html.escape(s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#176b91">\1</link>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', s)
    return s

def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#c9d5dd'))
    canvas.line(40, 33, A4[0]-40, 33)
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#526270'))
    canvas.drawString(40, 22, 'DRAKKAR ASCENT | Analytical study - conditional design basis')
    canvas.drawRightString(A4[0]-40, 22, str(doc.page))

def export_pdf(source, target):
    lines = source.splitlines(); story = []; i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if line.startswith('```'):
            block=[]; i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                block.extend(textwrap.wrap(lines[i], 100, replace_whitespace=False, drop_whitespace=False) or [''])
                i += 1
            story.append(Preformatted('\n'.join(block), styles['CodeBlock']))
        elif line.startswith('|'):
            rows=[]
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'[\s:\-]+', c) for c in cells):
                    rows.append([Paragraph(inline(c.strip()), styles['Cell']) for c in cells])
                i += 1
            table=Table(rows, colWidths=[WIDTH/len(rows[0])]*len(rows[0]), repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce9ef')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f8')]),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),
                ('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
                ('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#8fa7b5'))]))
            story.extend([KeepTogether([table]) if len(rows)<=6 else table,Spacer(1,10)]); continue
        elif line.startswith('!['):
            path = ROOT / re.search(r'\]\(([^)]+)\)', line).group(1)
            im=Image(str(path)); scale=min(WIDTH/im.imageWidth,470/im.imageHeight)
            im.drawWidth=im.imageWidth*scale; im.drawHeight=im.imageHeight*scale
            story.extend([im,Spacer(1,10)])
        elif line.startswith('#'):
            if line in ['## 7. Concept and mass boundary', '### Baseline metal shell checks']:
                story.append(PageBreak())
            n=len(line)-len(line.lstrip('#'))
            style='Title' if n==1 else 'Heading'+str(min(n-1,3))
            story.append(Paragraph(inline(line[n:].strip()),styles[style]))
        else:
            if line.startswith('- '):
                story.append(Paragraph(inline(line[2:]), styles['Body'], bulletText='-'))
            else:
                p=[line]
                while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].startswith(('#','|','```','![','- ')):
                    i+=1; p.append(lines[i].strip())
                story.append(Paragraph(inline(' '.join(p)),styles['Body']))
        i += 1
    SimpleDocTemplate(str(target),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=35,bottomMargin=46,
                      title=target.stem.replace('_',' '),author='Drakkar Ascent design study').build(story,onFirstPage=footer,onLaterPages=footer)

def main():
    PDF.mkdir(parents=True,exist_ok=True)
    data=json.loads((ROOT/'results/design.json').read_text());s=data['selected'];t=data['transfer_selected']
    summary=f'''# Drakkar Ascent - requirement-led results

**Service-load shell screen: {s['material']}, {s['shell_mass']:.6f} kg shell only.** Required safety factors, ring/connection mass and manufacturing details remain unresolved. This is not a final passing competition design.

| Parameter | Brief moment | Separate M + V*L case |
|---|---|---|
| Metal | {s['material']} | {t['material']} |
| Length | 1500 mm | 1500 mm |
| Outside diameter | {s['diameter_mm']:.0f} mm | {t['diameter_mm']:.0f} mm |
| Nominal wall | {s['nominal_t_mm']:.2f} mm | {t['nominal_t_mm']:.2f} mm |
| Shell mass | {s['shell_mass']:.6f} kg | {t['shell_mass']:.6f} kg |
| Assembly mass | Unresolved | Unresolved |

## Requirements and methods retained

Supplied loads/materials, rigid circular end boundaries and K = 1. Von Mises for metals; a declared quadratic screen for effective QI materials; Euler/beam-column mechanics; NASA SP-8007 geometric shell knockdowns. Bending remains in the shell and real joints. A knockdown factor is not an assigned safety factor.

## Unsupported numerical choices removed

No baseline 1.5 load multiplier, 5% wall loss, 1.5 mm initial bow, 0.35 shell cap or 0.35 Brazier multiplier. No unpressurised case, assumed bolt/flange dimensions, invented composite ply thickness or material-specific minimum wall. Nominal thickness is used directly. The old 2.878 kg assembly used different assumptions and cannot be compared as an assembly weight saving.

## Results and remaining limits

All seven materials use a common shell-only mass boundary and numerical thickness grid. Composite interaction and laminate data remain incomplete. The full report includes both moment cases, all-material load scenarios and separate closed-end pressure strength checks.

Pressure enters strength at the stated 0.3 MPa. Pressure-stabilised buckling is unresolved; the model retains a labelled no-credit capacity screen. Long-shell extrapolation, peak-shear surrogate and ideal ovalisation remain analytical limitations. Passing a numerical screen does not establish required safety-factor compliance or a global optimum.

## What makes the study complete

Specify the required safety factors, design and account for the end connections/rings, and establish manufacturing/laminate details. See the full report for equations, applicability limits and sources. No FEA or physical testing was performed.
'''
    (OUT/'Results_summary.md').write_text(summary)
    export_pdf(summary,PDF/'Drakkar_Results_Summary.pdf')
    export_pdf((ROOT/'The_Drakkar_Ascent_Challenge_Solution.md').read_text(),PDF/'Drakkar_Analytical_Report.pdf')
    included=[*PDF.glob('*.pdf'), OUT/'Results_summary.md',*sorted((ROOT/'assets').glob('*.png')),
              *sorted((ROOT/'results').glob('*')),ROOT/'The_Drakkar_Ascent_Challenge_Solution.md',
              ROOT/'House_Veridian_Design_Review_Presentation.md',ROOT/'README.md']
    manifest='DRAKKAR ASCENT OUTPUT PACKAGE\n\nPDF report and summary are in pdf/. Figures are in assets/.\nJSON is the numerical source; CSV files contain the diameter sweeps.\nRead the design assumptions and applicability limits before using the results.\n\nSHA-256 checksums:\n'
    entries=[]
    for path in included:
        name=str(path.relative_to(OUT) if path.is_relative_to(OUT) else path.relative_to(ROOT))
        entries.append((path,name));manifest+=hashlib.sha256(path.read_bytes()).hexdigest()+'  '+name+'\n'
    (OUT/'PACKAGE_MANIFEST.txt').write_text(manifest)
    with zipfile.ZipFile(OUT/'Drakkar_Output_Package.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path,name in entries:archive.write(path,name)
        archive.write(OUT/'PACKAGE_MANIFEST.txt','PACKAGE_MANIFEST.txt')
    print('Generated two PDFs, summary, manifest and ZIP in output/')

if __name__=='__main__':main()
