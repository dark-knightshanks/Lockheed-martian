# Guild Assay Response

DRA-GAR-C | Lockheed Martian, VJTI | 6 October 2026

## 1. Material properties and analysis basis

| Material | E GPa | nu | Density kg/m3 | Strength MPa | k |
| --- | --- | --- | --- | --- | --- |
| 7075-T6 | 71.7 | 0.33 | 2810 | Yield 402 | 0.4 |
| Carbon/epoxy QI | 52.3 | 0.3 | 1600 | Xc 480; Yt 400; S 160 | 0.5 |

L = 1500 mm; D <= 300 mm; load factor = 1.1. Design P = 33.0 kN, V = 1.611642 kN and p = 0.330 MPa. Case A first-order moment is 2.417463 kN m; case B is M + VL = 4.834926 kN m. Beam-column moment and secondary shear are included. The selected 122.0 mm OD x 1.520 mm effective-QI shell passes both cases in the specified analytical model.

Local stability uses sigma_cr = k E(t/r)/sqrt[3(1-nu^2)]. Transverse shear is bounded by the local geometric-energy identity C wx^2 + 2 T wx ws - h ws^2 <= (C + T^2/h) wx^2, h > 0. The circumference maximum C_eff is compared with sigma_cr. No torsional capacity or shear knockdown is substituted. The pressure-supported bound is restricted to the specified pressurised operating state.

Metal strength uses von Mises. QI strength uses the conservative quadratic envelope FI <= (abs(sigma_x)/X_sign + sigma_h/Yt + abs(tau)/S)^2; this bounds all positive-semidefinite quadratic interactions with the supplied uniaxial limits. The QI continuum is an assignment-level effective material, not a qualified ply schedule. Elastic capacities above the material normal allowable are rejected, not capped.

## 2. Numerical margins and verdict

| Mode | Original Al, case A | QI design, case A | QI design, case B |
| --- | --- | --- | --- |
| Material failure | +2.07% | +95.88% | +15.85% |
| Euler | +490.98% | +625.81% | +625.81% |
| Local shell | -25.55% | +76.27% | +0.91% |
| Ovalisation | +34.67% | +160.07% | +30.03% |

MS = 1/U - 1. Original geometry: aluminium 7075-T6, 119 x 0.960 mm, 1.500541 kg. **Original verdict: FAIL**, governing local margin -25.55%. **Revised verdict: PASS within the stated homogeneous-shell model**, governing local margin +0.91% in case B. Ideal end-ring and connection masses are outside the calculated shell mass.

## 3. Minimum-mass fix

The minimum nominal-grid shell for case A is carbon/epoxy QI, 105.0 x 1.300 mm, 1.016443 kg. The recommended design also covers case B: carbon/epoxy QI, 122.0 x 1.520 mm, **1.380765 kg**. Relative to the original 1.500541 kg shell, Delta m = **-0.119776 kg (-7.98%)**. All seven material sets were searched, using 1 mm OD and 0.01 mm wall increments. The refined 0.1/0.001 mm search provides the numerical-resolution comparison on page 2.

<!-- PAGE -->
# Guild Assay Response - continued

## 4. Design-space comparison and refinement

| Alternative | OD x wall mm | Shell mass kg | Application |
| --- | --- | --- | --- |
| QI minimum, A | 105.0 x 1.300 | 1.016443 | Case A only |
| QI selected, A+B | 122.0 x 1.520 | 1.380765 | Both cases |
| Metal minimum, A+B | 194.0 x 1.420 | 2.280940 | Magnesium AZ31B |

The refined case-B QI result is 121.6 x 1.517 mm and 1.373499 kg. Nominal-grid minima exceed refined minima by no more than 0.968% across both cases and all materials. The minimum is confined to homogeneous unstiffened shells; ring-stiffened, sandwich and hybrid assembly optima are not claimed.

## 5. Failure-mode declaration and matched comparison

Local shell buckling governs the original design under both matched clean and degraded inputs and governs the selected QI solution; the governing class is unchanged. Under the same Revision C equations, the original clean-material local margin is -6.94%; the degraded margin is -25.55%. The archived original calculation used a different interaction model, so its reported +0.38% margin is not used as the clean endpoint of a material-only comparison.

## 6. Material quality versus gust sensitivity

At fixed original geometry and the same equations, clean-to-B-basis degradation changes local U from 1.074556 to 1.343195 (+25.00%). With B-basis properties fixed, gust 20 to 22 m/s changes U to 1.444249 (+7.52%); 24 m/s gives 1.545084 (+15.03%). Only aerodynamic loads change with atan(w_g/200); thrust and pressure are fixed. For these perturbations, material degradation has the larger effect. The selected case-B design's calculated gust boundary is 20.2135 m/s and minimum actual wall is 1.513594 mm; nominal wall dimensions are not manufacturing tolerances.

## 7. Verification, score and scope

Independent N/mm/MPa calculations verify 30 cases; 12,001-point angular scans differ from the analytic utilisations by at most 4.083e-09. Fourier beam-column verification differs by at most 1.791e-12. Tests cover energy inequalities, composite interaction bounds, material data, bisection against enumeration and saved sweep minima.

The original fails, then the shell fix has Delta m <= 10%; the shell-only material-integrity bracket is M_i = 0.7. The unchanged governing-mode declaration is provided for H_i assessment. Total = 100(0.35 S_i + 0.15 M_i + 0.10 H_i + 0.25 R_i + 0.10 T_i + 0.05 I_i); total score needs competition/assessment inputs. Shell-to-assembly mass conversion needs ring and connection masses.

Basis: VJTI challenge sections 3-8; Guild Assay notice sections 2-5; NASA SP-8007 Rev. 2 equations 7 and 16. Derivations and applicability boundaries: DRA-MTH-C, sections 3-8. Separate global beam and local-shell checks do not establish nonlinear global/local collapse or manufactured laminate qualification; these are outside the defined analytical acceptance scope.
