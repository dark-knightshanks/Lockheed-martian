import math
import matplotlib.pyplot as plt
import numpy as np

# Set aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

# -------------------------------------------------------------
# 1. Physical Parameters and Load Definitions
# -------------------------------------------------------------
F = 30000.0         # Engine thrust [N]
p = 300000.0        # Ullage internal pressure [Pa]
M = 2197.69         # Gust bending moment [N.m]
V = 1465.13         # Gust shear force [N]
L = 1.5             # Barrel length [m]

FS_yield = 1.25     # Safety factor for yield
FS_buckle = 1.40    # Safety factor for buckling
gamma = 0.35        # NASA SP-8007 shell knockdown factor

materials = {
    'Carbon/Epoxy QI': {
        'E': 55.0e9, 'Xc': 600e6, 'Yt': 500e6, 'S': 200e6, 'rho': 1600, 'nu': 0.30, 'type': 'composite',
        'color': '#1f77b4', 'style': '-'
    },
    'Aluminium 7075-T6': {
        'E': 71.7e9, 'sigma_y': 503e6, 'rho': 2810, 'nu': 0.33, 'type': 'metal',
        'color': '#ff7f0e', 'style': '-'
    },
    'Magnesium AZ31B': {
        'E': 45.0e9, 'sigma_y': 220e6, 'rho': 1770, 'nu': 0.35, 'type': 'metal',
        'color': '#2ca02c', 'style': '--'
    },
    'Titanium Ti-6Al-4V': {
        'E': 113.8e9, 'sigma_y': 880e6, 'rho': 4430, 'nu': 0.31, 'type': 'metal',
        'color': '#d62728', 'style': ':'
    }
}

all_materials_bench = {
    'Carbon/Epoxy QI': {'E': 55.0e9, 'Xc': 600e6, 'Yt': 500e6, 'S': 200e6, 'rho': 1600, 'nu': 0.30, 'type': 'composite'},
    'Aramid/Epoxy QI': {'E': 35.0e9, 'Xc': 200e6, 'Yt': 300e6, 'S': 80e6, 'rho': 1400, 'nu': 0.34, 'type': 'composite'},
    'Magnesium AZ31B': {'E': 45.0e9, 'sigma_y': 220e6, 'rho': 1770, 'nu': 0.35, 'type': 'metal'},
    'Aluminium 7075-T6': {'E': 71.7e9, 'sigma_y': 503e6, 'rho': 2810, 'nu': 0.33, 'type': 'metal'},
    'Glass/Epoxy QI': {'E': 25.0e9, 'Xc': 300e6, 'Yt': 250e6, 'S': 100e6, 'rho': 1900, 'nu': 0.30, 'type': 'composite'},
    'Titanium Ti-6Al-4V': {'E': 113.8e9, 'sigma_y': 880e6, 'rho': 4430, 'nu': 0.31, 'type': 'metal'},
    'Steel 4130': {'E': 205.0e9, 'sigma_y': 460e6, 'rho': 7850, 'nu': 0.29, 'type': 'metal'},
}

def compute_thicknesses(D_m, props):
    R = D_m / 2.0
    E = props['E']
    rho = props['rho']
    nu = props['nu']
    
    # 1. Global Euler Column Buckling
    P_eq = F + (2.0 * M / R)
    t_euler = (FS_buckle * P_eq * (L**2)) / (math.pi**3 * (R**3) * E)
    
    # 2. Local Thin-Shell Buckling (NASA SP-8007)
    coeff = gamma * E / math.sqrt(3.0 * (1.0 - nu**2))
    N_comp_R = (F / (2.0 * math.pi)) + (M / (math.pi * R))
    t_local = math.sqrt((FS_buckle * N_comp_R) / coeff)
    
    # 3. Material Yield / Failure
    A_x = (F / (2.0 * math.pi * R)) + (M / (math.pi * (R**2))) - (p * R / 2.0)
    B_th = p * R
    tau_val = V / (math.pi * R)
    
    if props['type'] == 'metal':
        vm_bracket = A_x**2 + (A_x * B_th) + B_th**2 + (3.0 * tau_val**2)
        t_yield = (math.sqrt(vm_bracket) * FS_yield) / props['sigma_y']
    else:
        term = ((A_x / props['Xc'])**2 + 
                (B_th / props['Yt'])**2 + 
                (A_x * B_th) / (props['Xc'] * props['Yt']) + 
                (tau_val / props['S'])**2)
        t_yield = math.sqrt(term) * FS_yield
        
    t_design = max(t_yield, t_euler, t_local)
    mass = 2.0 * math.pi * R * L * t_design * rho
    
    return t_yield, t_euler, t_local, t_design, mass


# -------------------------------------------------------------
# PLOT 1: Outer Diameter (D) vs Total Structural Mass (m)
# -------------------------------------------------------------
d_range_mm = np.linspace(70, 300, 300)
fig, ax = plt.subplots(figsize=(10, 6))

min_points = {}

for mat_name, props in materials.items():
    masses = []
    for d_mm in d_range_mm:
        _, _, _, _, m = compute_thicknesses(d_mm / 1000.0, props)
        masses.append(m)
    
    masses = np.array(masses)
    min_idx = np.argmin(masses)
    min_d = d_range_mm[min_idx]
    min_m = masses[min_idx]
    min_points[mat_name] = (min_d, min_m)
    
    ax.plot(d_range_mm, masses, label=f"{mat_name} (Min: {min_m:.2f} kg @ {min_d:.0f} mm)",
            color=props['color'], linestyle=props['style'], linewidth=2.4)
    ax.scatter([min_d], [min_m], color=props['color'], s=60, zorder=5)

# Annotate Global Optimum
opt_d, opt_m = min_points['Carbon/Epoxy QI']
ax.annotate(f'Global Champion:\nCarbon/Epoxy QI\nMass = {opt_m:.2f} kg\nD = {opt_d:.0f} mm',
            xy=(opt_d, opt_m), xytext=(opt_d + 20, opt_m + 1.2),
            arrowprops=dict(facecolor='#1f77b4', edgecolor='none', shrink=0.08, width=1.8, headwidth=8),
            fontsize=10.5, fontweight='bold', bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#1f77b4", lw=1.5))

# Annotate Best Metal Optimum
al_d, al_m = min_points['Aluminium 7075-T6']
ax.annotate(f'Best Metallic:\nAl 7075-T6\nMass = {al_m:.2f} kg\nD = {al_d:.0f} mm',
            xy=(al_d, al_m), xytext=(al_d + 15, al_m + 1.7),
            arrowprops=dict(facecolor='#ff7f0e', edgecolor='none', shrink=0.08, width=1.8, headwidth=8),
            fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#ff7f0e", lw=1.5))

# Reference lines
ax.axvline(x=100, color='gray', linestyle=':', linewidth=1.5, label='Upper Vehicle Body Diameter (Du = 100 mm)')
ax.axvline(x=300, color='red', linestyle='--', linewidth=1.5, label='Max Allowable Diameter (300 mm)')

ax.set_title('The Drakkar Ascent Challenge: Structural Mass vs Outer Diameter (D)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Outer Diameter D (mm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Thrust Barrel Mass (kg)', fontsize=12, fontweight='bold')
ax.set_xlim(70, 310)
ax.set_ylim(0.8, 6.0)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper right', frameon=True, fontsize=9.5)

plt.tight_layout()
plot1_path = "trade_study_diameter_vs_mass.png"
plt.savefig(plot1_path)
plt.close()
print(f"Saved: {plot1_path}")


# -------------------------------------------------------------
# PLOT 2: Failure Mode Breakdown (Thickness vs Diameter)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Subplot 1: Carbon/Epoxy QI
ce_props = materials['Carbon/Epoxy QI']
t_yield_list = []
t_euler_list = []
t_local_list = []
t_des_list = []

for d_mm in d_range_mm:
    ty, te, tl, td, _ = compute_thicknesses(d_mm / 1000.0, ce_props)
    t_yield_list.append(ty * 1000)
    t_euler_list.append(te * 1000)
    t_local_list.append(tl * 1000)
    t_des_list.append(td * 1000)

ax1.plot(d_range_mm, t_euler_list, 'r--', label='Euler Column Buckling', linewidth=2.0)
ax1.plot(d_range_mm, t_local_list, 'b-', label='Local Shell Buckling', linewidth=2.0)
ax1.plot(d_range_mm, t_yield_list, 'g-.', label='Material Strength (Quadratic)', linewidth=1.8)
ax1.plot(d_range_mm, t_des_list, 'k', label='Active Sizing Envelope t(D)', linewidth=2.8)
ax1.axvline(x=opt_d, color='#1f77b4', linestyle=':', label=f'Optimal D = {opt_d:.0f} mm')

ax1.set_title('(a) Carbon/Epoxy QI Sizing Limits', fontsize=12, fontweight='bold')
ax1.set_xlabel('Outer Diameter D (mm)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Required Wall Thickness t (mm)', fontsize=11, fontweight='bold')
ax1.set_xlim(70, 300)
ax1.set_ylim(0, 4.5)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='upper right', fontsize=9.5)

# Subplot 2: Aluminium 7075-T6
al_props = materials['Aluminium 7075-T6']
t_yield_list_al = []
t_euler_list_al = []
t_local_list_al = []
t_des_list_al = []

for d_mm in d_range_mm:
    ty, te, tl, td, _ = compute_thicknesses(d_mm / 1000.0, al_props)
    t_yield_list_al.append(ty * 1000)
    t_euler_list_al.append(te * 1000)
    t_local_list_al.append(tl * 1000)
    t_des_list_al.append(td * 1000)

ax2.plot(d_range_mm, t_euler_list_al, 'r--', label='Euler Column Buckling', linewidth=2.0)
ax2.plot(d_range_mm, t_local_list_al, 'b-', label='Local Shell Buckling', linewidth=2.0)
ax2.plot(d_range_mm, t_yield_list_al, 'g-.', label='von Mises Yielding', linewidth=1.8)
ax2.plot(d_range_mm, t_des_list_al, 'k', label='Active Sizing Envelope t(D)', linewidth=2.8)
ax2.axvline(x=al_d, color='#ff7f0e', linestyle=':', label=f'Optimal D = {al_d:.0f} mm')

ax2.set_title('(b) Aluminium 7075-T6 Sizing Limits', fontsize=12, fontweight='bold')
ax2.set_xlabel('Outer Diameter D (mm)', fontsize=11, fontweight='bold')
ax2.set_xlim(70, 300)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(loc='upper right', fontsize=9.5)

plt.suptitle('Governing Failure Mode Transition: Euler Cliff vs Local Shell Stability', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()
plot2_path = "failure_modes_vs_diameter.png"
plt.savefig(plot2_path)
plt.close()
print(f"Saved: {plot2_path}")


# -------------------------------------------------------------
# PLOT 3: Material Benchmark Bar Chart (D=300mm vs Optimal D)
# -------------------------------------------------------------
mat_names = list(all_materials_bench.keys())
mass_at_300 = []
mass_at_opt = []
opt_diameters = []

for m_name, props in all_materials_bench.items():
    # at 300 mm
    _, _, _, _, m300 = compute_thicknesses(0.30, props)
    mass_at_300.append(m300)
    
    # find optimal
    best_m = 1e9
    best_d = 0.30
    for d_mm in np.linspace(80, 300, 221):
        _, _, _, _, m_val = compute_thicknesses(d_mm / 1000.0, props)
        if m_val < best_m:
            best_m = m_val
            best_d = d_mm
    mass_at_opt.append(best_m)
    opt_diameters.append(best_d)

x = np.arange(len(mat_names))
width = 0.38

fig, ax = plt.subplots(figsize=(11, 6))

rects1 = ax.bar(x - width/2, mass_at_300, width, label='At Max Diameter (D = 300 mm)', color='#aec7e8', edgecolor='#1f77b4', hatch='//')
rects2 = ax.bar(x + width/2, mass_at_opt, width, label='At Optimal Diameter (D = 100-120 mm)', color='#2ca02c', edgecolor='#1b611b')

ax.set_ylabel('Total Structural Mass (kg)', fontsize=12, fontweight='bold')
ax.set_title('Material Performance Comparison: Mass Reduction from Diameter Optimization', fontsize=13, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels([f"{name}\n(Opt D={opt_diameters[i]:.0f}mm)" for i, name in enumerate(mat_names)], fontsize=9)
ax.grid(True, axis='y', linestyle='--', alpha=0.7)
ax.legend(fontsize=10.5)

# Value labels on top of bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f} kg',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plot3_path = "trade_materials_comparison_barchart.png"
plt.savefig(plot3_path)
plt.close()
print(f"Saved: {plot3_path}")
