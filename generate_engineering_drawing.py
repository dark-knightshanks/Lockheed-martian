import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Wedge

# Set styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

fig, ax = plt.subplots(figsize=(15, 10))
ax.set_xlim(0, 150)
ax.set_ylim(0, 100)
ax.axis('off')

# -------------------------------------------------------------
# 1. Outer Border & Engineering Title Block
# -------------------------------------------------------------
# Main border
border = Rectangle((2, 2), 146, 96, fill=False, edgecolor='black', linewidth=2.0)
ax.add_patch(border)

# Title block (Bottom-Right corner)
tb_x, tb_y, tb_w, tb_h = 95, 2, 53, 24
ax.add_patch(Rectangle((tb_x, tb_y), tb_w, tb_h, fill=False, edgecolor='black', linewidth=1.5))
ax.plot([tb_x, tb_x + tb_w], [tb_y + 16, tb_y + 16], 'k-', lw=1.0)
ax.plot([tb_x, tb_x + tb_w], [tb_y + 10, tb_y + 10], 'k-', lw=1.0)
ax.plot([tb_x, tb_x + tb_w], [tb_y + 5, tb_y + 5], 'k-', lw=1.0)
ax.plot([tb_x + 26, tb_x + 26], [tb_y, tb_y + 10], 'k-', lw=1.0)

ax.text(tb_x + 2, tb_y + 20, "VEERMATA JIJABAI TECHNOLOGICAL INSTITUTE (VJTI)", fontsize=8.5, fontweight='bold')
ax.text(tb_x + 2, tb_y + 17, "HOUSE VERIDIAN: THE DRAKKAR ASCENT CHALLENGE", fontsize=8.5, fontweight='bold', color='#1f77b4')
ax.text(tb_x + 2, tb_y + 12.5, "DWG: CYLINDRICAL BOOSTER THRUST BARREL SECTION", fontsize=8, fontweight='bold')
ax.text(tb_x + 2, tb_y + 7, "DWG NO: HVR-TB-001", fontsize=8)
ax.text(tb_x + 28, tb_y + 7, "REV: 1.0 (FINAL OPTIMAL)", fontsize=8)
ax.text(tb_x + 2, tb_y + 2, "MATERIAL: Carbon/Epoxy QI", fontsize=8)
ax.text(tb_x + 28, tb_y + 2, "MASS: 1.27 kg | SCALE: NTS", fontsize=8, fontweight='bold', color='darkgreen')

# -------------------------------------------------------------
# 2. View 1: Main Side Elevation (Longitudinal View)
# -------------------------------------------------------------
ax.text(8, 93, "VIEW A: LONGITUDINAL ELEVATION & LOAD SCHEMATIC", fontsize=11, fontweight='bold', color='#333333')

# Cylinder wall geometry
cyl_x, cyl_y = 20, 68
cyl_len = 90
cyl_dia = 16
wall_t = 0.8

# Centerline
ax.plot([cyl_x - 5, cyl_x + cyl_len + 5], [cyl_y, cyl_y], 'r-.', lw=1.0, alpha=0.8)

# Top wall
ax.add_patch(Rectangle((cyl_x, cyl_y + cyl_dia/2 - wall_t), cyl_len, wall_t, facecolor='#4b6584', edgecolor='black', lw=1.0))
# Bottom wall
ax.add_patch(Rectangle((cyl_x, cyl_y - cyl_dia/2), cyl_len, wall_t, facecolor='#4b6584', edgecolor='black', lw=1.0))
# Interior cavity (hollow)
ax.add_patch(Rectangle((cyl_x, cyl_y - cyl_dia/2 + wall_t), cyl_len, cyl_dia - 2*wall_t, facecolor='#f1f2f6', edgecolor='none'))

# Rigid End Rings (Specified in Challenge Brief)
ring_w = 2.5
ring_h = cyl_dia + 2.0
# Forward end ring (Top/Upper stage interface)
ax.add_patch(Rectangle((cyl_x + cyl_len, cyl_y - ring_h/2), ring_w, ring_h, facecolor='#778ca3', edgecolor='black', lw=1.2))
# Aft end ring (Engine thrust structure interface)
ax.add_patch(Rectangle((cyl_x - ring_w, cyl_y - ring_h/2), ring_w, ring_h, facecolor='#778ca3', edgecolor='black', lw=1.2))

# Dimension: Length L = 1500 mm
ax.annotate('', xy=(cyl_x, cyl_y + cyl_dia/2 + 5), xytext=(cyl_x + cyl_len, cyl_y + cyl_dia/2 + 5),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
ax.plot([cyl_x, cyl_x], [cyl_y + cyl_dia/2 + 1, cyl_y + cyl_dia/2 + 7], 'k-', lw=0.8)
ax.plot([cyl_x + cyl_len, cyl_x + cyl_len], [cyl_y + cyl_dia/2 + 1, cyl_y + cyl_dia/2 + 7], 'k-', lw=0.8)
ax.text(cyl_x + cyl_len/2, cyl_y + cyl_dia/2 + 6.5, "LENGTH L = 1500 mm", ha='center', fontsize=9, fontweight='bold')

# Dimension: Outer Diameter D = 120 mm
ax.annotate('', xy=(cyl_x + cyl_len + 8, cyl_y - cyl_dia/2), xytext=(cyl_x + cyl_len + 8, cyl_y + cyl_dia/2),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
ax.plot([cyl_x + cyl_len + 3, cyl_x + cyl_len + 10], [cyl_y - cyl_dia/2, cyl_y - cyl_dia/2], 'k-', lw=0.8)
ax.plot([cyl_x + cyl_len + 3, cyl_x + cyl_len + 10], [cyl_y + cyl_dia/2, cyl_y + cyl_dia/2], 'k-', lw=0.8)
ax.text(cyl_x + cyl_len + 11, cyl_y, "Ø 120 mm (OUTER DIA)", va='center', fontsize=8.5, fontweight='bold')

# Applied Load Callouts on View A
# Engine Thrust T = 30 kN
ax.annotate('ENGINE THRUST\nT = 30 kN (AXIAL)', xy=(cyl_x - ring_w, cyl_y), xytext=(cyl_x - 17, cyl_y),
            arrowprops=dict(facecolor='red', edgecolor='black', shrink=0.05, width=2.5, headwidth=8),
            fontsize=8, fontweight='bold', color='darkred', ha='center', va='center')

# Internal Pressure p = 0.3 MPa
for px in [cyl_x + 20, cyl_x + 45, cyl_x + 70]:
    ax.annotate('', xy=(px, cyl_y + cyl_dia/2 - wall_t), xytext=(px, cyl_y + 2),
                arrowprops=dict(arrowstyle='->', color='#2ed573', lw=1.5))
    ax.annotate('', xy=(px, cyl_y - cyl_dia/2 + wall_t), xytext=(px, cyl_y - 2),
                arrowprops=dict(arrowstyle='->', color='#2ed573', lw=1.5))
ax.text(cyl_x + 45, cyl_y + 0.5, "INTERNAL PRESSURE p = 0.3 MPa", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#20bf6b')

# Gust Bending Moment & Shear
ax.annotate('GUST SHEAR V = 1465 N\nBENDING M = 2198 N·m', xy=(cyl_x + cyl_len + ring_w, cyl_y + 4),
            xytext=(cyl_x + cyl_len + 16, cyl_y + 12),
            arrowprops=dict(facecolor='blue', edgecolor='black', shrink=0.05, width=1.5, headwidth=6),
            fontsize=8, fontweight='bold', color='navy')

# -------------------------------------------------------------
# 3. View 2: Cross-Section B-B (Transverse View)
# -------------------------------------------------------------
ax.text(8, 48, "VIEW B-B: CROSS-SECTION DETAILS", fontsize=11, fontweight='bold', color='#333333')

sec_x, sec_y = 25, 27
r_out = 14
r_in = 12.6

# Centerlines
ax.plot([sec_x - 18, sec_x + 18], [sec_y, sec_y], 'r-.', lw=0.8, alpha=0.7)
ax.plot([sec_x, sec_x], [sec_y - 18, sec_y + 18], 'r-.', lw=0.8, alpha=0.7)

# Rings
circle_out = Circle((sec_x, sec_y), r_out, facecolor='#4b6584', edgecolor='black', lw=1.2)
circle_in = Circle((sec_x, sec_y), r_in, facecolor='white', edgecolor='black', lw=1.0)
ax.add_patch(circle_out)
ax.add_patch(circle_in)

# Annotations for View B
ax.annotate('OUTER DIA: Ø 120.0 mm', xy=(sec_x + r_out * 0.707, sec_y + r_out * 0.707),
            xytext=(sec_x + 18, sec_y + 15),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.0),
            fontsize=8, fontweight='bold')

ax.annotate('INNER DIA: Ø 117.2 mm', xy=(sec_x + r_in * 0.707, sec_y - r_in * 0.707),
            xytext=(sec_x + 18, sec_y - 8),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.0),
            fontsize=8)

ax.annotate('WALL THICKNESS:\nt = 1.40 mm', xy=(sec_x - r_out, sec_y),
            xytext=(sec_x - 22, sec_y + 8),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.0),
            fontsize=8, fontweight='bold', color='#1f77b4')

# -------------------------------------------------------------
# 4. View 3: Laminate Micro-Architecture & Ply Layup
# -------------------------------------------------------------
ax.text(58, 48, "DETAIL C: 9-PLY QUASI-ISOTROPIC LAMINATE ARCHITECTURE", fontsize=11, fontweight='bold', color='#333333')

lay_x, lay_y = 60, 20
ply_w = 28
ply_h = 2.2

plies = [
    ("Ply 9: 0° (Outer Hoop/Axial)", "#2bcbba"),
    ("Ply 8: +45° (Shear Web)", "#45aaf2"),
    ("Ply 7: -45° (Shear Web)", "#4b7bec"),
    ("Ply 6: 90° (Hoop Pressure)", "#a55eea"),
    ("Ply 5: 0° (Core Axial Rib)", "#fd9644"),
    ("Ply 4: 90° (Hoop Pressure)", "#a55eea"),
    ("Ply 3: -45° (Shear Web)", "#4b7bec"),
    ("Ply 2: +45° (Shear Web)", "#45aaf2"),
    ("Ply 1: 0° (Inner Face)", "#2bcbba")
]

for idx, (p_name, p_color) in enumerate(plies):
    curr_y = lay_y + idx * (ply_h + 0.3)
    ax.add_patch(Rectangle((lay_x, curr_y), ply_w, ply_h, facecolor=p_color, edgecolor='black', lw=0.8))
    ax.text(lay_x + 1.5, curr_y + 0.6, p_name, fontsize=7.2, fontweight='bold', color='black')

ax.text(lay_x + ply_w + 3, lay_y + 12, "TOTAL THICKNESS: 1.40 mm\nEach Ply: 0.155 mm Prepreg Tape\nSymmetric & Balanced Layup\n[0 / +45 / -45 / 90 / 0 / 90 / -45 / +45 / 0]",
        fontsize=8, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", fc="#f1f2f6", ec="gray", lw=1.0))

# -------------------------------------------------------------
# 5. General Engineering Notes
# -------------------------------------------------------------
notes_text = (
    "GENERAL ENGINEERING NOTES:\n"
    "1. ALL DIMENSIONS ARE IN MILLIMETERS UNLESS SPECIFIED OTHERWISE.\n"
    "2. THEORETICAL DESIGN CONDUCTED IN STRICT COMPLIANCE WITH R5ME3203T COMPETITION RULES (NO FEA).\n"
    "3. SIZED AGAINST LOCAL SHELL BUCKLING (NASA SP-8007, KNOCKDOWN GAMMA = 0.35) AND EULER COLUMN BUCKLING.\n"
    "4. MARGIN OF SAFETY: MS_buckle = +0.00 (CRITICAL SIZING PINCH POINT), MS_yield = +1.43, MS_euler = +0.58.\n"
    "5. END RINGS ARE RIGID TITANIUM/ALUMINUM SPLICE COLLARS FOR UNIFORM LOAD INTRODUCTION AT PROP TANK & GIMBAL."
)
ax.text(8, 8, notes_text, fontsize=7.2, family='monospace', bbox=dict(boxstyle="square,pad=0.6", fc="#fafafa", ec="black", lw=1.0))

plt.tight_layout()
dwg_path = "thrust_barrel_cad_drawing.png"
plt.savefig(dwg_path)
plt.close()
print(f"Saved: {dwg_path}")
