# Drakkar Thrust Barrel: Structural Solution

Aircraft Structures R5ME3203T, VJTI Mumbai. Lockheed Martian.
Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).

## Selected design

Material: **Carbon/Epoxy QI**. Length: **1500 mm**. Outer diameter: **122.0 mm**. Uniform wall: **1.520 mm**. Shell mass: **1.380764654 kg**.

The same geometry passes the prescribed primary moment and the transfer moment M + V L under the supplied B-basis material properties. The governing check is local shell stability under the transfer load case. Selection minimises shell mass over the seven permitted homogeneous material families on a 1 mm diameter / 0.01 mm wall grid.

## Material data

| Material | E GPa | nu | Density kg/m3 | Yield / Xc MPa | Yt MPa | S MPa | k |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Aluminium 7075-T6 | 71.7 | 0.33 | 2810 | 402 | - | - | 0.4 |
| Titanium Ti-6Al-4V | 113.8 | 0.31 | 4430 | 704 | - | - | 0.4 |
| Steel 4130 | 205 | 0.29 | 7850 | 368 | - | - | 0.4 |
| Magnesium AZ31B | 45 | 0.35 | 1770 | 176 | - | - | 0.4 |
| Carbon/Epoxy QI | 52.3 | 0.3 | 1600 | 480 | 400 | 160 | 0.5 |
| Glass/Epoxy QI | 23.8 | 0.3 | 1900 | 240 | 200 | 80 | 0.5 |
| Aramid/Epoxy QI | 33.3 | 0.34 | 1400 | 160 | 240 | 64 | 0.5 |

Values follow the material-quality notice. Yield applies to metals; Xc, Yt and S apply to the effective-QI composites. Density and Poisson ratio follow the assignment. QI properties describe a homogeneous effective continuum; they do not specify a laminate stacking sequence.

## Acceptance results

| Check | Primary U | Primary MS % | Transfer U | Transfer MS % |
| --- | --- | --- | --- | --- |
| strength | 0.510507084 | +95.8837 | 0.863183224 | +15.8503 |
| Euler | 0.137777263 | +625.8092 | 0.137777263 | +625.8092 |
| local_shell | 0.567324043 | +76.2661 | 0.991014328 | +0.9067 |
| ovalisation | 0.384516385 | +160.0669 | 0.769032771 | +30.0335 |

U is demand/capacity and MS = 1/U - 1. All four U values are at most one, and the thin-shell and elastic-capacity gates pass. The proportional design load factor is 1.1. Numerical margins refer to that design load, not an additional nonlinear load multiplier.

The result covers the uniform shell with ideal simply supported rigid end rings. Ring and connection mass, manufactured laminate qualification, joint stiffness and nonlinear coupled global/local collapse are outside the supplied model. These are system-boundary exclusions, not zero-valued physical quantities.

<!-- PAGE -->
# Governing Equations and Applicability

Governing equations, admissible domain and numerical procedure.

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

The factor 1.1 is a declared design requirement, not a statistically derived material factor. Strength allowables are not divided by 1.1 a second time. Pressure-end thrust is not subtracted from compression in the design load case; a separate closed-end strength check is provided.

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

The notice prescribes k = 0.40 for B-basis metals and 0.50 for B-basis QI composites. No geometry-dependent NASA correlation is multiplied into these prescribed factors. The local axial classical relation is the lower continuous-wavenumber envelope used by the course shell model; a factor calibrated for one material population is not represented as experimental validation of this design.

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

Requiring U_QI <= 1 bounds every convex quadratic interaction having these normalised uniaxial limits. The sign-dependent criterion is maximised analytically on each axial-stress sign interval: it has the form A+B c+C sqrt(1-c^2). The QI equivalence treats in-plane tensile strength as direction-independent. No laminate stacking sequence, interlaminar strength or manufacturing qualification follows from this homogeneous model.

## 7. Optimisation and numerical resolution

The nominal search enumerates D = 1, 2, ..., 300 mm and walls at 0.01 mm increments. Each material is searched independently. Admissible upper wall is the smaller of D/21 and eta D/(2+eta), where eta = sigma_allow sqrt[3(1-nu^2)]/(k E). The latter enforces the elastic-capacity gate. Integer bisection locates the first feasible thickness within this domain; exhaustive sequential-search tests independently verify the search on representative diameters for every material and both load cases. The transfer-load sweep governs selection; the selected geometry is checked under both load cases. Nominal sweep minima are checked against the saved CSV file.

A complete second search at 0.1 mm diameter and 0.001 mm wall spacing quantifies discretisation effects. The nominal-grid solution, not the finer result, is used for the reported design dimensions. Neither grid defines stock availability or a wall-thickness tolerance. Acceptance requires every utilisation <= 1 and every applicability gate true.

Margins are MS = 1/U - 1. For nonlinear beam-column response, this is a capacity/demand utilisation margin at the specified design load; it is not an additional load factor obtained by scaling the complete nonlinear load path.

## 8. Design-space and mass boundary

The minimum is over the specified homogeneous, unstiffened shell family and discrete grids. All seven permitted effective material sets are included. No claim of a global minimum over all stiffened, sandwich or hybrid architectures is made. Such architectures require additional design variables and property data; the presence of a lower mass homogeneous QI candidate is reported rather than excluded from the optimisation.

```
m_assembly = m_shell + m_end_rings + m_connections + m_other_interfaces
```

The briefs prescribe ideal rigid end boundaries but no ring cross-sections, attachment geometry or interface mass budget. Reported masses therefore use shell mass. Interface contributions cannot be assigned numerical values from the supplied information. This is an explicit system-boundary exclusion, not a computational result equal to zero.

## 9. Sources and equation provenance

1. VJTI, *The Drakkar Ascent Challenge*, August 2026, sections 3-8: geometry, load derivation, boundary conditions, material data and scoring.
2. Guild Assay Office, *Tweak to Drakkar Ascent*, 3 October 2026, sections 2-5: revised material properties, prescribed knockdowns and response requirements.
3. NASA/SP-8007-2020/REV 2, *Buckling of Thin-Walled Circular Cylinders*, equations 7 and 16 and section 4.1.1: reference axial-shell and ovalisation expressions; printed page 25 identifies long-cylinder/global-local and plasticity limitations. https://ntrs.nasa.gov/citations/20205011530
4. The pressure-supported completion-of-square bound and PSD composite interaction bound are derived in sections 4 and 6 of this document. They are not represented as empirical correlations from source 3.

<!-- PAGE -->
# Numerical Evaluation and Verification

## Selected geometry under both load cases

### Primary load case

```
D = 122.000000 mm; t = 1.520000 mm
A = 575.318606015 mm^2; I = 1044040.799942592 mm^4
P = 33000.000000 N; p = 0.330000 MPa
M_first = 2417.463166173 N m; M_max = 2895.910499680 N m
V_external = 1611.642110782 N; V_secondary = 1239.508869784 N
P_Euler = 239517.023978570 N
P/A = 57.359521585 MPa; M r_o/I = 169.198886184 MPa
Peak shear = 9.911554922 MPa
Hoop tension lower bound = 12.913421053 MPa
C_eff = 226.558407769 MPa
sigma_cr = 399.345683408 MPa
Normal allowable = 400.000000000 MPa
C_eff maximum angle = 180.000000 deg
M_Brazier = 7531.305842865 N m
```

### Transfer load case

```
D = 122.000000 mm; t = 1.520000 mm
A = 575.318606015 mm^2; I = 1044040.799942592 mm^4
P = 33000.000000 N; p = 0.330000 MPa
M_first = 4834.926332346 N m; M_max = 5791.820999360 N m
V_external = 1611.642110782 N; V_secondary = 2479.017739568 N
P_Euler = 239517.023978570 N
P/A = 57.359521585 MPa; M r_o/I = 338.397772367 MPa
Peak shear = 14.220502544 MPa
Hoop tension lower bound = 12.913421053 MPa
C_eff = 395.757293952 MPa
sigma_cr = 399.345683408 MPa
Normal allowable = 400.000000000 MPa
C_eff maximum angle = 180.000000 deg
M_Brazier = 7531.305842865 N m
```

## Search convergence

The transfer-load search contains 1033 feasible material/diameter pairs. A refined grid of 0.1 mm diameter and 0.001 mm wall checks numerical resolution. The largest nominal-grid mass excess over the refined material minimum is 0.968000%. The selected dimensions remain those of the declared nominal grid. The search record in `data/trade_study.csv` and the refinement data in `data/solution.json` support this single design selection; they are not additional design submissions.

## Gust and thickness sensitivity

| Load case | Gust m/s | Local U | Strength U | Pass |
| --- | --- | --- | --- | --- |
| primary | 20 | 0.567324 | 0.510507 | PASS |
| primary | 22 | 0.609370 | 0.546024 | PASS |
| primary | 24 | 0.651325 | 0.581464 | PASS |
| transfer | 20 | 0.991014 | 0.863183 | PASS |
| transfer | 22 | 1.075106 | 0.933699 | FAIL |
| transfer | 24 | 1.159016 | 1.004062 | FAIL |

At fixed selected geometry the calculated transfer-case gust boundary is 20.213515 m/s. At the specified 20 m/s gust, the minimum actual wall is 1.513594 mm; the difference from nominal wall is 0.006406 mm. These are model acceptance boundaries, not prescribed production tolerances. Only the aerodynamic loading changes with gust; thrust and internal pressure remain fixed.

Closed-end thrust is checked as a strength sensitivity using the same geometry. Primary and transfer strength utilisations are 0.497225310 and 0.849901450, respectively. The main stability calculation does not credit axial pressure-thrust relief.

## Independent numerical verification

An independent implementation in N, mm and MPa verifies 22 calculation records, including material-search minima, refinement results, both selected-geometry load cases and gust scenarios. It imports no analysis functions. A 12001-point circumferential scan checks the analytical stress maxima; a 2000-term Fourier series checks the beam-column moment. Maximum absolute utilisation discrepancy is 3.447700681e-09; maximum relative Fourier moment discrepancy is 1.155076035e-12. Saved nominal material minima also match the full CSV sweep.

The unit suite checks energy and composite-interaction inequalities, analytical extrema, beam response, material properties, gust isolation, elastic-domain rejection, bisection against direct enumeration and saved-design consistency. Agreement verifies the stated equations and implementation; it does not constitute experimental validation.

## Reproduction

Python >= 3.10. The calculation and verification require only the standard library. Report generation requires the dependency in `requirements.txt`.

```sh
python3 src/solve.py
python3 src/verify.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
.venv/bin/python src/report.py
```

The report is generated from the numerical dataset. A SHA-256 check prevents report generation from using a verification record for different solution data.
