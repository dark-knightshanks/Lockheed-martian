# Drakkar Ascent - design review notes

## Objective and requirements

1500 mm barrel, OD <= 300 mm; supplied loads and seven materials. K = 1 for buckling; shell and joints still transfer bending. No FEA.

## Corrected basis

Use service loads and nominal thickness. Remove arbitrary 1.5 load factor, 5% wall loss, 1.5 mm bow and 0.35 caps. Retain required geometric shell knockdowns. Required safety factors are unspecified.

## Current material screens

| Material | OD (mm) | Wall (mm) | Shell mass (kg) | Status |
| --- | --- | --- | --- | --- |
| Aluminium 7075-T6 | 115 | 0.93 | 1.404759 | metal shell screen |
| Titanium Ti-6Al-4V | 94 | 0.81 | 1.575793 | metal shell screen |
| Steel 4130 | 151 | 0.55 | 3.061016 | metal shell screen |
| Magnesium AZ31B | 165 | 1.05 | 1.435870 | metal shell screen |
| Carbon/Epoxy QI | 98 | 1.16 | 0.846981 | equivalent-QI screen |
| Glass/Epoxy QI | 121 | 1.55 | 1.657725 | equivalent-QI screen |
| Aramid/Epoxy QI | 164 | 1.18 | 1.267532 | equivalent-QI screen |

## What the result means

The smallest screened metal shell is Aluminium 7075-T6, 1.404759 kg. ALL rows are shell-only. Connections, manufacturing qualification and required safety factors remain unresolved. The old 2.878 kg assembly is from a different assumed basis and is not the current result.

## Evidence and limitations

See the full report for equations, pressure treatment, composite interaction assumptions, long-shell extrapolation and all-material scenario results. A numerical screen is not a passing competition entry. Rings and joints need a defined design before total structural mass can be ranked.
