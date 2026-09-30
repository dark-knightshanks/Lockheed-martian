# Drakkar Ascent - requirement-led shell study

**Current status: service-load screening; competition compliance unresolved.** The lowest screened metal-shell mass is **Aluminium 7075-T6: 1.404759 kg**, 115 mm OD x 0.93 mm nominal wall. This is not total assembly mass or a final passing design.

The brief does not supply numerical safety factors, tolerances, imperfection amplitude or connection details. Unsupported numerical allowances and the assumed joint model have been removed. Geometry-dependent shell knockdowns remain because the brief requires them. All seven materials, both moment cases and illustrative load multipliers are included.

Read the [full report](The_Drakkar_Ascent_Challenge_Solution.md), [PDF report](output/pdf/Drakkar_Analytical_Report.pdf), [PDF summary](output/pdf/Drakkar_Results_Summary.pdf) or [file guide](PROJECT_FILES_GUIDE_AND_EXPLANATION.md). Results are in [JSON](results/design.json) and [CSV](results/trade_study.csv). Earlier assembly results remain in Git history at 472798d.

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

Python >= 3.10. Core calculations/tests use the standard library. Graphics/PDF dependencies are pinned. The ZIP bundle and local inspection files are excluded from Git. No FEA or physical testing is used.
