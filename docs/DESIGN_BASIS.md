# Design Basis and System Boundary

Geometry, loads, material law and system boundary.

## Normative inputs

The original assignment supplies geometry, flight conditions, material families and ideal boundary conditions. The 3 October 2026 notice supersedes the original strength values, composite elastic moduli and buckling knockdowns. The numerical material tables are reproduced in the technical report. The original source PDFs are retained without modification in `docs/briefs/`.

| Item | Adopted requirement |
| --- | --- |
| Shell length | 1500 mm |
| Maximum outer diameter | 300 mm |
| Boundary idealisation | Simply supported, circular rigid end rings |
| Axial service force | 30 kN compression |
| Wall service pressure | 0.3 MPa internal |
| Nominal flight / gust speed | 200 / 20 m/s |
| Air density | 1.225 kg/m3 |
| Upper vehicle | Length 3 m, diameter 0.10 m, normal-force slope 2 rad^-1 |
| Proportional design load factor | 1.1, applied once before beam-column response |
| Primary load case | Assignment moment M = f L_u^2/2 |
| Transfer load case | Upper-interface moment plus V L across the shell |
| Material-quality factors | Metals k = 0.40; supplied effective-QI materials k = 0.50 |
| Numerical acceptance | Every required utilisation <= 1 and all applicability gates satisfied |

## Model closure

The design family is an unstiffened, uniform, homogeneous shell. Quasi-isotropic material behaviour is represented by the supplied effective properties. The conservative PSD quadratic strength envelope bounds unknown convex quadratic cross coefficients; it does not define a ply schedule.

The positive operating pressure is used in a derived local-shell energy inequality to bound transverse shear. This does not import an empirical pressure enhancement or substitute a torsion capacity for transverse-shear capacity. The capacity uses only the prescribed axial knockdown. Unpressurised operation is outside the stated load set.

Elastic buckling capacities exceeding the relevant normal allowable are rejected. A strength cap is not used as an elastic-plastic constitutive model. The adopted material law is linear elastic up to the supplied allowable; verification of a particular product form's proportional limit requires its stress-strain data.

The moment and shear envelopes include beam-column amplification. Global Euler and ideal cross-section ovalisation are additional checks. The complete energy derivation and the boundary between local-shell modelling and nonlinear coupled structural response are stated in [METHOD.md](METHOD.md).

## Mass and interface boundary

The objective is shell mass within the defined family. Rigid end rings specify kinematic boundary conditions. Their sections, finite stiffness, attachment details and masses are not supplied.

```
m_assembly = m_shell + m_end_rings + m_connections + m_other_interfaces
```

The missing interface terms are excluded from the numerical objective. They are not assumed to be physically zero. Stiffened, sandwich and hybrid configurations would add design variables and failure constraints; their global optimum is not established by the current homogeneous-shell search.

## Acceptance versus production release

A passing result is an analytical acceptance of the stated course model. Minimum actual thickness and gust boundaries are calculated rather than treated as implied production allowances. Product tolerances, laminate qualification, finite joint stiffness and full nonlinear global/local collapse are not established by the supplied scalar material data and ideal boundary conditions. These scope exclusions cannot be eliminated by changing a software flag or increasing numerical precision.
