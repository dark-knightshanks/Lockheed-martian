"""Plot shell-only results without implying complete assembly compliance."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
    d=json.loads((ROOT/'results/design.json').read_text())
    rows=list(csv.DictReader((ROOT/'results/trade_study.csv').open()))
    out=ROOT/'assets';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'figure.dpi':180})
    fig,axes=plt.subplots(1,2,figsize=(12,5.5))
    for m in d['materials']:
        ax=axes[int(m['yield_stress']==0)];r=[x for x in rows if x['material']==m['name']]
        ax.plot([float(x['diameter_mm']) for x in r],[float(x['shell_mass']) for x in r],label=m['name'])
    for ax,title in zip(axes,['Metal shells','Equivalent-QI shells: laminate unresolved']):
        ax.set(xlabel='Outside diameter (mm)',ylabel='Shell-only mass (kg)',title=title)
        ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.suptitle('Service-load screens | rings/joints and required safety factors unresolved')
    fig.tight_layout();fig.savefig(out/'trade_study_diameter_vs_mass.png');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5.5))
    for ax,key,label in zip(axes,['selected','transfer_selected'],['Brief moment','Separate M + V*L scenario']):
        r=d[key];names=list(r['utilisations'])
        ax.bar(names,list(r['utilisations'].values()),color='#2671b8')
        ax.axhline(1,color='#b94848',ls='--');ax.tick_params(axis='x',rotation=15)
        ax.set(ylabel='Screen utilisation at service loads',ylim=(0,1.2),title=f"{label}\n{r['material']}: {r['shell_mass']:.3f} kg shell")
    fig.suptitle('Numerical screen limit is not required safety-factor compliance')
    fig.tight_layout();fig.savefig(out/'failure_modes_vs_diameter.png');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,6))
    wins=d['winners'];labels=[x['material'].replace(' ','\n',1) for x in wins]
    axes[0].bar(range(len(wins)),[x['shell_mass'] for x in wins],color=['#2671b8']*4+['#dc8835']*3)
    axes[0].set_xticks(range(len(wins)),labels,fontsize=7)
    axes[0].set(ylabel='Shell-only mass (kg)',title='All materials | common mass boundary')
    for m in d['materials']:
        r=[x for x in d['sensitivities'] if x['material']==m['name']]
        axes[1].plot([x['load_multiplier'] for x in r],[x['shell_mass'] for x in r],'-o',label=m['name'])
    axes[1].set(xlabel='Illustrative load multiplier (not assigned safety factor)',ylabel='Re-screened shell mass (kg)',title='All-material load scenarios')
    axes[1].legend(fontsize=7);axes[1].grid(alpha=.2)
    fig.tight_layout();fig.savefig(out/'trade_materials_comparison_barchart.png');plt.close(fig)
    print('Generated three shell-screen figures')

if __name__=='__main__':main()
