# Drakkar Ascent — corrected design review notes

Numerical source: `results/design.json`. This is a presentation script, not a claim of flight qualification.

## 1. Design objective and explicit basis

Minimise modelled structural assembly mass in a discrete unstiffened-barrel family. L = 1500 mm between mating faces; OD <= 300 mm. Use K = 1 for buckling while retaining joint-transferred bending. Project assumptions: 1.5 load factor, 5% wall-thickness reduction, 1.5 mm initial bow and 0.35 shell/ovalisation reduction cap. These factors are not specified by the brief.

## 2. Loads

F = 30 kN; p = 0.3 MPa; V = 1.465129 kN; M = 2.197694 kN m. Separate transfer scenario M + V*L = 4.395388 kN m. No helpful pressure stabilisation is used in buckling.

## 3. What changed from the original analysis

Actual axial force in Euler; explicit secant amplification and initial bow; exact A/I and mean radius; co-located circumferential stress checks; local combined-load screen; interior ovalisation check; manufacturable thickness grid; joint and hardware mass. The nine-ply non-QI specification and rounded-negative passing margin have been removed.

## 4. Material and diameter trade

| Metal | OD (mm) | Wall (mm) | Shell (kg) | Modelled assembly (kg) |
| --- | --- | --- | --- | --- |
| Magnesium AZ31B | 158 | 1.80 | 2.345 | 2.878 |
| Aluminium 7075-T6 | 160 | 1.40 | 2.940 | 3.440 |
| Titanium Ti-6Al-4V | 152 | 1.15 | 3.621 | 4.181 |
| Steel 4130 | 150 | 0.85 | 4.690 | 5.781 |

![Trade](assets/trade_study_diameter_vs_mass.png)

Composites are evaluated separately as shell-only candidates, because their joints and actual laminate stiffness/allowables are not established. No universal winner is claimed.

## 5. Selected all-metal concept

Magnesium AZ31B; OD 158 mm; nominal wall 1.80 mm; minimum analysed 1.7100 mm. Each integral flange is 16.0 mm thick with 36 x 4 mm titanium bolts on 146.0 mm PCD.

| Included item | Nominal mass (kg) |
| --- | --- |
| Shell baseline | 2.345135 |
| Two integral flange additions | 0.261721 |
| Two root taper additions | 0.030728 |
| Both sets of bolts, nuts and washers | 0.239941 |
| TOTAL MODELLED | 2.877525 |

![Drawing](assets/thrust_barrel_cad_drawing.png)

## 6. Verification

| Check | Utilisation at design load | Margin (capacity/demand - 1) |
| --- | --- | --- |
| strength | 0.822757 | +0.215426 |
| Euler | 0.088916 | +10.246536 |
| shell_interaction | 0.919964 | +0.086999 |
| ovalisation | 0.993815 | +0.006224 |
| Joint: bolt | 0.998136 | +0.001867 |
| Joint: flange | 0.991037 | +0.009044 |
| Joint: washer_bearing | 0.627943 | +0.592501 |
| Joint: thread_strip | 0.925618 | +0.080360 |
| Joint: bearing | 0.008114 | +122.249199 |
| Joint: pullthrough | 0.142090 | +6.037772 |

All IMPLEMENTED checks pass at factored loads. The rigid-ring idealisation, empirical long-shell extrapolation, transverse-shear surrogate and assumed joint prying/root factors remain model limitations.

## 7. Alternative moment envelope and sensitivity

The transfer-envelope candidate is Magnesium AZ31B, 212 mm OD x 2.10 mm wall, 4.423 kg. It is a separate design, not the brief candidate checked with an unreported extra moment.

![Sensitivity](assets/trade_materials_comparison_barchart.png)

No guaranteed score, unrestricted global optimum, impact resistance or flight readiness is claimed. Instructor acceptance of the explicit design basis and additional laminate/joint data determine whether further refinement is appropriate.
