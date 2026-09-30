# Drakkar Ascent — corrected analytical design

Reproducible theoretical thrust-barrel study: no FEA or hardware testing.

**Primary all-metal candidate under the documented assumptions:** Magnesium AZ31B, 158 mm OD x 1.80 mm nominal wall, **2.878 kg modelled structural assembly**. This is a discrete-family result, not a flight-qualified or unrestricted global optimum. Composite shell candidates are kept separate because interface and ply-level data are missing.

Printable outputs: [full PDF report](output/pdf/Drakkar_Analytical_Report.pdf) and [one-page results summary](output/pdf/Drakkar_Results_Summary.pdf). Run `generate_outputs.py` to refresh the PDFs and a local ZIP bundle; the redundant ZIP is excluded from Git.

Start with the [complete solution](The_Drakkar_Ascent_Challenge_Solution.md), [design review notes](House_Veridian_Design_Review_Presentation.md), or [file guide](PROJECT_FILES_GUIDE_AND_EXPLANATION.md).

Python >= 3.10:

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

The model/tests need only the standard library. Graphics and PDF dependencies are pinned in `requirements.txt`. JSON/CSV files in `results/` are the numerical source; generators update canonical files in `assets/`. All equations in the report use plain text. The original research audit is preserved in [docs/RESEARCH_AUDIT.md](docs/RESEARCH_AUDIT.md).

Key assumptions: factor 1.5 on all loads, 95% wall thickness, 1.5 mm bow, conservative pressure cases and a provisional 0.35 shell/ovalisation cap. The report identifies empirical applicability limits and assumed joint behaviour explicitly. Change the `Basis` parameters in the model and rerun all generators when the course design basis changes.
