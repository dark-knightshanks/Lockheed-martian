# File guide

| File | Purpose |
|---|---|
| [Model](parametric_diameter_study.py) | Service-load shell mechanics, material search and explicit scenarios |
| [Results](results/design.json) | All seven materials; assembly mass and required safety factor explicitly unresolved |
| [Brief sweep](results/trade_study.csv) | Shell screening across diameter |
| [Transfer sweep](results/transfer_trade_study.csv) | Separate M + V*L scenario |
| [Full report](The_Drakkar_Ascent_Challenge_Solution.md) | Requirements, removed assumptions, equations and limitations |
| [Review notes](House_Veridian_Design_Review_Presentation.md) | Short presentation script |
| [Report generator](generate_report.py) | Regenerates Markdown reports |
| [Plot generator](plot_trade_studies.py) | Three current figures |
| [Drawing generator](generate_engineering_drawing.py) | Shell concept with unspecified end boundaries |
| [Output exporter](generate_outputs.py) | PDFs and local ZIP |
| [Tests](tests/test_analysis.py) | Mechanics checks and result consistency |
| [Historical audit](docs/RESEARCH_AUDIT.md) | Audit of the original research revision, not current results |

All current masses are shell-only. Historical assembly masses must not be combined with the current basis.
