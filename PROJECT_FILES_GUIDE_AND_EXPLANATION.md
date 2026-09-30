# Project file guide

The corrected solution is generated from one calculation model. All file links are repository-relative.

| File | Purpose |
|---|---|
| [Solution report](The_Drakkar_Ascent_Challenge_Solution.md) | Design basis, readable equations, assumptions, selected designs, margins and sources |
| [Design review notes](House_Veridian_Design_Review_Presentation.md) | Seven-part presentation script with generated numerical tables |
| [Analytical model](parametric_diameter_study.py) | Standard-library mechanics, connection model, discrete search and sensitivities |
| [Numerical results](results/design.json) | Full selected candidates, material minima and assumptions |
| [Primary sweep](results/trade_study.csv) | Best candidate at each diameter for the brief moment |
| [Transfer sweep](results/transfer_trade_study.csv) | Separate larger moment-transfer envelope |
| [Plot generator](plot_trade_studies.py) | Three figures generated from JSON/CSV, no duplicated mechanics |
| [Concept drawing generator](generate_engineering_drawing.py) | Selected primary design dimensions, not a manufacturing release |
| [PDF/package exporter](generate_outputs.py) | Printable report, summary and local ZIP generated from current results |
| [Report generator](generate_report.py) | Keeps solution and review notes consistent with results |
| [Verification cases](tests/test_analysis.py) | Independent limits, numerical checks and output consistency |
| [Historical audit](docs/RESEARCH_AUDIT.md) | Findings against the old research commit; historical numbers are not current results |

Canonical figures:

- [Diameter trade](assets/trade_study_diameter_vs_mass.png): metal assembly mass and composite shell-only mass in separate panels.
- [Checks and mass](assets/failure_modes_vs_diameter.png): selected candidates' utilisations and mass breakdown. Filename retained; obsolete Euler-cliff interpretation removed.
- [Materials and sensitivity](assets/trade_materials_comparison_barchart.png): metal assembly minima and assumption sensitivity.
- [Concept drawing](assets/thrust_barrel_cad_drawing.png): primary brief-moment design only.

Read the report's applicability statements before treating a numerical pass as a validated structural design. The composite plots deliberately exclude unknown joint mass; do not compare their shell-only ordinate directly with metal assembly mass.
