# Drakkar Ascent - requirement-led analytical study

**Current result: service-load shell screening, not a complete passing competition design.** The smallest calculated metal-shell mass in the declared search is Aluminium 7075-T6, 115 mm OD x 0.93 mm wall, **1.404759 kg shell only**. Ring/connection mass and required safety factors remain unresolved. All seven supplied materials are reported.

This supersedes the earlier 2.878 kg assembly claim as the current design basis. That number belonged to a different assumed load/tolerance/connection model. The new shell mass is NOT a like-for-like assembly weight saving. The earlier implementation remains in Git history at commit 472798d.

## 1. What is required, removed and unresolved

| Item | Treatment | Why |
| --- | --- | --- |
| Length, OD limit, F/M/V/p, material properties | Retained as supplied | Brief sections 3-7 |
| Rigid circular ends and K = 1 | Retained | Brief and user clarification; bending still transfers through shell/joints |
| Required safety factor | Unspecified; compliance unresolved | Brief section 8 requires factors but gives no values |
| 1.5 load multiplier | Removed from baseline | 1.0 means service loads, not an adopted design safety factor |
| 5% wall loss and 1.5 mm initial bow | Removed | No tolerances or measured imperfection supplied |
| 0.35 shell reduction cap | Removed | Retain geometry-dependent knockdown correlation required by section 6 |
| 0.35 ovalisation multiplier | Removed | Use ideal Brazier capacity only as an analytical screen |
| Unpressurised load case | Removed | Only the stated pressure appears in the baseline |
| Bolt prying/root/shear multipliers and assumed fasteners | Removed with joint sizing | No defensible complete connection specified; mass is now shell-only for ALL materials |
| Minimum metal wall and composite ply/block thickness | Removed | Common numerical thickness grid; no claim of a manufacturable laminate |
| Positive composite cross term | Removed | Diagonal quadratic screen; actual interaction remains unresolved |

Some modelling choices are unavoidable: a structural family, governing equations, a composite quadratic criterion and a numerical search resolution. They are declared below rather than presented as problem data. The supplied information does not uniquely determine a complete assembly optimum. Simply setting all empirical knockdown factors to 1 would violate the instruction to use knockdown factors and would remove a relevant physical effect.

## 2. Loads and support interpretation

```text
q = 0.5 * rho_air * V_inf^2 = 24500.000 Pa
alpha = atan(20/200) = 0.099668652 rad
f = q * CN_alpha * alpha * Du = 488.376397 N/m
V = f * Lu = 1465.129192 N
M = f * Lu^2 / 2 = 2197.693787 N m
F = 30000 N compression
p = 300000 Pa
L = 1.5 m; maximum OD = 0.300 m; K = 1
```

These are the stated service loads, without an added 1.5 factor. Bending remains in the wall and transfers through real joints as circumferentially varying axial force. Rigid end rings prescribe end circularity; they do not make interior ovalisation or bending disappear.

The primary case follows the prescribed M. A separately labelled scenario uses M + V*L when shear traverses the barrel without an intermediate lateral reaction. It is not imposed on the primary assignment case.

## 3. Retained mechanics and explicit approximations

The selected family is a uniform, unstiffened circular shell. Nominal thickness equals analysed thickness; there is no prescribed tolerance or initial bow. This is an ideal nominal geometry, not a claim that manufactured barrels are perfect.

```text
ro = Do/2; ri = ro-t; r = (ro+ri)/2
A = pi*(ro^2-ri^2)
I = pi/4*(ro^4-ri^4)
mass_shell = density * A * L
Pcr = pi^2*E*I/L^2
M_design = M / cos[0.5*L*sqrt(F/(E*I))]
```

The secant expression retains load-induced beam-column bending; it adds no arbitrary initial imperfection. It is exact for the equal-end-couple uniform first-order moment idealisation, used here as an envelope. Euler uses the actual axial force, not an invented equivalent compression from bending.

```text
sx(theta) = -F/A + M_design*ro*cos(theta)/I
sy = p*ro/t
tau(theta) = V*sin(theta)/(pi*r*t)
metal utilisation = sqrt(sx^2 + sy^2 - sx*sy + 3*tau^2) / yield
```

The hoop expression uses outer radius as a thin-wall upper approximation. Strength is evaluated at the same angle for all stress components; angular maxima are solved analytically and tested against an independent scan.

For QI materials, the explicit diagonal quadratic screen is:

```text
X = Xc for sx < 0; X = Yt for sx >= 0
FI = (sx/X)^2 + (sy/Yt)^2 + (tau/S)^2
utilisation = sqrt(FI)
```

Directional tensile equivalence is inferred from QI properties. The cross coefficient is set to zero solely to define this preliminary quadratic model; the supplied uniaxial allowables do not identify an interaction coefficient or actual ply-level failure. These rows therefore remain equivalent-material screens, not validated first-ply designs. No ply thickness, stacking schedule or manufactured laminate is invented.

## 4. Stability and pressure treatment

```text
phi = sqrt(r/t)/16
gx = 1 - 0.901*(1-exp(-phi))
gb = 1 - 0.731*(1-exp(-phi))
classical_stress = E/sqrt(3*(1-nu^2)) * t/r
sx_cr = min(gx*classical_stress, material_normal_limit)
sb_cr = min(gb*classical_stress, material_normal_limit)
tau_cr = 0.747*0.67*E*(t/r)^1.25 / sqrt(L/r)
Ulocal = (F/A)/sx_cr + (M_design*ro/I)/sb_cr
       + [V/(pi*r*t)]/tau_cr
M_Brazier_ideal = 0.987*E*r*t^2/sqrt(1-nu^2)
Uoval = M_design/M_Brazier_ideal
```

The shear capacity is capped by the supplied shear strength (yield/sqrt(3) for metals). The dimensional range of the moderately-long torsional-shell formula is checked, as is 10 <= r/t < 1500. Its use with peak transverse shear is a surrogate, not a validated transverse-shear solution. The linear combined-load interaction is an explicit approximation. Applying isotropic shell formulas to effective QI properties is also conditional.

NASA SP-8007 supplies the geometric knockdown correlations and ideal Brazier expression. Its axial empirical correlation is not experimentally verified for L/r > 5; the selected candidates require extrapolation. Removing an extra arbitrary reduction does not repair this limitation. [NASA SP-8007 Rev 2](https://ntrs.nasa.gov/citations/20205011530).

**Pressure has not been removed:** p = 0.3 MPa enters every primary strength calculation. The brief specifies pressure on the wall, without establishing closed-end axial thrust. A separate closed-end strength scenario adds p*pi*ri^2/A; it is not silently credited in Euler or local buckling.

Pressure-stabilised buckling is not solved by this model. NASA sections 4.1.1.5.4-6 give pressure-dependent methods, including end-load and empirical pressure corrections, with applicability restrictions. Arbitrarily crediting an unspecified benefit would replace one unsupported assumption with another. The unpressurised-capacity comparison is retained and labelled as a no-credit screening approximation, not a problem requirement or pressure-aware optimum. Ideal Brazier is likewise a no-pressure-stiffening diagnostic.

## 5. Search and results

Diameter: 1-300 mm in 1 mm steps. Wall: 0.01 mm numerical steps, restricted by the thin-shell domain rather than an invented material-specific minimum. The same resolution applies to metals and QI materials. Search resolution is not a manufacturing prescription. There is no additional 8 mm upper-wall cap: the domain ends at r/t = 10.

At each diameter, the first thickness meeting the numerical screen is retained. Shell mass increases monotonically with thickness in this domain, so that is the minimum grid mass at that diameter. The minimum over diameters is then reported. A numerical screen requires all implemented utilisations <= 1; it does NOT certify required safety-factor compliance or resolved model applicability.

| Material | OD (mm) | Wall (mm) | Shell mass (kg) | Status |
| --- | --- | --- | --- | --- |
| Aluminium 7075-T6 | 115 | 0.93 | 1.404759 | metal shell screen |
| Titanium Ti-6Al-4V | 94 | 0.81 | 1.575793 | metal shell screen |
| Steel 4130 | 151 | 0.55 | 3.061016 | metal shell screen |
| Magnesium AZ31B | 165 | 1.05 | 1.435870 | metal shell screen |
| Carbon/Epoxy QI | 98 | 1.16 | 0.846981 | equivalent-QI screen |
| Glass/Epoxy QI | 121 | 1.55 | 1.657725 | equivalent-QI screen |
| Aramid/Epoxy QI | 164 | 1.18 | 1.267532 | equivalent-QI screen |

![Diameter trade](assets/trade_study_diameter_vs_mass.png)

### Baseline metal shell checks

| Check | Service-load utilisation | Capacity/demand - 1 |
| --- | --- | --- |
| strength | 0.784167 | +0.275238 |
| Euler | 0.175954 | +4.683307 |
| shell_interaction | 0.995056 | +0.004969 |
| ovalisation | 0.751612 | +0.330474 |

These ratios are not proportional-load safety factors: second-order bending changes nonlinearly with load. No final passing status is assigned while the required factors remain unspecified.

![Checks](assets/failure_modes_vs_diameter.png)

### Separate transfer-moment scenario

The lowest screened metal shell for M + V*L is Aluminium 7075-T6, 133 mm OD x 1.06 mm wall, 1.851952 kg shell only. Every material's corresponding result is saved in JSON and the separate CSV.

## 6. Sensitivities without hidden defaults

Multipliers 1.00, 1.25, 1.50 and 2.00 are illustrative proportional-load scenarios, not required factors of safety. Every material is re-screened for each scenario. All loads including pressure scale in these scenarios; no pressure stabilisation is credited. The baseline remains 1.00. Numerical data for every scenario are in results/design.json.

![Material comparison and scenarios](assets/trade_materials_comparison_barchart.png)

The following changes only pressure-end thrust in strength for the same baseline shell. It does not establish pressure-dependent stability or redesign the shell:

| Material | Wall-pressure strength U | Closed-end strength U |
| --- | --- | --- |
| Aluminium 7075-T6 | 0.784167 | 0.766191 |
| Titanium Ti-6Al-4V | 0.782214 | 0.772581 |
| Steel 4130 | 0.818502 | 0.774438 |
| Magnesium AZ31B | 0.815717 | 0.763531 |
| Carbon/Epoxy QI | 0.807808 | 0.797627 |
| Glass/Epoxy QI | 0.790593 | 0.771858 |
| Aramid/Epoxy QI | 0.762490 | 0.711721 |

## 7. Concept and mass boundary

![Shell concept](assets/thrust_barrel_cad_drawing.png)

Rigid rings are shown schematically as prescribed boundaries. Their dimensions, stiffness, joints and mass are unresolved. Earlier bolt counts, flange dimensions, prying multipliers, root stress factors and fabricated hardware mass are removed. Shell mass must not be presented as total structural mass. Stiffened, hybrid and sandwich alternatives have not been ranked without their additional failure checks and material data.

## 8. Reproduction and verification

```sh
python3 parametric_diameter_study.py
python3 -m unittest discover -s tests -v
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python plot_trade_studies.py
.venv/bin/python generate_engineering_drawing.py
python3 generate_report.py
.venv/bin/python generate_outputs.py
```

Tests cover load derivation, exact section properties, beam-column limits, bending equilibrium, angular failure maximisation, removal of added allowances, explicit pressure scenarios and rechecking every material's saved result. Passing tests validates these implementation checks, not the unresolved physical approximations.

The challenge PDF sections 6-8 are the source for required methods, end conditions, manufacturing realism and unspecified required safety factors. The user's clarification governs bending transfer. Beam-column method reference: [Air Force Stress Analysis Manual](https://engineeringlibrary.org/reference/beam-columns-air-force-stress-manual). Composite knockdown limitations: [NASA bulletin](https://ntrs.nasa.gov/citations/20240000391).
