"""Nominal shell concept. End connections are intentionally unspecified."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
ROOT=Path(__file__).resolve().parents[1]

def main():
    data=json.loads((ROOT/'data/original/design.json').read_text());s=data['selected']
    d=s['diameter_mm'];t=s['nominal_t_mm']
    fig=plt.figure(figsize=(13,8),layout='constrained');grid=fig.add_gridspec(3,2,height_ratios=[1,.9,.5])
    ax=fig.add_subplot(grid[0,:]);ax.axis('off');ax.set(xlim=(-100,1650),ylim=(-150,180))
    for sign in [-1,1]:
        ax.plot([0,1500],[sign*d/2]*2,color='#174d65',lw=2)
        ax.plot([0,1500],[sign*(d/2-t)]*2,color='#174d65',lw=1)
    for x in [0,1500]:ax.plot([x,x],[-d/2,d/2],ls='--',color='#dc8835',lw=3)
    ax.annotate('',(0,110),(1500,110),arrowprops={'arrowstyle':'<->'})
    ax.text(750,120,'1500 mm shell span',ha='center')
    ax.text(750,-105,'Dashed end boundaries: prescribed rigid circular end rings',ha='center',fontsize=10)
    ax.set_title(f"{s['material']} | analytical shell geometry",loc='left')
    ax=fig.add_subplot(grid[1,0]);ax.set_aspect('equal');ax.axis('off')
    for r in [d/2,d/2-t]:ax.add_patch(Circle((0,0),r,fill=False,color='#174d65'))
    ax.set(xlim=(-d*.7,d*.7),ylim=(-d*.7,d*.7))
    ax.text(0,0,f'OD {d:.0f} mm\nID {d-2*t:.2f} mm\nwall {t:.2f} mm',ha='center',va='center')
    ax.set_title('Shell cross-section')
    ax=fig.add_subplot(grid[1,1]);ax.axis('off')
    ax.text(0,.95,f"Shell-only mass: {s['shell_mass']:.6f} kg\n\nService loads: F = 30 kN; p = 0.3 MPa\nV = 1.465 kN; M = 2.198 kN m\n\nNominal thickness used directly\nDesign loads = 1.1 x service loads\nTeam design load multiplier: 1.1\nMass scope: shell only",va='top',fontsize=11,linespacing=1.6)
    ax=fig.add_subplot(grid[2,:]);ax.axis('off')
    ax.text(.01,.95,'ANALYTICAL SHELL CONCEPT | LOAD FACTOR 1.1\nK = 1 applies to buckling; real joints transfer bending through shell-wall forces.\nDimensions are analytical sizing targets; see report for model limitations.\nRing and connection mass excluded.',va='top',fontsize=11,linespacing=1.6)
    fig.suptitle('DRAKKAR ASCENT | Lockheed martian',fontweight='bold',fontsize=16)
    fig.savefig(ROOT/'reports/original/figures/thrust_barrel_cad_drawing.png',dpi=180);plt.close(fig)
    print('Generated shell concept with unresolved end boundaries')

if __name__=='__main__':main()
