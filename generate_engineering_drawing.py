"""Dimensioned classroom concept, generated from the selected analytical design."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Arc
ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'results/design.json').read_text());s=data['selected'];j=s['connection']
    fig=plt.figure(figsize=(14,9),layout='constrained')
    grid=fig.add_gridspec(3,2,height_ratios=[1.1,1,.72])
    ax=fig.add_subplot(grid[0,:]);ax.set_xlim(-130,1700);ax.set_ylim(-190,250);ax.axis('off')
    d=s['diameter_mm'];t=s['nominal_t_mm'];ft=j['flange_t_mm'];w=j['flange_width_mm']
    for sign in [-1,1]:
        y=sign*d/2
        ax.plot([0,1500],[y,y],color='#174d65',lw=2)
        ax.plot([ft,1500-ft],[y-sign*t,y-sign*t],color='#174d65',lw=1)
    for x in [0,1500-ft]:
        ax.add_patch(Rectangle((x,-d/2),ft,d,facecolor='#d9e4eb',edgecolor='#174d65'))
        ax.add_patch(Rectangle((x,-d/2+w),ft,d-2*w,facecolor='white',edgecolor='#174d65'))
    ax.plot([-70,1570],[0,0],ls='-.',lw=.8,color='#888')
    ax.annotate('',(0,d/2+45),(1500,d/2+45),arrowprops={'arrowstyle':'<->'})
    ax.text(750,d/2+58,'1500 mm TOTAL BARREL LENGTH, including integral flanges',ha='center',fontsize=10)
    ax.annotate('F = 30 kN',(0,0),(-110,0),arrowprops={'arrowstyle':'->','color':'#b34c47'},ha='center',fontsize=9)
    ax.annotate('V = 1.465 kN',(1500,0),(1500,-165),arrowprops={'arrowstyle':'->','color':'#2671b8'},ha='center',fontsize=9)
    ax.add_patch(Arc((1555,30),95,95,theta1=25,theta2=290,color='#2671b8',lw=1.5))
    ax.annotate('',(1571,-15),(1548,-16),arrowprops={'arrowstyle':'->','color':'#2671b8'})
    ax.text(1600,95,'M = 2.198 kN m',ha='center',fontsize=9,color='#2671b8')
    for x in [300,750,1200]:
        ax.annotate('',(x,d/2-t),(x,15),arrowprops={'arrowstyle':'->','color':'#15836e'})
        ax.annotate('',(x,-d/2+t),(x,-15),arrowprops={'arrowstyle':'->','color':'#15836e'})
    ax.text(750,-150,'p = 0.300 MPa | Service loads shown; analysis uses 1.5 x loads',ha='center',fontsize=10)
    ax.set_title(f"LONGITUDINAL SECTION | {s['material']} | conceptual geometry, NTS",loc='left',fontweight='bold')

    ax=fig.add_subplot(grid[1,0]);ax.set_aspect('equal');ax.axis('off')
    for rad,color,fill in [(d/2,'#174d65',False),(j['flange_bore_mm']/2,'#174d65',False)]:
        ax.add_patch(Circle((0,0),rad,fill=fill,edgecolor=color,lw=2))
    import math
    for k in range(j['bolts_per_end']):
        a=2*math.pi*k/j['bolts_per_end'];r=j['bolt_circle_mm']/2
        ax.add_patch(Circle((r*math.cos(a),r*math.sin(a)),j['hole_mm']/2,fill=False,lw=.7))
    ax.set_xlim(-d*.65,d*.65);ax.set_ylim(-d*.65,d*.65)
    ax.text(0,15,f"OD {d:.0f} mm\nBore {j['flange_bore_mm']:.1f} mm\nPCD {j['bolt_circle_mm']:.1f} mm",ha='center',va='center',fontsize=10)
    ax.text(0,-40,f"{j['bolts_per_end']} holes / end\n{j['hole_mm']:.1f} mm diameter",ha='center',fontsize=9)
    ax.set_title('END FLANGE: equally spaced axial through bolts',fontsize=11,loc='left')

    ax=fig.add_subplot(grid[1,1]);ax.axis('off')
    lines=[f"Shell nominal wall: {t:.2f} mm",f"Minimum analysed wall: {s['minimum_t_mm']:.4f} mm (95%)",
           f"Integral flange: {ft:.1f} mm axial x {w:.1f} mm radial",'Root band: 20 mm taper after each flange',
           'Taper wall from 2t at root to t at barrel',f"Fasteners: {j['bolts_per_end']} x {j['bolt_d_mm']:.0f} mm Ti-6Al-4V per end",
           f"Specified minimum bolt core: {j['bolt_d_mm']*.75:.2f} mm",'Nut engagement >= 0.7 x nominal bolt diameter',
           'Two washers/bolt; dimensions defined in report',f"Modelled assembly mass: {s['objective_mass']:.3f} kg"]
    ax.text(0,1,'\n'.join(lines),va='top',fontsize=10,linespacing=1.65)
    ax.set_title('DIMENSIONS & MASS',loc='left',fontsize=11,pad=12)

    ax=fig.add_subplot(grid[2,:]);ax.axis('off')
    notes=('CONCEPT FOR THEORETICAL COMPETITION — not a manufacturing release\n'
           'Rigid end rings are the prescribed boundary idealisation. K = 1 applies to buckling only; joints transfer bending.\n'
           'Single-piece machined metal barrel avoids welding the specified temper. Dimensions include both flanges.\n'
           'Joint model assumes rigid mating faces, equal bolt spacing, 2x prying envelope and 1.5 root stress factor.\n'
           'Mating adapters, seal, coating/galvanic isolation and detailed thread/preload qualification are outside the model.\n'
           'No FEA or hardware testing. See report for assumptions, validity limits and the separate transfer-envelope design.')
    ax.text(.01,.95,notes,va='top',fontsize=10,linespacing=1.55,bbox={'boxstyle':'round,pad=.7','facecolor':'#f2f6f8','edgecolor':'#ccd8df'})
    fig.suptitle('DRAKKAR ASCENT | corrected all-metal design study',fontsize=16,fontweight='bold')
    (ROOT/'assets').mkdir(exist_ok=True)
    fig.savefig(ROOT/'assets/thrust_barrel_cad_drawing.png',dpi=180);plt.close(fig)
    print('Wrote assets/thrust_barrel_cad_drawing.png')

if __name__=='__main__':main()
