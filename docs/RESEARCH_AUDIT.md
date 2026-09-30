# Drakkar repository audit

Audited 29 September 2026. Research revision: `dd1fce2a91e4b179e3aacabb6fe4e8c2f5c1d641`. Main: `a10e10f`.

**Verdict: useful preliminary study; the final passing-design, optimum-diameter and total-mass claims are not established.** This is an analytical audit, not structural certification or a replacement final design.

All tracked files in the research snapshot were inspected, including three Python scripts, three substantive Markdown documents, README, gitignore, the PDF, five distinct valid PNGs and one duplicate PNG. `assets/test.png` is text, not an image. The branch PDF is byte-identical to the supplied workspace PDF. Work was performed in a temporary snapshot without changing the checkout or repository files. The user-provided end-condition clarification is treated as part of the design basis.

## Priority 1: correct before calling any design passing or optimal

### A01 — Euler demand uses an unjustified equivalent axial force

Locations: `parametric_diameter_study.py:45-49`; `plot_trade_studies.py:59-61`; solution report section 4.2.

The model sets `P_eq = F + 2*M/R` and compares it against Euler capacity. This quantity is area times peak compressive stress, not the actual axial resultant. Integrating the bending stress around the cylinder gives zero net axial force. The conversion does not establish a beam-column stability criterion.

At D = 120 mm the code replaces 30 kN with 103.256 kN. At D = 80 mm, carbon Euler thickness is 4.037 mm under that rule; axial-only Euler screening gives 0.866 mm. Holding the other preliminary criteria unchanged produces 1.636 mm thickness and 0.987 kg shell mass at 80 mm. These are sensitivity numbers, NOT a newly validated design.

Improvement: use `Pcr = pi²*E*I/(K*L)²`, K = 1, with the actual axial compression; preserve bending stress and evaluate second-order beam-column effects using an applicable analytical solution. Do not merely delete the bending term and declare the thinner design safe. The current artificial Euler branch drives the reported optimum.

Reference: Air Force Flight Dynamics Laboratory Stress Analysis Manual, beam-column chapter, reproduced at https://engineeringlibrary.org/reference/beam-columns-air-force-stress-manual . It distinguishes axial load from bending and treats compression-induced moment amplification explicitly.

### A02 — Final thickness fails the repository's own local-buckling check

Locations: solution report lines 232 and 250-258; presentation lines 145-148; drawing script lines 162 and 173.

Keeping the repository's R = 60 mm, E = 55 GPa, gamma = 0.35 and buckling factor = 1.40:

| Quantity | Recalculation |
|---|---:|
| Required local-buckling thickness | 1.405263 mm |
| Selected nominal thickness | 1.400000 mm |
| Applied maximum compression at selected thickness | 195.639951 MPa |
| Reduced local critical stress | 271.848033 MPa |
| Local margin: capacity/(1.4*demand) - 1 | -0.007477 (-0.748%) |
| Actual thickness from 9 × 0.155 mm | 1.395000 mm |
| Local margin at actual nine-ply thickness | -0.014554 (-1.455%) |

The reported +0.00 is a rounded negative margin. Using mean radius consistently makes the 1.4 mm screen approximately -1.57%, and the 1.395 mm screen approximately -2.27%.

Improvement: select a realizable laminate thickness, round upward, and recompute every check at that exact geometry. Display the pass/fail decision using unrounded values. Do not imply a small nominal thickness increase resolves the other laminate and model issues.

### A03 — The specified laminate is not quasi-isotropic

Locations: presentation slide 5; drawing script lines 145-163; both drawing PNGs.

The equal-thickness UD layup `[0/+45/-45/90/0/90/-45/+45/0]` is symmetric and balanced, but has orientation counts 3, 2, 2, 2. It is not an in-plane quasi-isotropic laminate for ordinary orthotropic UD carbon/epoxy. Symmetry removes extension-bending coupling; balance removes in-plane extension-shear coupling. Neither proves isotropy or removes every bending coupling term.

The brief's effective QI E, nu and strength allowables therefore cannot automatically be assigned to this specific nine-ply laminate. Even a genuinely in-plane-QI laminate does not automatically have isotropic bending stiffness.

Improvement: either explicitly remain at the brief's homogenised QI material level without inventing a validated ply schedule, or select a genuinely QI schedule and establish its properties from ply data. A symmetric eight-ply `[0/+45/-45/90]s` is a familiar QI orientation example, but its thickness and buckling still require sizing; it is not a ready replacement design.

Reference example of QI versus cross-ply effective properties: NASA MAC/GMC example manual, https://nasa-multiscale.github.io/legacy/MAC-GMC-4.0-Example-Manual-12.html .

### A04 — Total structural mass is not the quantity being optimised

Locations: calculation script line 94; plotting script line 84; solution report lines 233 and 240; presentation lines 151-154 and 170; plot axes and drawing title block.

Both scripts compute shell mass only. The presentation separately gives 0.380 kg forward ring and 0.420 kg aft ring, bringing its stated 1.271 kg shell to 2.071 kg, but later claims 1.27 kg as the lightest passing component mass. The additional 0.800 kg is about 63% of that quoted shell mass.

No ring dimensions, connection design, material assignment or derivation substantiates those collar masses. There are no joint reinforcement, fastening or bonding calculations. Diameter-dependent ring and transition masses can move the optimum.

Improvement: label existing results shell-only; define the component mass boundary; derive a complete bill of mass and optimise it consistently. If rings are supplied externally and excluded by the competition, document that explicit convention rather than assuming it.

### A05 — Knockdown and safety factors have no documented design basis

Locations: both calculation scripts' constants; report section 4.3; presentation slide 3 and line 139.

A constant gamma = 0.35 is applied to every material and diameter and described as NASA SP-8007. No specific equation, figure, validity limits or laminate justification is given. This audit does not establish that 0.35 is necessarily unsafe; it establishes that its applicability and conservatism have not been demonstrated.

The PDF requires safety factors but does not state 1.25 and 1.40. They must be labelled assumptions unless supplied by the instructor separately. The presentation incorrectly describes them as required values.

Improvement: cite an applicable analytical buckling method, separate safety factors from imperfection knockdowns, justify extensions to QI material and show sensitivity. Avoid claiming one constant guarantees no in-flight buckling.

References: NASA SP-8007 Rev 2, https://ntrs.nasa.gov/citations/20205011530 ; NASA composite-cylinder knockdown caution, https://ntrs.nasa.gov/citations/20240000391 . NASA's caution about universal composite factors supports the need for a specific rationale; it does not provide a replacement factor for this design.

### A06 — Pressure, composite failure and interaction checks are incomplete

Locations: calculation script lines 61-82; plotting script lines 69-80; report sections 3.1 and 4.1; presentation slide 6.

Strength sizing subtracts `p*R/2` from the axial membrane compression, assuming closed-end pressure force is carried through the barrel. The load path is not established. The local-buckling check omits relief, which may be a deliberate conservative screen, but that distinction is not documented as a load-case policy.

At 120 mm diameter the assumed end force is about 3.39 kN; at 300 mm it is about 21.21 kN. Its significance varies greatly across the sweep.

The quadratic composite equation is explicitly written, but its interaction coefficient and use of the supplied directional allowables are not justified. Only the compression-side envelope is evaluated; there is no tensile-side allowables treatment or complete circumference check. The brief lacks a complete directional allowable set, so missing inputs should be stated rather than invented.

The code combines peak bending stress with peak transverse shear from another circumferential position. That is a conservative envelope at that fibre under the assumed model, not a physically co-located exact stress state. It can add unnecessary mass and is not a substitute for checking the full circumference. Shear appears in material failure but there is no local shear-buckling/combined-load treatment or justification for neglecting it.

Improvement: define pressure load paths and load cases, evaluate signed axial/hoop/shear stresses at common circumferential positions, state the approved composite interaction model, and justify or evaluate buckling interactions.

## Priority 2: reconcile results and geometry

### A07 — The claimed global optimum is contradicted by the existing code

Locations: report line 28 and section 7; presentation slide 4; plotting script line 92 and benchmark grid line 229.

Even before fixing the mechanics, the plot's 300-point grid gives carbon minimum 1.164835 kg at 104.615385 mm, while its 1 mm benchmark grid gives 1.167538 kg at 105 mm. The report claims a global minimum of 1.271 kg at 120 mm, which is only the best carbon point on its coarse tabulated grid.

The code searches 70-300 or 80-300 mm, despite the brief specifying only a maximum diameter. A search over an assumed lower bound does not establish a global optimum over all permitted geometry. Thickness is continuous and no laminate increments or manufacturing limits are enforced.

Improvement: state the search domain and practical constraints, refine minima, evaluate discrete buildable candidates, and distinguish the mathematical screening minimum from the selected design. Recompute only after resolving A01-A06.

### A08 — Aluminium is not the lightest metal in the existing results

Locations: plotting script line 122; report section 7; guide and presentation conclusions.

On the current 1 mm grid, magnesium is 1.553022 kg at 121 mm versus aluminium 1.743304 kg at 101 mm. Magnesium is about 10.9% lighter. Aluminium can be a preferred practical baseline, but that needs a stated reason; it cannot be called the lightest metal on these numbers.

The current model also shows strength controlling the magnesium and steel optima. Claims that material failure never governs are not generally true.

### A09 — Outer radius is misidentified as mean radius

Locations: report line 97; both scripts' `R = D / 2`.

For specified OD and wall thickness, mean radius is `(D - t)/2`. Exact section expressions are `A = pi*(Do²-Di²)/4` and `I = pi*(Do⁴-Di⁴)/64`, with `Di = Do - 2*t`.

For the 120 × 1.4 mm carbon shell, exact mass is 1.251912 kg versus 1.266690 kg from the code's outer-radius thin-wall approximation. Exact Euler capacity is 221.301 kN versus 229.198 kN. These corrections matter when margins are near zero. At the smallest diameters some predicted walls approach several millimetres, so the thin-wall assumption itself needs checking.

Improvement: use exact A and I for global beam calculations and consistent mean radius for shell theory; solve implicit thickness sizing if needed. Check approximation validity rather than claiming exact geometry.

### A10 — Presentation failure-index and pressure-margin numbers are unsupported

Location: presentation lines 145-148.

At D = 120 mm, t = 1.4 mm, using the repo's own stress envelope, the quadratic failure index is 0.108988, not 0.0172. Its allowable 1/1.25² = 0.64 is correct. The proportional-load strength margin is `1/(1.25*sqrt(FI)) - 1 = 1.423264`, agreeing with the reported +1.43. Thus the displayed FI and margin do not describe the same calculation.

For the claimed pressurised local margin +0.38, no supporting equation is implemented. Crediting only the repo's closed-end axial pressure relief gives approximately +0.02624 at t = 1.4 mm, using its radius convention. Additional pressure stabilisation could require a separate applicable model; +0.38 cannot be reproduced from the supplied one.

Improvement: generate displayed indices, margins and pass/fail directly from checked results and state the exact pressure-stabilisation model if one is used.

### A11 — End conditions, load transfer and assembly envelope need explicit treatment

Locations: report stress/global-buckling sections; drawing script lines 60-72; presentation slide 1.

The repo retains bending stress and uses the K = 1 Euler expression, which are consistent with the supplied clarification. It does not, however, explain the separation of buckling restraint from physical joint moment transfer, or size the joints for the circumferential axial-force distribution.

Document `Nx(theta) = -F/(2*pi*r) + M*cos(theta)/(pi*r²) + Nx_pressure`, plus shear transfer, with signs and angular convention. The rigid rings keep the ends circular, not the entire shell immune to ovalisation or local instability.

The drawing dimensions a 1500 mm shell and places end rings outside both ends. It does not establish whether the complete assembly fits the 1500 mm envelope. Specify assembly datums and included length.

The brief's prescribed moment is 2.198 kN·m. State the section at which it acts and the assumed moment distribution. If an upper-interface moment and shear pass to the lower interface without an intermediate lateral reaction, the additional moment magnitude is V*L = 2.198 kN·m. Do not silently replace the assignment load: document the assignment convention and distinguish it from the physical free-body model.

## Priority 3: reproducibility, drawings and presentation

### A12 — Sources and generated outputs drift apart

The committed material chart labels glass/epoxy optimum 138 mm; the source's 1 mm grid returns 118 mm and 2.215345 kg. The two material-bar-chart files are byte-identical duplicates. Two near-identical barrel drawings contain different layup notation, but only one output filename is generated by the current script.

All graphics scripts save to the current working directory, while committed figures reside in `assets/`; simply running them from the repo root leaves the tracked figures stale. Drawings hardcode dimensions, mass and margins instead of receiving checked results.

Improvement: maintain one small calculation source and material table, a consistent output directory, and derived tables/drawings. This is a justified reduction of existing duplication, not a need for a large software framework.

### A13 — Reproduction instructions and dependencies are absent

README contains only the project name. No dependency manifest, Python version instructions, run commands, result export or automated checks are present. The stdlib calculation script ran successfully. Both graphics scripts initially failed in the default Python environment because Matplotlib could not import `packaging`; Python 3.12 also lacked Matplotlib. These are environment failures, not proof of a syntax bug in the scripts, but the repo gives no reproducible setup.

Improvement: add a minimal dependency specification and short run instructions. Use a main guard so importing calculations does not print tables or create files. A small set of independent checks should cover the load derivation, exact geometry, margin sign at the selected thickness, and consistency of generated labels. Do not rely on scripts agreeing with each other when they share the same faulty formula.

### A14 — Drawing is a concept schematic, not a completed engineering definition

Both drawing PNGs were visually inspected. The notes box overlaps the bottom of the cross-section and some thrust annotation extends outside the drawing border. There are no dimensioned collar/joint details, assembly-length definition, selected ring material, tolerances or laminate acceptance assumptions. Shear and moment share a single arrow rather than distinct force and couple symbols. The graphic is labelled NTS, so exaggerated wall thickness alone is not an error.

Improvement: after correcting the design, separate force and couple arrows, clear overlaps, dimension the interface and assembly, mark the load axes and ply reference direction, and remove unsupported FINAL OPTIMAL/pass labels.

### A15 — Broken links and invalid/redundant assets

The guide uses absolute `file:///C:/AERO_SEM5_PROJ/...` links, which do not work as repository-relative links on GitHub or this machine. Figure paths omit `assets/`. `assets/test.png` contains the four ASCII characters `test`. The bar-chart duplicate and ungenerated alternate drawing confuse which outputs are authoritative.

Improvement: use relative links, embed canonical figures, remove the text placeholder and retire or clearly version superseded assets. No files were removed during this audit.

### A16 — Unsupported claims should be replaced with bounded statements

Across the guide, report and presentation:

- 120 mm does not equal the upper vehicle's 100 mm diameter; a transition remains.
- No aerodynamic calculation establishes elimination of transonic wave drag or separation.
- A cure cycle of 180 C and 7 bar needs a selected material/process specification.
- R/t alone does not establish impact tolerance or zero handling microbuckling.
- The stated 300 mm baseline R/t = 167 does not match its 1.065 mm carbon wall (approximately 141 under the report's radius convention).
- Euler thickness growth is algebraic, not exponential; with the repo's extra moment term it includes R^-3 and R^-4 contributions.
- Surface-area growth alone does not prove total mass grows linearly when thickness changes.
- Full marks and the lightest competitor mass cannot be known from this repository.

Improvement: report demonstrated results, identify assumptions, and reserve ranking claims for the evaluated candidate set and mass boundary.

## Verification record

- Read all three Python sources and parsed all successfully.
- Ran the parametric script: 48 cases, successful exit.
- Extracted and executed the unmodified plotting calculation function independently of graphics imports.
- Compared all 48 shared cases: exact numerical agreement between the two implementations.
- Checked all 22 report table rows against the implemented equations. Broad agreement; small last-digit inconsistencies exist in several 250 mm values, and displayed chosen thickness and continuous-thickness mass are not consistently distinguished.
- Recomputed all seven material minima on the benchmark's 1 mm grid: carbon 105 mm/1.167538 kg; aramid 118/1.369789; magnesium 121/1.553022; aluminium 101/1.743304; glass 118/2.215345; titanium 94/2.093237; steel 122/3.275303. These reproduce the current model, not a validated optimum.
- Independently recalculated final-design stresses, failure index, margins, pressure relief, exact section properties and shell mass.
- Verified PDF identity and image file types; visually inspected all distinct valid committed figures; verified the duplicate chart by hash.
- Installed an isolated temporary environment (Python 3.10.19, NumPy 2.2.6, Matplotlib 3.10.9), then ran both original graphics scripts successfully with the Agg backend. Each produced its expected files in the snapshot root. Nonfatal font-cache warnings occurred. Visually inspected all four regenerated outputs; the regenerated material chart correctly labels glass at 118 mm, confirming the committed 138 mm label is stale.
- Checked git status: main checkout and original untracked PDF/tmp entries unchanged by this audit.

## Recommended order of work

1. Establish the instructor-approved safety factors, composite failure assumptions, pressure load path and moment convention.
2. Correct Euler/beam-column treatment, geometry and laminate validity; justify the shell-buckling method.
3. Re-evaluate signed stress and stability interactions, then select manufacturable thicknesses with unrounded nonnegative margins.
4. Define joints, end rings and assembly mass/length; repeat the diameter/material trade on total mass.
5. Regenerate all tables, figures and drawings from the checked calculation, with one canonical asset per output.
6. Rewrite the conclusions, add reproduction instructions and a few independent verification cases.

Do not freeze a replacement optimum diameter until steps 1-4 are complete. Carbon/epoxy remains a candidate, not a proven competition winner.
