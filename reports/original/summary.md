# RESULTS SUMMARY — Lockheed Martian

**THE DRAKKAR ASCENT CHALLENGE**

| Team member | Roll number |
|---|---|
| Aryan Vyapari | 241030078 |
| Ashutosh Yadav | 241030079 |
| Rishiraj Rajgore | 241030067 |
| Archit More | 241030057 |

---

## 1. Design Basis

| Parameter | Value |
|---|---|
| Shell length | 1500 mm |
| Applied load factor (team-selected) | **1.1** — multiplies F, M, V and p before analysis |
| Required safety factor | 1.1 |
| Moment case | Brief (primary moment only) |
| Pressure path | Wall-only strength (no closed-end credit) |
| Diameter search range | 1 – 300 mm |
| Thickness step | 0.01 mm |

### Applied loads (after ×1.1 factor)

| Symbol | Value |
|---|---|
| Axial thrust P | 33 000 N |
| Shear V | 1 611.6 N |
| Internal pressure p | 330 000 Pa |
| Bending moment M | 3 027.9 N·m (first-order: 2 417.5 N·m) |

---

## 2. Selected Metal Design

### 2a. Primary moment case (bending only)

| Parameter | Value |
|---|---|
| Material | Aluminium 7075-T6 |
| Outside diameter | **119 mm** |
| Wall thickness | **0.96 mm** |
| Shell mass | **1.501 kg** |
| Governing failure mode | Shell interaction (local) |
| Governing utilisation U | 0.9962 |
| Strength utilisation | 0.7830 |
| Euler (column) utilisation | 0.1692 |
| Ovalisation utilisation | 0.7425 |
| r/t ratio | 61.5 |
| L/r ratio | 25.4 |

### 2b. Separate M + V·L case (transfer loads)

| Parameter | Value |
|---|---|
| Material | Aluminium 7075-T6 |
| Outside diameter | **137 mm** |
| Wall thickness | **1.10 mm** |
| Shell mass | **1.980 kg** |
| Governing failure mode | Shell interaction (local) |
| Governing utilisation U | 0.9956 |
| Strength utilisation | 0.8486 |
| Euler (column) utilisation | 0.0968 |
| Ovalisation utilisation | 0.8884 |
| r/t ratio | 61.8 |
| L/r ratio | 22.1 |

---

## 3. Full Material Trade — Primary Moment Case (LF = 1.1)

Optimal shell for each material at the team load factor. All candidates governed by shell interaction.

| Material | D (mm) | t (mm) | Mass (kg) | U |
|---|---|---|---|---|
| **Aluminium 7075-T6** ✓ | **119** | **0.96** | **1.501** | 0.9962 |
| Magnesium AZ31B | 169 | 1.10 | 1.540 | 0.9978 |
| Aramid/Epoxy QI | 169 | 1.23 | 1.361 | 0.9951 |
| Carbon/Epoxy QI | 101 | 1.20 | 0.903 | 0.9936 |
| Titanium Ti-6Al-4V | 96 | 0.84 | 1.669 | 0.9978 |
| Glass/Epoxy QI | 125 | 1.60 | 1.768 | 0.9955 |
| Steel 4130 | 154 | 0.58 | 3.292 | 0.9999 |

> **Carbon/Epoxy QI** achieves the minimum shell mass (0.903 kg) but was not selected as the primary metal candidate. Aluminium 7075-T6 is the primary metal selection at 1.501 kg.

---

## 4. Full Material Trade — Transfer Load Case (Separate M + V·L)

| Material | D (mm) | t (mm) | Mass (kg) | U |
|---|---|---|---|---|
| **Aluminium 7075-T6** ✓ | **137** | **1.10** | **1.980** | 0.9956 |
| Magnesium AZ31B | 199 | 1.23 | 2.029 | 0.9987 |
| Carbon/Epoxy QI | 113 | 1.40 | 1.178 | 0.9946 |
| Aramid/Epoxy QI | 195 | 1.40 | 1.788 | 0.9984 |
| Titanium Ti-6Al-4V | 111 | 0.96 | 2.205 | 0.9915 |
| Glass/Epoxy QI | 141 | 1.84 | 2.293 | 0.9988 |
| Steel 4130 | 183 | 0.65 | 4.385 | 0.9979 |

---

## 5. Sensitivity to Load Factor

Minimum-mass Aluminium 7075-T6 shell at five load factor levels:

| Load factor | D (mm) | t (mm) | Mass (kg) |
|---|---|---|---|
| 1.00 | 115 | 0.93 | 1.405 |
| **1.10** | **119** | **0.96** | **1.501** ← selected |
| 1.25 | 120 | 1.04 | 1.638 |
| 1.50 | 130 | 1.09 | 1.861 |
| 2.00 | 144 | 1.21 | 2.288 |

---

## 6. Pressure Scenario Utilisations

Pressure-only strength utilisation (no combined loads) for each material at the selected geometry:

| Material | Wall-only U | Closed-end U |
|---|---|---|
| Aluminium 7075-T6 | 0.783 | 0.763 |
| Titanium Ti-6Al-4V | 0.799 | 0.788 |
| Steel 4130 | 0.829 | 0.782 |
| Magnesium AZ31B | 0.826 | 0.770 |
| Carbon/Epoxy QI | 0.804 | 0.793 |
| Glass/Epoxy QI | 0.787 | 0.766 |
| Aramid/Epoxy QI | 0.764 | 0.709 |

All candidates pass wall-only pressure strength with utilisation < 1.0.

---

## 7. Assumptions and Scope

- Uniform nominal wall; pinned beam-column envelope.
- No pressure-stabilisation credit applied.
- Equivalent-QI quadratic failure model for composites.
- Mass includes the shell only (no end rings, fittings, or connections).
- Prescribed end rings retain circularity; shell stresses carry bending.
- Local interaction criterion governs all selected candidates.
- Transverse-shear interaction handled via surrogate; long-shell correlation extrapolated.
- Material strength cap active for Aluminium 7075-T6 (σ_bending_cr capped at yield).

---

## 8. Verification and Interpretation

- All **16 unit tests pass**. Independent arithmetic reproduces 14 detailed candidates and 35 load-scenario checks.
- Results satisfy the implemented analytical screen.
- **Model limitations:** inelastic capacity, transverse-shear interaction, and long-shell applicability not fully validated; a total-assembly optimum is not established.
- Full verification data: [`results/calculation_verification.json`](../results/calculation_verification.json)
- Raw trade sweeps: [`results/trade_study.csv`](../results/trade_study.csv), [`results/transfer_trade_study.csv`](../results/transfer_trade_study.csv)

---

## 9. Output Files

| File | Description |
|---|---|
| `output/pdf/Drakkar_Analytical_Report.pdf` | Full analytical report with equations and worked calculations |
| `output/pdf/Drakkar_Results_Summary.pdf` | PDF version of this summary |
| `assets/trade_study_diameter_vs_mass.png` | Shell mass vs. diameter sweep (all materials) |
| `assets/failure_modes_vs_diameter.png` | Failure mode utilisations vs. diameter |
| `assets/trade_materials_comparison_barchart.png` | Bar chart comparing all-material minima |
| `assets/thrust_barrel_cad_drawing.png` | Engineering drawing of thrust barrel |
| `results/design.json` | Full numerical results (JSON) |
| `results/trade_study.csv` | Diameter sweep data — primary case |
| `results/transfer_trade_study.csv` | Diameter sweep data — transfer case |

---

*Updated: 2026-09-30. All data sourced directly from `results/design.json` produced by `parametric_diameter_study.py`.*
