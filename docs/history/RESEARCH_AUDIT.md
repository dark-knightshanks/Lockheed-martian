# Analytical Model Revision Record

DRA-AUD-C | 6 October 2026

## Purpose

This record distinguishes numerical verification from model applicability and identifies the treatment of each issue in the current analytical solution. Revision A denotes the original clean-material submission. Revision B denotes the initial material-notice calculation. Revision C is specified in `docs/METHOD.md`.

| Issue | Revision C disposition | Evidence / scope |
| --- | --- | --- |
| Material-quality tables | Exact notice values implemented for all seven materials | Material-data regression test |
| Clean/degraded comparison | Same Revision C equations applied to both property sets | Matched fixed-geometry sensitivity records |
| Transverse shear represented by torsional capacity | Removed from revised acceptance calculations | Completion-of-square local geometric-energy bound |
| Additional shear knockdown interpretation | Removed | Only the prescribed normal-shell capacity factor is used |
| QI quadratic cross coefficients | Replaced by PSD interaction envelope | Derived bound and random-PSD regression test |
| Yield-capped elastic buckling capacities | Rejected outside elastic-capacity domain | Explicit domain test and rejected-candidate regression |
| Moment reference section | Case A and M+VL case B both evaluated | Separate saved sweeps and dual-case design check |
| Secondary beam-column shear | Included as an absolute-value envelope | Independent N/mm/MPa calculation |
| Search discretisation | Complete nominal and tenfold-refined grids | Per-material mass convergence record |
| Integer thickness search | Checked against sequential enumeration | Every material and both cases sampled in regression |
| Report/code inconsistency | Reports generated from JSON plus verification record | No independently maintained result tables |
| Total assembly mass | Excluded interface masses identified symbolically | End-ring / connection dimensions absent from input brief |
| Manufactured composite qualification | Outside homogeneous-QI scope | Laminate architecture and constituent data absent |
| Full nonlinear global/local shell collapse | Not established by course-level local/beam decomposition | NASA SP-8007 Rev. 2 discussion, printed p. 25 |

## Historical numerical evidence

The independent baseline audit is `BASELINE_VERIFICATION.md`; it verifies the archived Revision A numbers and records its method limitations. Its numerical agreement is not used to validate Revision C. The current independent verifier is `src/verify_revised.py`, with evidence in `data/guild_assay/verification.json`.

## Publication boundary

The original assignment and material notice are source documents, not editable design outputs. Original reports and presentation remain labelled historical submission records. Current margins, recommended dimensions and model definitions are in the Revision C technical report and the two-page Guild Assay Response.
