"""Nominal shell concept. End connections are intentionally unspecified."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'results/design.json').read_text());s=data['selected']
    d=s['diameter_mm'];t=s['nominal_t_mm']
    fig=plt.figure(figsize=(13,8),layout='constrained');grid=fig.add_gridspec(3,2,height_ratios=[1,.9,.5])
    ax=fig.add_subplot(grid[0,:]);ax.axis('off');ax.set(xlim=(-100,1650),ylim=(-150,180))
    for sign in [-1,1]:
        ax.plot([0,1500],[sign*d/2]*2,color='#174d65',lw=2)
        ax.plot([0,1500],[sign*(d/2-t)]*2,color='#174d65',lw=1)
    for x in [0,1500]:ax.plot([x,x],[-d/2,d/2],ls='--',color='#dc8835',lw=3)
    ax.annotate('',(0,110),(1500,110),arrowprops={'arrowstyle':'<->'})
    ax.text(750,120,'1500 mm shell span',ha='center')
    ax.text(750,-105,'Dashed end boundaries: prescribed rigid rings; geometry and mass unresolved',ha='center',fontsize=10)
    ax.set_title(f"{s['material']} | nominal shell concept - not a manufacturing drawing",loc='left')
    ax=fig.add_subplot(grid[1,0]);ax.set_aspect('equal');ax.axis('off')
    for r in [d/2,d/2-t]:ax.add_patch(Circle((0,0),r,fill=False,color='#174d65'))
    ax.set(xlim=(-d*.7,d*.7),ylim=(-d*.7,d*.7))
    ax.text(0,0,f'OD {d:.0f} mm\nID {d-2*t:.2f} mm\nwall {t:.2f} mm',ha='center',va='center')
    ax.set_title('Shell cross-section')
    ax=fig.add_subplot(grid[1,1]);ax.axis('off')
    ax.text(0,.95,f"Shell-only mass: {s['shell_mass']:.6f} kg\n\nService loads: F = 30 kN; p = 0.3 MPa\nV = 1.465 kN; M = 2.198 kN m\n\nNominal thickness used directly\nNo assigned initial bow or thickness loss\nRequired safety factor: unspecified\nTotal assembly mass: unresolved",va='top',fontsize=11,linespacing=1.6)
    ax=fig.add_subplot(grid[2,:]);ax.axis('off')
    ax.text(.01,.95,'SERVICE-LOAD SCREEN, NOT A PASSING COMPETITION DESIGN\nK = 1 applies to buckling; real joints transfer bending through shell-wall forces.\nRing/joint dimensions, manufacturing, and required safety factors need resolution.\nNo bolt count, ply schedule, flange dimensions or complete assembly weight is implied.',va='top',fontsize=11,linespacing=1.6)
    fig.suptitle('DRAKKAR ASCENT | requirement-led shell study',fontweight='bold',fontsize=16)
    fig.savefig(ROOT/'assets/thrust_barrel_cad_drawing.png',dpi=180);plt.close(fig)
    print('Generated shell concept with unresolved end boundaries')

if __name__=='__main__':main()
