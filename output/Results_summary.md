# Drakkar Ascent - results at a glance

**Recommended analytical candidate for the brief loads: 2.878 kg modelled assembly.** The expanded geometric search reduces mass by 7.59% relative to the previous 3.114 kg candidate, using the same safety assumptions.

| Parameter | Brief-load candidate | Larger transfer-moment candidate |
|---|---|---|
| Material | Magnesium AZ31B | Magnesium AZ31B |
| Length | 1500 mm | 1500 mm |
| Outer diameter | 158 mm | 212 mm |
| Nominal wall | 1.80 mm | 2.10 mm |
| Minimum analysed wall | 1.7100 mm | 1.9950 mm |
| Modelled assembly | 2.877525 kg | 4.423218 kg |
| Service bending moment | 2.198 kN m | 4.395 kN m |

## What carries the load

The barrel wall carries bending as compression on one side and tension on the other. The end joints transfer those forces. Rigid circular end rings preserve the end shape; K = 1 is used only for buckling.

## Selected connection

Each end has a 16.0 mm thick, 12.0 mm wide integral flange, with 36 x 4 mm Ti-6Al-4V bolts on a 146.0 mm bolt circle. Bolt properties and dimensions are a model specification, not a commercial fastener qualification.

## Scope and decision

The search covers seven supplied materials, diameters 40-300 mm, discrete wall thicknesses, integer bolt counts 8-64 and five flange widths. Composite results remain shell-only because connection and ply-level properties are missing. The selected metal is the minimum within the implemented family, not a proven optimum across all architectures.

The basis uses 1.5 times the service loads, 95% wall thickness, 1.5 mm initial bow and a provisional 0.35 shell/ovalisation reduction cap. Mass includes the shell, integral flanges, root bands and modelled fasteners; it excludes adjacent adapters, seals and coatings. Some margins are small. Long-shell, shear and joint approximations remain conditional.

Use the larger transfer candidate if the bottom section must carry M + V*L. See the complete report for the load-path distinction, calculations, margins, sensitivity and sources. No FEA or hardware testing was performed.
