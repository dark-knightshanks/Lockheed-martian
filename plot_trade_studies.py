"""Render canonical figures from generated data; no duplicated structural model."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
COLORS=['#2671b8','#8571a9','#687784','#15836e','#dc8835','#ba5b69','#948a42']

def main():
    ASSETS.mkdir(exist_ok=True)
    data=json.loads((ROOT/'results/design.json').read_text())
    rows=list(csv.DictReader((ROOT/'results/trade_study.csv').open()))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'figure.dpi':180})
    fig,axes=plt.subplots(1,2,figsize=(12,5.5))
    for i,m in enumerate(data['materials']):
        group=[r for r in rows if r['material']==m['name']]
        comp=m['yield_stress']==0
        ax=axes[1 if comp else 0]
        ax.plot([float(r['diameter_mm']) for r in group],
                [float(r['objective_mass']) for r in group],label=m['name'],color=COLORS[i])
    for ax in axes:
        ax.set_xlabel('Shell / flange outer diameter (mm)')
        ax.set_ylabel('Predicted nominal mass (kg)')
        ax.grid(alpha=.2)
        ax.legend(fontsize=8)
    axes[0].set_title('Metals: shell + flanges + fasteners')
    axes[1].set_title('Composites: shell only, joints unresolved')
    s=data['selected']
    axes[0].scatter([s['diameter_mm']],[s['objective_mass']],color='#111',zorder=5)
    fig.suptitle('Discrete monocoque trade | brief moment | conditional analytical model',fontweight='bold')
    fig.tight_layout()
    fig.savefig(ASSETS/'trade_study_diameter_vs_mass.png');plt.close(fig)

    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5.5))
    s=data['selected']; t=data['transfer_selected']
    names=['Strength','Euler','Shell interaction','Ovalisation']
    x=list(range(4));w=.36
    ax1.bar([a-w/2 for a in x],list(s['utilisations'].values()),w,label='Brief design',color='#15836e')
    ax1.bar([a+w/2 for a in x],list(t['utilisations'].values()),w,label='Transfer-envelope design',color='#2671b8')
    ax1.axhline(1,color='#b94848',ls='--',label='Limit')
    ax1.set_xticks(x,names,rotation=15);ax1.set_ylabel('Utilisation at factored loads')
    ax1.set_ylim(0,1.2);ax1.legend(fontsize=8);ax1.set_title('Each design checked against its own load envelope')
    parts=['Shell','Flanges','Root bands','Fasteners']
    for k,row in enumerate([s,t]):
        j=row['connection'];vals=[row['shell_mass'],j['ring_extra_mass'],j['root_band_extra_mass'],j['fastener_mass']]
        bottom=0
        for name,value,color in zip(parts,vals,['#15836e','#2671b8','#dc8835','#8571a9']):
            ax2.bar(k,value,bottom=bottom,color=color,label=name if k==0 else None)
            bottom+=value
        ax2.text(k,bottom+.07,f'{bottom:.3f} kg',ha='center')
    ax2.set_xticks([0,1],['Brief','Transfer envelope']);ax2.set_ylabel('Assembly mass (kg)');ax2.set_title('Mass boundary is explicit')
    ax2.set_ylim(0,max(s['objective_mass'],t['objective_mass'])*1.2);ax2.legend(fontsize=8)
    fig.tight_layout();fig.savefig(ASSETS/'failure_modes_vs_diameter.png');plt.close(fig)

    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5.5),gridspec_kw={'width_ratios':[1.2,1]})
    metals=sorted([x for x in data['winners'] if x['connection']],key=lambda x:x['objective_mass'])
    labels=[x['material'].replace(' ','\n',1) for x in metals]
    for i,row in enumerate(metals):
        j=row['connection'];base=0
        for name,v,color in [('Shell',row['shell_mass'],'#15836e'),('End hardware',row['objective_mass']-row['shell_mass'],'#2671b8')]:
            ax1.bar(i,v,bottom=base,color=color,label=name if i==0 else None);base+=v
        ax1.text(i,base+.08,f'{base:.3f}',ha='center')
    ax1.set_xticks(range(len(metals)),labels,fontsize=8);ax1.set_ylabel('Assembly mass (kg)');ax1.legend(fontsize=8)
    ax1.set_ylim(0,max(x['objective_mass'] for x in metals)*1.17);ax1.set_title('All-metal minima, 1 mm diameter grid')
    for factor,color in zip([1.25,1.5,2],['#2671b8','#15836e','#dc8835']):
        r=[v for v in data['sensitivities'] if v['load_factor']==factor]
        ax2.plot([v['kdf_cap'] for v in r],[v['total_mass'] for v in r],'-o',label=f'Load factor {factor:g}',color=color)
    ax2.set_xlabel('Assumed shell / ovalisation reduction cap')
    ax2.set_ylabel('Reoptimised magnesium assembly mass (kg)')
    ax2.set_title('Sensitivity: 2 mm diameter grid');ax2.legend(fontsize=8);ax2.grid(alpha=.2)
    fig.tight_layout();fig.savefig(ASSETS/'trade_materials_comparison_barchart.png');plt.close(fig)
    print('Wrote three canonical figures in assets/')

if __name__=='__main__':main()
