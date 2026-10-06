# Drakkar Thrust Barrel: Technical Analysis

DRA-TR-C | Revision C | 6 October 2026

Aircraft Structures R5ME3203T, VJTI Mumbai. Cadre: Lockheed Martian. Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).

## Executive technical finding

The adopted dual-case solution is the supplied effective-QI carbon/epoxy material, outer diameter 122.0 mm, nominal wall 1.520 mm, length 1500 mm, shell mass 1.380765 kg. Case B local utilisation is 0.991014328. Its case-A margins are also positive. The lower mass case-A-only solution is 1.016443 kg. A homogeneous metal alternative for both cases is Magnesium AZ31B, 194.0 x 1.420 mm, 2.280940 kg.

Acceptance is defined by the mathematical checks and applicability gates in DRA-MTH-C. Ring/connection masses and manufactured laminate qualification are excluded quantities, not zero-valued results. The original clean-material dataset is maintained as Revision A; it is not the current B-basis design.

## Revised material-property register

| Material | E GPa | nu | rho kg/m3 | Yield / Xc MPa | Yt MPa | S MPa | k |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Aluminium 7075-T6 | 71.7 | 0.33 | 2810 | 402 | - | - | 0.4 |
| Titanium Ti-6Al-4V | 113.8 | 0.31 | 4430 | 704 | - | - | 0.4 |
| Steel 4130 | 205 | 0.29 | 7850 | 368 | - | - | 0.4 |
| Magnesium AZ31B | 45 | 0.35 | 1770 | 176 | - | - | 0.4 |
| Carbon/Epoxy QI | 52.3 | 0.3 | 1600 | 480 | 400 | 160 | 0.5 |
| Glass/Epoxy QI | 23.8 | 0.3 | 1900 | 240 | 200 | 80 | 0.5 |
| Aramid/Epoxy QI | 33.3 | 0.34 | 1400 | 160 | 240 | 64 | 0.5 |

The supplied density and Poisson ratios are unchanged. Exact tabulated B-basis stiffnesses and strengths are used. QI modulus is an effective homogeneous property; no constituent fibre or resin properties are inferred.

## Requirements traceability

| Requirement | Implementation / evidence |
| --- | --- |
| Length / OD | L = 1.5 m; OD <= 0.3 m; every enumerated candidate checked |
| All revised properties | Seven exact B-basis property sets; material-data regression test |
| Strength | Circumferential von Mises or conservative PSD quadratic QI envelope |
| Column stability | P < Euler capacity; secant moment and secondary shear included |
| Local shell stability | Pressure-supported geometric-energy bound / prescribed k axial capacity |
| No FEA | Closed-form mechanics, integer enumeration and analytic beam series |
| Minimum-mass modification | All seven homogeneous materials; nominal and refined complete OD sweeps |
| Margins and verdict | All four utilisation ratios and signed margins saved per design |
| Sensitivity | Fixed geometry, matched model, quality A/B and gust 20/22/24 m/s |
| Two-page supplement | Guild_Assay_Response.pdf, generated from the same result data |

<!-- PAGE -->
## Governing equations and applicability

Document DRA-MTH-C | Revision C | 6 October 2026

## 1. Scope, coordinates and units

The component is a homogeneous circular cylindrical shell of length L = 1.5 m and outer diameter D <= 0.300 m. The prescribed end rings are ideal circular, rigid, simply supported boundaries. The design variables are material, D and uniform wall thickness t. The model uses SI units; the independent verifier uses N, mm and MPa. The effective quasi-isotropic (QI) composite model is a homogeneous continuum using the assignment's supplied E, nu and strength allowables. It is not a ply-resolved laminate model.

Coordinates: x is axial; theta is circumferential; s = r theta; r = (D-t)/2 is the wall midsurface radius. Compression is positive in the stability calculation and tension is positive in the material-failure calculation. The admitted thin-shell domain is 10 <= r/t < 1500.

## 2. Loads and section properties

```
q = rho_air U^2/2
alpha = atan(w_g/U)
f = q C_Nalpha alpha D_u
V = f L_u
M_A = f L_u^2/2
M_B = M_A + V L
P_service = 30000 N; p_service = 300000 Pa
P, V, M_0, p = 1.1 times the corresponding service values
r_o = D/2; r_i = r_o-t
A = pi (r_o^2-r_i^2)
I = pi (r_o^4-r_i^4)/4
m_shell = rho_material A L
```

Inputs are rho_air = 1.225 kg/m3, U = 200 m/s, w_g = 20 m/s, C_Nalpha = 2 rad^-1, D_u = 0.10 m and L_u = 3 m. Case A applies the assignment's stated moment at the barrel. Case B includes the additional moment V L when the upper interface shear is transferred through the barrel without an intermediate lateral reaction. The recommended design is checked under both cases; their results are not mixed.

The factor 1.1 is a declared design requirement, not a statistically derived material factor. Strength allowables are not divided by 1.1 a second time. Pressure-end thrust is not subtracted from compression in the baseline; a separate closed-end strength check is provided.

## 3. Beam-column moment and shear envelope

```
P_E = pi^2 E I/L^2
beta = (L/2) sqrt(P/(E I))
M_max = M_0 sec(beta), valid only for P < P_E
V_secondary = M_0 sqrt(P/(E I)) tan(beta)
V_bound = V + V_secondary
```

A uniform first-order moment equal to the maximum end-moment magnitude is used as a majorant of the same-sign moment diagram. The equal-end-moment pinned beam-column solution supplies M_max. The end-slope term gives a conservative additional shear contribution; the external and secondary shear magnitudes are added. This is an envelope, not an assertion that the physical first-order diagram is constant while carrying nonzero shear. The independent verifier compares the moment with a 2,000-term sine-series solution of EI y'' + P y = -M_0.

## 4. Transverse shear without a torsional capacity substitution

The wall stress envelopes are

```
a = P/A; b = M_max r_o/I; s_0 = V_bound/(pi r t)
h = p r_i/t > 0
C(theta) = a-b cos(theta)
T(theta) = s_0 sin(theta)
```

For local radial perturbation w, the destabilising membrane term in the Donnell local-shell geometric energy is proportional to

```
C w_x^2 + 2 T w_x w_s - h w_s^2
= (C+T^2/h) w_x^2 - h (w_s-T w_x/h)^2
<= (C+T^2/h) w_x^2.
```

Consequently a uniform axial-compression majorant for this local-shell model is

```
C_eff = max_{-1 <= c <= 1} [a-b c + (s_0^2/h)(1-c^2)].
```

Evaluate the quadratic at c = -1, +1 and its stationary point when it lies in the interval. This inequality handles the co-located transverse shear and hoop tension directly. It does not use a torsional buckling stress or assign a shear knockdown factor. The smaller inner-radius hoop stress is used to avoid overstating membrane-tension support. The bound requires the specified positive operating pressure: it is not a depressurised-load qualification.

The inequality is a sufficient majorisation within the stated local Donnell energy model. It is not a proof of finite-amplitude shell collapse, pressure-follower effects, or coupled global/local instability in a geometrically imperfect manufactured structure. Those phenomena are outside the supplied course model. Global beam-column and cross-section ovalisation checks are retained independently.

## 5. Local capacity, elastic domain and stability checks

```
sigma_cl = E (t/r)/sqrt[3(1-nu^2)]
sigma_cr = k sigma_cl
U_local = C_eff/sigma_cr
U_Euler = P/P_E
M_Brazier = 0.987 E r t^2/sqrt(1-nu^2)
U_ovalisation = M_max/M_Brazier
```

The notice prescribes k = 0.40 for B-basis metals and 0.50 for B-basis QI composites. For the matched clean-material comparison use k = 0.50 and 0.65 respectively. No geometry-dependent NASA correlation is multiplied into these prescribed factors. The local axial classical relation is the lower continuous-wavenumber envelope used by the course shell model; a factor calibrated for one material population is not represented as experimental validation of this design.

An elastic buckling capacity must not exceed the metal yield allowable, or the smaller QI normal allowable. A candidate outside this domain is rejected; it is not accepted by clipping a predicted elastic capacity to a strength value. This eliminates yield-capped candidates from the design search. It does not substitute for proportional-limit or tangent-modulus data in a physical elastic-plastic analysis. Ideal unpressurised Brazier capacity is checked without pressure-stabilisation credit.

## 6. Co-located material failure

For metals, maximise the following over the circumference:

```
sigma_x = -P/A + (M_max r_o/I) cos(theta)
sigma_h = p r_o/t
tau = [V_bound/(pi r t)] sin(theta)
U_VM = sqrt(sigma_x^2 + sigma_h^2 - sigma_x sigma_h + 3 tau^2)/sigma_y.
```

The outer-radius hoop stress upper-bounds the membrane stress for the strength calculation. For closed-end strength sensitivity only, add p pi r_i^2/A to sigma_x. The exact extremum follows from a quadratic in cos(theta).

For QI composites, the supplied uniaxial allowables do not uniquely determine quadratic cross terms. Let z contain the three stresses normalised by the relevant uniaxial allowables, and let the normalised quadratic interaction matrix Q be positive semidefinite with unit diagonal. Its entries satisfy |Q_ij| <= 1, hence

```
FI = z^T Q z <= (|z_1|+|z_2|+|z_3|)^2
U_QI = |sigma_x|/X_sign + sigma_h/Y_t + |tau|/S
X_sign = X_c in axial compression, Y_t in axial tension.
```

Requiring U_QI <= 1 bounds every convex quadratic interaction having these normalised uniaxial limits. This replaces the special choice Q = identity. The sign-dependent criterion is maximised analytically on each axial-stress sign interval: it has the form A+B c+C sqrt(1-c^2). The QI equivalence treats in-plane tensile strength as direction-independent. No laminate stacking sequence, interlaminar strength or manufacturing qualification follows from this homogeneous model.

## 7. Optimisation and numerical resolution

The nominal search enumerates D = 1, 2, ..., 300 mm and walls at 0.01 mm increments. Each material is searched independently. Admissible upper wall is the smaller of D/21 and eta D/(2+eta), where eta = sigma_allow sqrt[3(1-nu^2)]/(k E). The latter enforces the elastic-capacity gate. Integer bisection locates the first feasible thickness within this domain; exhaustive sequential-search tests independently verify the search on representative diameters for every material and both load cases. All nominal sweep minima are checked against the saved CSV files.

A complete second search at 0.1 mm diameter and 0.001 mm wall spacing quantifies discretisation effects. The nominal-grid solution, not the finer result, is used for the reported design dimensions. Neither grid defines stock availability or a wall-thickness tolerance. Acceptance requires every utilisation <= 1 and every applicability gate true.

Margins are MS = 1/U - 1. For nonlinear beam-column response, this is a capacity/demand utilisation margin at the specified design load; it is not an additional load factor obtained by scaling the complete nonlinear load path.

## 8. Design-space and mass boundary

The minimum is over the specified homogeneous, unstiffened shell family and discrete grids. All seven permitted effective material sets are included. No claim of a global minimum over all stiffened, sandwich or hybrid architectures is made. Such architectures require additional design variables and property data; the presence of a lower mass homogeneous QI candidate is reported rather than excluded from the optimisation.

```
m_assembly = m_shell + m_end_rings + m_connections + m_other_interfaces
Delta m_assembly = Delta m_shell + Delta m_interfaces
```

The briefs prescribe ideal rigid end boundaries but no ring cross-sections, attachment geometry or interface mass budget. Reported masses and score calculations therefore use shell mass. Interface contributions cannot be assigned numerical values from the supplied information. This is an explicit system-boundary exclusion, not a computational result equal to zero.

## 9. Sources and equation provenance

1. VJTI, *The Drakkar Ascent Challenge*, August 2026, sections 3-8: geometry, load derivation, boundary conditions, material data and scoring.
2. Guild Assay Office, *Tweak to Drakkar Ascent*, 3 October 2026, sections 2-5: revised material properties, prescribed knockdowns and response requirements.
3. NASA/SP-8007-2020/REV 2, *Buckling of Thin-Walled Circular Cylinders*, equations 7 and 16 and section 4.1.1: reference axial-shell and ovalisation expressions; printed page 25 identifies long-cylinder/global-local and plasticity limitations. https://ntrs.nasa.gov/citations/20205011530
4. The pressure-supported completion-of-square bound and PSD composite interaction bound are derived in sections 4 and 6 of this document. They are not represented as empirical correlations from source 3.

The previously used NASA torsional capacity is not a transverse-shear formula and is absent from Revision C acceptance calculations. The online Air Force interaction-table transcription is not used as a normative equation source.

<!-- PAGE -->
# Results and numerical verification

## Primary load case: all-material optimisation

| Material | D mm | t mm | Mass kg | Governing | Margin % | Refined kg |
| --- | --- | --- | --- | --- | --- | --- |
| Aluminium 7075-T6 | 106.0 | 1.190 | 1.651571 | strength | 0.1437 | 1.645288 |
| Titanium Ti-6Al-4V | 86.0 | 1.070 | 1.897098 | local_shell | 0.5457 | 1.893116 |
| Steel 4130 | 162.0 | 0.560 | 3.344336 | strength | 0.8718 | 3.320301 |
| Magnesium AZ31B | 164.0 | 1.200 | 1.629484 | strength | 0.9024 | 1.619450 |
| Carbon/Epoxy QI | 105.0 | 1.300 | 1.016443 | local_shell | 0.5974 | 1.013079 |
| Glass/Epoxy QI | 129.0 | 1.750 | 1.993841 | local_shell | 0.7918 | 1.983086 |
| Aramid/Epoxy QI | 176.0 | 1.220 | 1.406762 | strength | 0.0488 | 1.406422 |

The original 119.0 x 0.960 mm aluminium geometry has B-basis local margin -25.55%. The fixed-diameter aluminium repair is 119.0 x 1.110 mm, 1.732796 kg.

## Transfer load case: all-material optimisation

| Material | D mm | t mm | Mass kg | Governing | Margin % | Refined kg |
| --- | --- | --- | --- | --- | --- | --- |
| Aluminium 7075-T6 | 125.0 | 1.400 | 2.291363 | strength | 0.5480 | 2.278641 |
| Titanium Ti-6Al-4V | 101.0 | 1.250 | 2.602962 | local_shell | 1.4753 | 2.578007 |
| Steel 4130 | 192.0 | 0.670 | 4.742078 | strength | 0.5284 | 4.709873 |
| Magnesium AZ31B | 194.0 | 1.420 | 2.280940 | strength | 0.6308 | 2.271429 |
| Carbon/Epoxy QI | 122.0 | 1.520 | 1.380765 | local_shell | 0.9067 | 1.373499 |
| Glass/Epoxy QI | 150.0 | 2.040 | 2.702522 | local_shell | 0.0490 | 2.698068 |
| Aramid/Epoxy QI | 208.0 | 1.440 | 1.962356 | local_shell | 0.2811 | 1.954598 |

The original 137.0 x 1.100 mm aluminium geometry has B-basis local margin -31.77%. The fixed-diameter aluminium repair is 137.0 x 1.330 mm, 2.389367 kg.

## Selected dual-case design: substituted quantities

### Case A

```
D = 122.000000 mm; t = 1.520000 mm
r_o = 61.000000 mm; r_i = 59.480000 mm
A = 575.318606015 mm^2; I = 1044040.799942592 mm^4
M_0 = 2417.463166173 N m; M_max = 2895.910499680 N m
V_external = 1611.642110782 N; V_secondary = 1239.508869784 N
P_E = 239517.023978570 N
P/A = 57.359521585 MPa
M r_o/I = 169.198886184 MPa
Peak shear bound = 9.911554922 MPa
Hoop tension lower bound = 12.913421053 MPa
C_eff = 226.558407769 MPa
sigma_cr = 399.345683408 MPa
QI normal-domain bound = 400.000000000 MPa
C_eff maximum angle = 180.000000 deg
M_Brazier = 7531.305842865 N m
```

| Check | Utilisation | Margin % |
| --- | --- | --- |
| strength | 0.510507084 | 95.883668 |
| Euler | 0.137777263 | 625.809164 |
| local_shell | 0.567324043 | 76.266106 |
| ovalisation | 0.384516385 | 160.066941 |
### Case B

```
D = 122.000000 mm; t = 1.520000 mm
r_o = 61.000000 mm; r_i = 59.480000 mm
A = 575.318606015 mm^2; I = 1044040.799942592 mm^4
M_0 = 4834.926332346 N m; M_max = 5791.820999360 N m
V_external = 1611.642110782 N; V_secondary = 2479.017739568 N
P_E = 239517.023978570 N
P/A = 57.359521585 MPa
M r_o/I = 338.397772367 MPa
Peak shear bound = 14.220502544 MPa
Hoop tension lower bound = 12.913421053 MPa
C_eff = 395.757293952 MPa
sigma_cr = 399.345683408 MPa
QI normal-domain bound = 400.000000000 MPa
C_eff maximum angle = 180.000000 deg
M_Brazier = 7531.305842865 N m
```

| Check | Utilisation | Margin % |
| --- | --- | --- |
| strength | 0.863183224 | 15.850259 |
| Euler | 0.137777263 | 625.809164 |
| local_shell | 0.991014328 | 0.906715 |
| ovalisation | 0.769032771 | 30.033470 |

## Independent verification record

Verification uses different units and independent geometry identities, 12,001 circumferential samples, and a 2,000-term sine series. 30 nominal/refined/original cases pass the arithmetic comparison; maximum absolute utilisation difference is 4.083359e-09, and maximum relative beam-moment difference is 1.791456e-12. Every nominal material minimum agrees with the saved diameter sweep.

| Case | Feasible D/material pairs | Maximum nominal/fine mass excess % |
| --- | --- | --- |
| primary | 1194 | 0.723901 |
| transfer | 1033 | 0.968000 |

## Wall-thickness and gust boundaries

| Case | Design | Minimum actual t mm | Allowable wall loss mm | Gust boundary m/s |
| --- | --- | --- | --- | --- |
| primary | selected | 1.296620 | 0.003380 | 20.149901 |
| primary | metal | 1.194672 | 0.005328 | 20.277740 |
| transfer | selected | 1.513594 | 0.006406 | 20.213515 |
| transfer | metal | 1.415407 | 0.004593 | 20.173897 |

These are computed acceptance boundaries of the stated model at fixed geometry and material. They are not prescribed production tolerances or certification gust envelopes.

## Fixed-geometry sensitivity record

| Case | Geometry | Quality | Gust m/s | Local U | Strength U | Status |
| --- | --- | --- | --- | --- | --- | --- |
| primary | original | A | 20 | 1.074556 | 0.783024 | FAIL |
| primary | original | A | 22 | 1.155400 | 0.840291 | FAIL |
| primary | original | A | 24 | 1.236067 | 0.897441 | FAIL |
| primary | original | B | 20 | 1.343195 | 0.979754 | FAIL |
| primary | original | B | 22 | 1.444249 | 1.051409 | FAIL |
| primary | original | B | 24 | 1.545084 | 1.122917 | FAIL |
| primary | selected | A | 20 | 0.715913 | 0.682566 | OUTSIDE DOMAIN |
| primary | selected | A | 22 | 0.772704 | 0.734770 | OUTSIDE DOMAIN |
| primary | selected | A | 24 | 0.829373 | 0.786860 | OUTSIDE DOMAIN |
| primary | selected | B | 20 | 0.994061 | 0.866527 | PASS |
| primary | selected | B | 22 | 1.073223 | 0.933104 | FAIL |
| primary | selected | B | 24 | 1.152213 | 0.999536 | FAIL |
| primary | metal | A | 20 | 0.792694 | 0.792846 | PASS |
| primary | metal | A | 22 | 0.845258 | 0.841402 | PASS |
| primary | metal | A | 24 | 0.897709 | 0.889884 | PASS |
| primary | metal | B | 20 | 0.990867 | 0.991057 | PASS |
| primary | metal | B | 22 | 1.056573 | 1.051752 | FAIL |
| primary | metal | B | 24 | 1.122136 | 1.112355 | FAIL |
| transfer | original | A | 20 | 1.172561 | 0.848604 | FAIL |
| transfer | original | A | 22 | 1.269277 | 0.916799 | FAIL |
| transfer | original | A | 24 | 1.365784 | 0.984854 | FAIL |
| transfer | original | B | 20 | 1.465701 | 1.061811 | FAIL |
| transfer | original | B | 22 | 1.586597 | 1.147139 | FAIL |
| transfer | original | B | 24 | 1.707230 | 1.232292 | FAIL |
| transfer | selected | A | 20 | 0.719092 | 0.685011 | OUTSIDE DOMAIN |
| transfer | selected | A | 22 | 0.780026 | 0.740875 | OUTSIDE DOMAIN |
| transfer | selected | A | 24 | 0.840829 | 0.796617 | OUTSIDE DOMAIN |
| transfer | selected | B | 20 | 0.991014 | 0.863183 | PASS |
| transfer | selected | B | 22 | 1.075106 | 0.933699 | FAIL |
| transfer | selected | B | 24 | 1.159016 | 1.004062 | FAIL |
| transfer | metal | A | 20 | 0.794758 | 0.794985 | PASS |
| transfer | metal | A | 22 | 0.854988 | 0.850646 | PASS |
| transfer | metal | A | 24 | 0.915088 | 0.906227 | PASS |
| transfer | metal | B | 20 | 0.993448 | 0.993731 | PASS |
| transfer | metal | B | 22 | 1.068736 | 1.063308 | FAIL |
| transfer | metal | B | 24 | 1.143860 | 1.132784 | FAIL |

## Closed-end pressure sensitivity

| Case | Material | Closed-end strength U | Wall-only strength U |
| --- | --- | --- | --- |
| primary | Carbon/Epoxy QI | 0.853159 | 0.866527 |
| primary | Magnesium AZ31B | 0.928818 | 0.991057 |
| transfer | Carbon/Epoxy QI | 0.849901 | 0.863183 |
| transfer | Magnesium AZ31B | 0.931511 | 0.993731 |

## Reproduction and deliverable control

Run from the repository root with Python >= 3.10:

```sh
python3 src/guild_assay.py
python3 src/verify_revised.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
.venv/bin/python src/generate_assay_response.py
```

The first command regenerates both full diameter sweeps, material optima, matched clean comparisons, refinement, pressure and gust checks. Verification produces data/guild_assay/verification.json. The report generator obtains every reported result from the JSON datasets; it contains no independently maintained design-result constants. The original Revision A report, presentation and dataset remain separately labelled reference records.
