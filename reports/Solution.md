# Drakkar Thrust Barrel: Structural Solution

Aircraft Structures R5ME3203T, VJTI Mumbai. Lockheed Martian.
Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).

## Selected design

Material: **Carbon/Epoxy QI**. Length: **1500 mm**. Outer diameter: **122.0 mm**. Uniform wall: **1.520 mm**. Shell mass: **1.380764654 kg**.

The same geometry passes the prescribed primary moment and the transfer moment $M+VL$ under the supplied B-basis material properties. The governing check is local shell stability under the transfer load case. Selection minimises shell mass over the seven permitted homogeneous material families on a 1 mm diameter / 0.01 mm wall grid.

## Material data

| Material | $E$ / GPa | $\nu$ | $\rho$ / kg m$^{-3}$ | $\sigma_y$ / $X_c$ / MPa | $Y_t$ / MPa | $S$ / MPa | $k$ |
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

$U$ is demand/capacity and $\mathrm{MS}=1/U-1$. All four U values are at most one, and the thin-shell and elastic-capacity gates pass. The proportional design load factor is 1.1. Numerical margins refer to that design load, not an additional nonlinear load multiplier.

The result covers the uniform shell with ideal simply supported rigid end rings. Ring and connection mass, manufactured laminate qualification, joint stiffness and nonlinear coupled global/local collapse are outside the supplied model. These are system-boundary exclusions, not zero-valued physical quantities.

<!-- PAGE -->
# Governing Equations and Applicability

Governing equations, admissible domain and numerical procedure.

## 1. Scope, coordinates and units

The component is a homogeneous circular cylindrical shell of length $L=1.5\ \mathrm{m}$ and outer diameter $D\leq0.300\ \mathrm{m}$. The prescribed end rings are ideal circular, rigid, simply supported boundaries. The design variables are material, D and uniform wall thickness t. The model uses SI units; the independent verifier uses N, mm and MPa. The effective quasi-isotropic (QI) composite model is a homogeneous continuum using the assignment's supplied E, nu and strength allowables. It is not a ply-resolved laminate model.

Coordinates: $x$ is axial; $\theta$ is circumferential; $s=r\theta$; $r=(D-t)/2$ is the wall midsurface radius. Compression is positive in the stability calculation and tension is positive in the material-failure calculation. The admitted thin-shell domain is $10\leq r/t<1500$.

## 2. Loads and section properties

$$
q=\frac{1}{2}\rho_{\mathrm{air}}U^2,\qquad \alpha=\tan^{-1}\!\left(\frac{w_g}{U}\right)
$$

$$
f=qC_{N\alpha}\alpha D_u,\qquad V=fL_u
$$

$$
M_A=\frac{fL_u^2}{2},\qquad M_B=M_A+VL
$$

$$
P_{\mathrm{service}}=30\,000\ \mathrm{N},\qquad p_{\mathrm{service}}=300\,000\ \mathrm{Pa}
$$

$$
(P,V,M_0,p)=1.1\,(P,V,M_0,p)_{\mathrm{service}}
$$

$$
r_o=\frac{D}{2},\qquad r_i=r_o-t,\qquad r=\frac{r_o+r_i}{2}
$$

$$
A=\pi(r_o^2-r_i^2),\qquad I=\frac{\pi}{4}(r_o^4-r_i^4)
$$

$$
m_{\mathrm{shell}}=\rho_{\mathrm{material}}AL
$$

Inputs are $\rho_{\mathrm{air}}=1.225\ \mathrm{kg/m^3}$, $U=200\ \mathrm{m/s}$, $w_g=20\ \mathrm{m/s}$, $C_{N\alpha}=2\ \mathrm{rad}^{-1}$, $D_u=0.10\ \mathrm{m}$ and $L_u=3\ \mathrm{m}$. Case A applies the assignment's stated moment at the barrel. Case B includes the additional moment $VL$ when the upper interface shear is transferred through the barrel without an intermediate lateral reaction. The recommended design is checked under both cases; their results are not mixed.

The factor 1.1 is a declared design requirement, not a statistically derived material factor. Strength allowables are not divided by 1.1 a second time. Pressure-end thrust is not subtracted from compression in the design load case; a separate closed-end strength check is provided.

## 3. Beam-column moment and shear envelope

$$
P_E=\frac{\pi^2 EI}{L^2},\qquad \beta=\frac{L}{2}\sqrt{\frac{P}{EI}}
$$

$$
M_{\max}=M_0\sec\beta,\qquad P<P_E
$$

$$
V_{\mathrm{secondary}}=M_0\sqrt{\frac{P}{EI}}\tan\beta
$$

$$
V_{\mathrm{bound}}=V+V_{\mathrm{secondary}}
$$

A uniform first-order moment equal to the maximum end-moment magnitude is used as a majorant of the same-sign moment diagram. The equal-end-moment pinned beam-column solution supplies $M_{\max}$. The end-slope term gives a conservative additional shear contribution; the external and secondary shear magnitudes are added. This is an envelope, not an assertion that the physical first-order diagram is constant while carrying nonzero shear. The independent verifier compares the moment with a 2,000-term sine-series solution of $EIy''+Py=-M_0$.

## 4. Transverse shear without a torsional capacity substitution

The wall stress envelopes are

$$
a=\frac{P}{A},\qquad b=\frac{M_{\max}r_o}{I},\qquad s_0=\frac{V_{\mathrm{bound}}}{\pi rt}
$$

$$
h=\frac{pr_i}{t}>0
$$

$$
C(\theta)=a-b\cos\theta,\qquad T(\theta)=s_0\sin\theta
$$

For local radial perturbation $w$, the destabilising membrane term in the Donnell local-shell geometric energy is proportional to

$$
\mathcal{G}=Cw_x^2+2Tw_xw_s-hw_s^2
$$

$$
\mathcal{G}=\left(C+\frac{T^2}{h}\right)w_x^2-h\left(w_s-\frac{T}{h}w_x\right)^2
$$

$$
\mathcal{G}\leq\left(C+\frac{T^2}{h}\right)w_x^2
$$

Consequently a uniform axial-compression majorant for this local-shell model is

$$
C_{\mathrm{eff}}=\max_{-1\leq c\leq 1}\left[a-bc+\frac{s_0^2}{h}(1-c^2)\right]
$$

Evaluate the quadratic at $c=-1,+1$ and its stationary point when it lies in the interval. This inequality handles the co-located transverse shear and hoop tension directly. It does not use a torsional buckling stress or assign a shear knockdown factor. The smaller inner-radius hoop stress is used to avoid overstating membrane-tension support. The bound requires the specified positive operating pressure: it is not a depressurised-load qualification.

The inequality is a sufficient majorisation within the stated local Donnell energy model. It is not a proof of finite-amplitude shell collapse, pressure-follower effects, or coupled global/local instability in a geometrically imperfect manufactured structure. Those phenomena are outside the supplied course model. Global beam-column and cross-section ovalisation checks are retained independently.

## 5. Local capacity, elastic domain and stability checks

$$
\sigma_{\mathrm{cl}}=\frac{E}{\sqrt{3(1-\nu^2)}}\frac{t}{r},\qquad \sigma_{\mathrm{cr}}=k\sigma_{\mathrm{cl}}
$$

$$
U_{\mathrm{local}}=\frac{C_{\mathrm{eff}}}{\sigma_{\mathrm{cr}}},\qquad U_{\mathrm{Euler}}=\frac{P}{P_E}
$$

$$
M_{\mathrm{Brazier}}=\frac{0.987\,Ert^2}{\sqrt{1-\nu^2}},\qquad U_{\mathrm{ovalisation}}=\frac{M_{\max}}{M_{\mathrm{Brazier}}}
$$

The notice prescribes $k=0.40$ for B-basis metals and 0.50 for B-basis QI composites. No geometry-dependent NASA correlation is multiplied into these prescribed factors. The local axial classical relation is the lower continuous-wavenumber envelope used by the course shell model; a factor calibrated for one material population is not represented as experimental validation of this design.

An elastic buckling capacity must not exceed the metal yield allowable, or the smaller QI normal allowable. A candidate outside this domain is rejected; it is not accepted by clipping a predicted elastic capacity to a strength value. This eliminates yield-capped candidates from the design search. It does not substitute for proportional-limit or tangent-modulus data in a physical elastic-plastic analysis. Ideal unpressurised Brazier capacity is checked without pressure-stabilisation credit.

## 6. Co-located material failure

For metals, maximise the following over the circumference:

$$
\sigma_x=-\frac{P}{A}+\frac{M_{\max}r_o}{I}\cos\theta,\qquad \sigma_h=\frac{pr_o}{t}
$$

$$
\tau=\frac{V_{\mathrm{bound}}}{\pi rt}\sin\theta
$$

$$
U_{\mathrm{VM}}=\frac{\sqrt{\sigma_x^2+\sigma_h^2-\sigma_x\sigma_h+3\tau^2}}{\sigma_y}
$$

The outer-radius hoop stress upper-bounds the membrane stress for the strength calculation. For closed-end strength sensitivity only, add $p\pi r_i^2/A$ to $\sigma_x$. The exact extremum follows from a quadratic in $\cos\theta$.

For QI composites, the supplied uniaxial allowables do not uniquely determine quadratic cross terms. Let z contain the three stresses normalised by the relevant uniaxial allowables, and let the normalised quadratic interaction matrix Q be positive semidefinite with unit diagonal. Its entries satisfy $|Q_{ij}|\leq1$, hence

$$
\mathrm{FI}=\mathbf{z}^{\mathsf{T}}\mathbf{Q}\mathbf{z}\leq\left(\left|z_1\right|+\left|z_2\right|+\left|z_3\right|\right)^2
$$

$$
U_{\mathrm{QI}}=\frac{|\sigma_x|}{X_{\mathrm{sign}}}+\frac{\sigma_h}{Y_t}+\frac{|\tau|}{S}
$$

$$
X_{\mathrm{sign}}=X_c\quad(\sigma_x<0),\qquad X_{\mathrm{sign}}=Y_t\quad(\sigma_x\geq 0)
$$

Requiring $U_{\mathrm{QI}}\leq1$ bounds every convex quadratic interaction having these normalised uniaxial limits. The sign-dependent criterion is maximised analytically on each axial-stress sign interval: it has the form $A+Bc+C\sqrt{1-c^2}$. The QI equivalence treats in-plane tensile strength as direction-independent. No laminate stacking sequence, interlaminar strength or manufacturing qualification follows from this homogeneous model.

## 7. Optimisation and numerical resolution

The nominal search enumerates $D=1,2,\ldots,300\ \mathrm{mm}$ and walls at 0.01 mm increments. Each material is searched independently. The admissible upper wall is

$$
t_{\max}=\min\left(\frac{D}{21},\frac{\eta D}{2+\eta}\right),\qquad \eta=\frac{\sigma_{\mathrm{allow}}\sqrt{3(1-\nu^2)}}{kE}.
$$
 The latter enforces the elastic-capacity gate. Integer bisection locates the first feasible thickness within this domain; exhaustive sequential-search tests independently verify the search on representative diameters for every material and both load cases. The transfer-load sweep governs selection; the selected geometry is checked under both load cases. Nominal sweep minima are checked against the saved CSV file.

A complete second search at 0.1 mm diameter and 0.001 mm wall spacing quantifies discretisation effects. The nominal-grid solution, not the finer result, is used for the reported design dimensions. Neither grid defines stock availability or a wall-thickness tolerance. Acceptance requires every utilisation $U\leq1$ and every applicability gate true.

The utilisation margin is

$$
\mathrm{MS}=\frac{1}{U}-1.
$$
 For nonlinear beam-column response, this is a capacity/demand utilisation margin at the specified design load; it is not an additional load factor obtained by scaling the complete nonlinear load path.

## 8. Design-space and mass boundary

The minimum is over the specified homogeneous, unstiffened shell family and discrete grids. All seven permitted effective material sets are included. No claim of a global minimum over all stiffened, sandwich or hybrid architectures is made. Such architectures require additional design variables and property data; the presence of a lower mass homogeneous QI candidate is reported rather than excluded from the optimisation.

$$
m_{\mathrm{assembly}}=m_{\mathrm{shell}}+m_{\mathrm{end\ rings}}+m_{\mathrm{connections}}+m_{\mathrm{other\ interfaces}}
$$

The briefs prescribe ideal rigid end boundaries but no ring cross-sections, attachment geometry or interface mass budget. Reported masses therefore use shell mass. Interface contributions cannot be assigned numerical values from the supplied information. This is an explicit system-boundary exclusion, not a computational result equal to zero.


<!-- PAGE -->
# Numerical Evaluation and Verification

## Selected geometry under both load cases

| Quantity | Symbol | Unit | Primary | Transfer |
| --- | --- | --- | --- | --- |
| Outer diameter | $D$ | mm | 122.000000 | 122.000000 |
| Wall thickness | $t$ | mm | 1.520000 | 1.520000 |
| Area | $A$ | $\mathrm{mm}^2$ | 575.318606 | 575.318606 |
| Second moment of area | $I$ | $\mathrm{mm}^4$ | 1044040.799943 | 1044040.799943 |
| Axial force | $P$ | N | 33000.000000 | 33000.000000 |
| Internal pressure | $p$ | MPa | 0.330000 | 0.330000 |
| First-order moment | $M_0$ | $\mathrm{N\,m}$ | 2417.463166 | 4834.926332 |
| Amplified moment | $M_{\max}$ | $\mathrm{N\,m}$ | 2895.910500 | 5791.820999 |
| External shear | $V$ | N | 1611.642111 | 1611.642111 |
| Secondary shear | $V_{\mathrm{secondary}}$ | N | 1239.508870 | 2479.017740 |
| Euler load | $P_E$ | N | 239517.023979 | 239517.023979 |
| Axial stress | $P/A$ | MPa | 57.359522 | 57.359522 |
| Bending stress | $M_{\max}r_o/I$ | MPa | 169.198886 | 338.397772 |
| Peak shear stress | $s_0$ | MPa | 9.911555 | 14.220503 |
| Hoop tension lower bound | $h$ | MPa | 12.913421 | 12.913421 |
| Effective compression | $C_{\mathrm{eff}}$ | MPa | 226.558408 | 395.757294 |
| Critical stress | $\sigma_{\mathrm{cr}}$ | MPa | 399.345683 | 399.345683 |
| Normal allowable | $\sigma_{\mathrm{allow}}$ | MPa | 400.000000 | 400.000000 |
| Critical angle | $\theta_{\mathrm{crit}}$ | $^{\circ}$ | 180.000000 | 180.000000 |
| Brazier moment | $M_{\mathrm{Brazier}}$ | $\mathrm{N\,m}$ | 7531.305843 | 7531.305843 |

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

<!-- PAGE -->

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

## References

1. VJTI, *The Drakkar Ascent Challenge*, August 2026, sections 3-8: geometry, load derivation, boundary conditions, material data and scoring.
2. Guild Assay Office, *Tweak to Drakkar Ascent*, 3 October 2026, sections 2-5: revised material properties, prescribed knockdowns and response requirements.
3. NASA/SP-8007-2020/REV 2, *Buckling of Thin-Walled Circular Cylinders*, equations 7 and 16 and section 4.1.1: reference axial-shell and ovalisation expressions; printed page 25 identifies long-cylinder/global-local and plasticity limitations. https://ntrs.nasa.gov/citations/20205011530

Derivation note: The pressure-supported completion-of-square bound and PSD composite interaction bound are derived in sections 4 and 6 of this document. They are not represented as empirical correlations from source 3.
