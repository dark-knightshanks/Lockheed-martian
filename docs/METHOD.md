# Analytical Method Specification

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
