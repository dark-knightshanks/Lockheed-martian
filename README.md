# Drakkar thrust-barrel solution

Analytical sizing of a 1.5 m circular thrust barrel under compression, bending, transverse shear and internal pressure, using the supplied B-basis properties. No finite element analysis is used.

## Solution

**Carbon/Epoxy QI, 122.0 mm outer diameter, 1.520 mm wall, 1.380765 kg shell mass.** The same shell satisfies the primary and transfer moment load cases within the documented homogeneous-shell model.

Read the [technical solution](reports/Solution.pdf) or its [Markdown source](reports/Solution.md). The [design basis](docs/DESIGN_BASIS.md) and [governing equations](docs/METHOD.md) define the assumptions and validity domain. Ring/connection geometry, total assembly mass and manufactured laminate qualification require additional physical inputs.

## Repository

| Path | Purpose |
| --- | --- |
| src/analysis.py | Material inputs, mechanics and numerical optimisation |
| src/solve.py | One selected design, load-case checks and search data |
| src/verify.py | Independent numerical verification in N/mm/MPa |
| src/report.py | Technical report generated from verified results |
| tests/test_analysis.py | Analytical and saved-result tests |
| data/solution.json | Selected geometry and supporting calculations |
| data/trade_study.csv | Material/diameter search record |
| data/verification.json | Independent verification results |
| docs/briefs/ | Assignment and material-property notice |
| reports/ | One solution in PDF and editable Markdown |

## Reproduction

Python >= 3.10. Analysis and tests use the standard library.

```sh
python3 src/solve.py
python3 src/verify.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/report.py
```

## Authors

Aryan Vyapari (241030078), Ashutosh Yadav (241030079), Rishiraj Rajgore (241030067), Archit More (241030057).
