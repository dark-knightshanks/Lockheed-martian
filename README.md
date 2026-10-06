# Drakkar thrust-barrel structural analysis

Revision C | VJTI Aircraft Structures R5ME3203T | Lockheed Martian

Analytical optimisation of a 1.5 m circular thrust barrel under compression, bending, transverse shear and internal pressure. The material-quality revision uses the 3 October 2026 B-basis properties. No finite element analysis is used.

## Current technical deliverables

- [Guild Assay Response - two pages](reports/guild_assay/Guild_Assay_Response.pdf).
- [Technical report](reports/guild_assay/Technical_Report.pdf) and [editable Markdown](reports/guild_assay/Technical_Report.md).
- [Governing equations and applicability](docs/METHOD.md).
- [Design basis and system boundary](docs/DESIGN_ASSUMPTIONS.md).
- [Independent verification](docs/CALCULATION_VERIFICATION.md).
- [Numerical results](data/guild_assay/response.json).

The nominal-grid effective-QI solution satisfying both reported moment cases is **Carbon/Epoxy QI, D = 122.0 mm, t = 1.520 mm, shell mass 1.380765 kg**. The metal alternative is Magnesium AZ31B, 194.0 x 1.420 mm, 2.280940 kg. Acceptance applies to the defined homogeneous-shell model with ideal rigid end boundaries; total assembly mass and manufactured laminate qualification are not outputs of this model.

## Reproduction

Python >= 3.10. Analysis, verification and tests use the standard library. Report generation requires the pinned dependencies in `requirements.txt`.

```sh
python3 src/guild_assay.py
python3 src/verify_revised.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/generate_assay_response.py
```

## Repository structure

| Directory | Contents |
| --- | --- |
| src/ | Revised and baseline mechanics, verification and document generators |
| tests/ | Baseline and revised regression / analytical checks |
| data/guild_assay/ | Current material study, sweeps and independent verification |
| data/original/ | Revision A numerical reference data |
| docs/ | Governing method, design basis and verification record |
| docs/briefs/ | Original assignment and material-quality notice |
| docs/history/ | Historical method audit and baseline verification |
| reports/guild_assay/ | Current response and detailed technical report |
| reports/original/ | Original report, figures and editable presentation |

## Revision A reference

The [original report](reports/original/Drakkar_Analytical_Report.pdf), [summary](reports/original/Drakkar_Results_Summary.pdf) and [presentation](reports/original/slides/Design_Review.pptx) describe the original clean-material submission. They do not represent the revised design. `src/parametric_diameter_study.py` regenerates that baseline. `src/verify_calculations.py` audits it and writes the historical verification record. The baseline figure generators likewise use only `data/original/`.

## Authors

Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).
