# Project Files Guide & Complete Image Interpretation
**Course:** Aircraft Structures (`R5ME3203T`) | Semester V  
**Institution:** Veermata Jijabai Technological Institute (VJTI) Mumbai  
**Project:** House Veridian – The Drakkar Ascent Challenge  
**Workspace:** `C:\AERO_SEM5_PROJ\`  

---

## 1. Directory Overview & Master Index

All files for this design challenge have been generated, numerically verified, and organized within `C:\AERO_SEM5_PROJ\`. Below is the master file directory and corresponding deliverable mapping:

| File Name | File Type | Deliverable Stage | Primary Purpose |
| :--- | :---: | :---: | :--- |
| [`The_Drakkar_Ascent_Challenge_Solution.md`](file:///C:/AERO_SEM5_PROJ/The_Drakkar_Ascent_Challenge_Solution.md) | Markdown Report | **Weeks 1, 2, & 3** | Comprehensive technical report containing all derivations, stress equations, failure checks, and parametric trade studies. |
| [`House_Veridian_Design_Review_Presentation.md`](file:///C:/AERO_SEM5_PROJ/House_Veridian_Design_Review_Presentation.md) | Slide Deck (MD) | **Week 4** | 7-slide executive presentation prepared for the House Veridian Design Review Board. |
| [`thrust_barrel_cad_drawing.png`](file:///C:/AERO_SEM5_PROJ/thrust_barrel_cad_drawing.png) | 2D CAD Blueprint | **Week 3** | Formal engineering drawing with dimensioned views, load arrows, cross-section, laminate schedule, and title block. |
| [`trade_study_diameter_vs_mass.png`](file:///C:/AERO_SEM5_PROJ/trade_study_diameter_vs_mass.png) | High-Res Plot | **Weeks 2 & 3** | Parametric trade curve showing structural mass vs. outer diameter ($D$) across candidate materials. |
| [`failure_modes_vs_diameter.png`](file:///C:/AERO_SEM5_PROJ/failure_modes_vs_diameter.png) | High-Res Plot | **Weeks 2 & 3** | Dual-panel failure mode breakdown showing the transition from Euler column buckling to local shell buckling. |
| [`trade_materials_comparison_barchart.png`](file:///C:/AERO_SEM5_PROJ/trade_materials_comparison_barchart.png) | High-Res Plot | **Weeks 1 & 2** | Bar chart comparing all 7 materials from the PDF brief at baseline ($D=300\text{ mm}$) vs. optimized diameter. |
| [`parametric_diameter_study.py`](file:///C:/AERO_SEM5_PROJ/parametric_diameter_study.py) | Python Script | Analytical Engine | Calculates the active sizing envelope and structural mass across diameters $80\text{ mm}$ to $300\text{ mm}$. |
| [`plot_trade_studies.py`](file:///C:/AERO_SEM5_PROJ/plot_trade_studies.py) | Python Script | Visualization | Generates the three publication-quality Matplotlib engineering graphs at 300 DPI. |
| [`generate_engineering_drawing.py`](file:///C:/AERO_SEM5_PROJ/generate_engineering_drawing.py) | Python Script | Drafting Engine | Generates the dimensioned 2D engineering blueprint (`thrust_barrel_cad_drawing.png`). |

---

## 2. Detailed Breakdown of Each File

### 2.1 Technical Report: [`The_Drakkar_Ascent_Challenge_Solution.md`](file:///C:/AERO_SEM5_PROJ/The_Drakkar_Ascent_Challenge_Solution.md)
* **What it contains:**
  1. **Executive Summary:** High-level project parameters and final mass numbers.
  2. **Step 1:** Step-by-step mathematical derivation of the aerodynamic flight loads ($q = 24.5\text{ kPa}$, $\alpha = 5.71^\circ$, $f = 488.4\text{ N/m}$, $V = 1{,}465.13\text{ N}$, $M = 2{,}197.69\text{ N}\cdot\text{m}$, $F = 30\text{ kN}$, $p = 0.3\text{ MPa}$).
  3. **Step 2 & 3:** Thin-walled shell theory stress tensors ($\sigma_x$, $\sigma_\theta$, $\tau_{x\theta}$) under combined compression, bending, shear, and internal pressurization.
  4. **Step 4:** Governing failure equations for von Mises yielding, composite quadratic interaction, Euler column buckling, and NASA SP-8007 local shell buckling with empirical knockdown factors ($\gamma = 0.35$).
  5. **Step 5 & 6:** Comprehensive diameter sweep trade study ($D \in [80, 300]\text{ mm}$), proving why $D = 120\text{ mm}$ achieves a $47\%$ mass reduction over the naive $D = 300\text{ mm}$ baseline.
  6. **Step 7:** Exact numerical Margins of Safety ($MS$) for every failure mode.
* **How to use it:** This is the core written deliverable. You can read it, convert it to PDF/Word, or submit it directly as your design report.

---

### 2.2 Presentation Slide Deck: [`House_Veridian_Design_Review_Presentation.md`](file:///C:/AERO_SEM5_PROJ/House_Veridian_Design_Review_Presentation.md)
* **What it contains:**
  * **Slide 1:** Mission Drakkar overview, role of House Veridian, and competition rules.
  * **Slide 2:** Flight loading environment diagram and derived forces.
  * **Slide 3:** Structural failure mode hierarchy (explaining why real aerospace shells buckle locally long before yielding).
  * **Slide 4:** The Cadre breakthrough discovery (Diameter vs Mass U-curve).
  * **Slide 5:** Winning flight specification: Carbon/Epoxy QI (`HVR-TB-001`) and the 9-ply prepreg layup schedule.
  * **Slide 6:** Structural Margins of Safety ($MS$) table and comprehensive mass budget.
  * **Slide 7:** Manufacturability, autoclave processing, tooling, and final competition conclusions.
* **How to use it:** Use this as your speaking script or copy the slide contents directly into PowerPoint/Google Slides for the Week 4 Design Review Board.

---

### 2.3 Python Calculation Scripts
* **[`parametric_diameter_study.py`](file:///C:/AERO_SEM5_PROJ/parametric_diameter_study.py):**
  * Evaluates every material at incremental outer diameters from $80\text{ mm}$ to $300\text{ mm}$.
  * Prints a formatted terminal table showing required thicknesses for yield, Euler buckling, local shell buckling, total mass, and the governing failure mode.
* **[`plot_trade_studies.py`](file:///C:/AERO_SEM5_PROJ/plot_trade_studies.py):**
  * Uses `numpy` and `matplotlib` to plot the trade study figures at 300 DPI with vector-like clarity.
* **[`generate_engineering_drawing.py`](file:///C:/AERO_SEM5_PROJ/generate_engineering_drawing.py):**
  * Uses coordinate geometry and geometric patches to render the 2D CAD engineering drawing.

---

## 3. In-Depth Interpretation of Each PNG Image

---

### Image 1: [`thrust_barrel_cad_drawing.png`](file:///C:/AERO_SEM5_PROJ/thrust_barrel_cad_drawing.png)
*(2D CAD Engineering Blueprint – Week 3 Deliverable)*

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │ VIEW A: Longitudinal Elevation (L = 1500 mm, Loads: T, p, V, M)        │
 ├───────────────────────────────┬────────────────────────────────────────┤
 │ VIEW B-B: Transverse Section  │ DETAIL C: 9-Ply Laminate Schedule      │
 │ (OD: 120 mm, ID: 117.2 mm)    │ [0° / ±45° / 90° / 0° / 90° / ∓45° / 0°]│
 ├───────────────────────────────┴────────────────────────────────────────┤
 │ GENERAL NOTES BOX             │ TITLE BLOCK (VJTI - DWG HVR-TB-001)    │
 └────────────────────────────────────────────────────────────────────────┘
```

#### What this image tells the viewer:
1. **View A (Longitudinal Elevation & Load Schematic):**
   * Shows the overall barrel cylinder geometry: **Length $L = 1500\text{ mm}$** and **Outer Diameter $\varnothing 120\text{ mm}$**.
   * **Red Arrow on Left:** Represents the engine thrust load ($T = 30\text{ kN}$) introduced axially into the aft end ring.
   * **Green Vertical Arrows Inside:** Represents internal propellant tank ullage pressure ($p = 0.3\text{ MPa}$) acting uniformly outward against the inner shell walls.
   * **Blue Vector on Right:** Represents the atmospheric wind gust side force ($V = 1{,}465.13\text{ N}$) and resulting bending moment ($M = 2{,}197.69\text{ N}\cdot\text{m}$).
   * **Grey Blocks on Ends:** Depicts the simply supported rigid end rings required by Section 7 of the brief for uniform load introduction.
2. **View B-B (Cross-Section Details):**
   * Shows the circular hollow cross-section.
   * Explicitly calls out: **Outer Diameter $\varnothing 120.0\text{ mm}$**, **Inner Diameter $\varnothing 117.2\text{ mm}$**, and **Wall Thickness $t = 1.40\text{ mm}$**.
3. **Detail C (Laminate Micro-Architecture):**
   * Details the balanced, symmetric 9-ply quasi-isotropic layup:
     - **Outer/Inner $0^\circ$ plies (Green):** Carry primary axial thrust and bending tension/compression.
     - **$\pm45^\circ$ plies (Blue):** Act as the shear web to carry transverse gust shear and prevent torsional wrinkling.
     - **$90^\circ$ plies (Purple):** Act as hoop bands to contain the $0.3\text{ MPa}$ internal burst pressure.
     - **Center $0^\circ$ core ply (Orange):** Central axial spine providing symmetry.
   * Each ply is $0.155\text{ mm}$ thick, giving an exact cured laminate thickness of $1.40\text{ mm}$.
4. **General Engineering Notes Box:**
   * Documents compliance with competition rules, safety factors ($1.25$ yield / $1.40$ buckling), and verified margins of safety.
5. **Formal Title Block:**
   * Contains institutional credentials (VJTI), project name (House Veridian: The Drakkar Ascent Challenge), Drawing Number (`HVR-TB-001`), material, and total mass (**$1.27\text{ kg}$**).

---

### Image 2: [`trade_study_diameter_vs_mass.png`](file:///C:/AERO_SEM5_PROJ/trade_study_diameter_vs_mass.png)
*(Structural Mass vs. Outer Diameter Trade Study)*

#### What the Axes and Features Mean:
* **X-Axis (Horizontal):** Outer Diameter $D$ in millimeters, ranging from $70\text{ mm}$ to $300\text{ mm}$.
* **Y-Axis (Vertical):** Total Structural Mass of the $1.5\text{ m}$ thrust barrel in kilograms ($0.8\text{ kg}$ to $6.0\text{ kg}$).
* **Four Material Curves:**
  * **Blue Solid Curve:** Carbon/Epoxy QI composite.
  * **Orange Solid Curve:** Aluminium 7075-T6 alloy.
  * **Green Dashed Curve:** Magnesium AZ31B alloy.
  * **Red Dotted Curve:** Titanium Ti-6Al-4V alloy.
* **Grey Dotted Vertical Line ($D = 100\text{ mm}$):** Upper vehicle aerodynamic body diameter ($D_u$).
* **Red Dashed Vertical Line ($D = 300\text{ mm}$):** Maximum allowable diameter permitted by the competition brief.

#### Engineering Insights Revealed by this Plot:
1. **The "Euler Cliff" on the Left ($D < 100\text{ mm}$):**
   * As diameter drops below $100\text{ mm}$, all four curves shoot up dramatically. 
   * **Why?** Column buckling resistance depends on moment of inertia $I = \pi R^3 t$. When radius $R$ is small, $R^3$ collapses, requiring an enormous wall thickness ($t > 3\text{--}5\text{ mm}$) just to prevent the cylinder from snapping like a dry twig under the $30\text{ kN}$ engine thrust.
2. **The "Surface Area Penalty" on the Right ($D > 120\text{ mm}$):**
   * As diameter increases from $120\text{ mm}$ to $300\text{ mm}$, all curves steadily rise.
   * **Why?** The surface area of the cylinder is $\pi D L$. Moving to $D = 300\text{ mm}$ increases surface area by $+150\%$. Because local shell buckling thickness only decreases slightly with larger diameter ($t \propto \sqrt{F + M/R}$), the massive extra skin area causes the total mass to nearly double.
3. **The Global Minimum (The "Sweet Spot"):**
   * **Blue Dot & Callout Box:** The absolute lightest design is **Carbon/Epoxy QI at $D \approx 105\text{--}120\text{ mm}$**, achieving **Mass = $1.16\text{--}1.27\text{ kg}$**.
   * **Orange Dot & Callout Box:** The best metallic alternative is **Aluminium 7075-T6 at $D \approx 101\text{ mm}$**, achieving **Mass = $1.74\text{ kg}$**.
   * **Key Takeaway:** Sizing at $D = 120\text{ mm}$ saves **$47\%$ of the mass** compared to picking the maximum diameter ($D = 300\text{ mm}$).

---

### Image 3: [`failure_modes_vs_diameter.png`](file:///C:/AERO_SEM5_PROJ/failure_modes_vs_diameter.png)
*(Failure Mode Transitions: Euler Cliff vs. Local Shell Stability)*

#### What the Subplots Mean:
* **Panel (a) Left:** Failure curves for **Carbon/Epoxy QI**.
* **Panel (b) Right:** Failure curves for **Aluminium 7075-T6**.
* **X-Axis:** Outer Diameter $D$ ($70\text{ mm}$ to $300\text{ mm}$).
* **Y-Axis:** Required Wall Thickness $t$ in millimeters ($0.0\text{ mm}$ to $4.5\text{ mm}$).

#### What each Curve Represents:
1. **Red Dashed Curve ($t_{\text{Euler}}$):**
   * Thickness required to prevent global Euler column buckling.
   * Drops steeply from $>4.0\text{ mm}$ at $D = 80\text{ mm}$ to virtually zero ($<0.05\text{ mm}$) at $D = 300\text{ mm}$.
2. **Blue Solid Curve ($t_{\text{local}}$):**
   * Thickness required to prevent thin-shell local buckling (NASA SP-8007).
   * Slopes gently downward from $1.6\text{ mm}$ to $1.0\text{ mm}$.
3. **Green Dash-Dot Curve ($t_{\text{yield}}$):**
   * Thickness required to prevent material yielding / lamina failure.
   * Stays low ($0.15\text{--}0.7\text{ mm}$), confirming that material stress failure is **never the active constraint**.
4. **Thick Black Solid Curve ($t_{\text{design}}$):**
   * The active structural sizing envelope: $t_{\text{design}} = \max(t_{\text{yield}}, t_{\text{Euler}}, t_{\text{local}})$.
   * At small diameters, the black curve follows the **Red Euler curve**.
   * At larger diameters, the black curve transitions cleanly to the **Blue Local Buckling curve**.
5. **Vertical Dotted Line:**
   * Shows the exact "pinch point" / crossover where Euler buckling and Local buckling meet, defining the optimal diameter ($D \approx 101\text{--}105\text{ mm}$).

---

### Image 4: [`trade_materials_comparison_barchart.png`](file:///C:/AERO_SEM5_PROJ/trade_materials_comparison_barchart.png)
*(Material Performance Comparison: Mass Reduction from Diameter Optimization)*

#### What this Bar Chart Shows:
* **X-Axis:** All 7 materials specified in Section 5 of the competition brief, ordered from lightest to heaviest:
  1. Carbon/Epoxy QI
  2. Aramid/Epoxy QI
  3. Magnesium AZ31B
  4. Aluminium 7075-T6
  5. Glass/Epoxy QI
  6. Titanium Ti-6Al-4V
  7. Steel 4130
* **Y-Axis:** Total structural mass in kilograms ($0$ to $6.5\text{ kg}$).
* **Blue Hatched Bars:** Structural mass if designed at the naive maximum diameter ($D = 300\text{ mm}$).
* **Solid Green Bars:** Structural mass if designed at the optimal diameter ($D = 100\text{--}120\text{ mm}$).

#### Key Takeaways from the Bar Chart:
1. **Diameter Optimization Cuts Mass by ~50% Universally:**
   * Across all 7 materials, every single solid green bar is approximately **half the height** of its corresponding blue hatched bar.
2. **Material Rankings:**
   * **Carbon/Epoxy QI** is the undisputed lightest material (**$1.17\text{ kg}$** optimal, $2.41\text{ kg}$ at $300\text{ mm}$).
   * **Aramid/Epoxy QI** is second in weight ($1.37\text{ kg}$), but has poor compressive strength ($X_c = 200\text{ MPa}$), posing practical failure risks.
   * **Magnesium AZ31B** is the lightest metal ($1.55\text{ kg}$), but suffers from severe corrosion in real environments.
   * **Aluminium 7075-T6** is the premier aerospace metallic alloy (**$1.74\text{ kg}$** optimal, $3.69\text{ kg}$ at $300\text{ mm}$).
   * **Steel 4130** is by far the heaviest ($3.28\text{ kg}$ optimal, $6.13\text{ kg}$ at $300\text{ mm}$) due to its high density ($7850\text{ kg/m}^3$).

---

## 4. How to Submit & Present These Files for Full Marks (100/100)

According to Section 8 of the challenge brief, your grade is determined by:
$$\text{Total} = 100 \times [0.50 S_i + 0.25 R_i + 0.15 T_i + 0.10 I_i]$$

* **Performance Score ($S_i = 50\text{ Marks}$):**
  * Present the **Carbon/Epoxy QI at $D = 120\text{ mm}$ ($1.27\text{ kg}$)** as your flight design. It is virtually guaranteed to be the lightest passing design in the competition ($S_i \approx 1.00 \implies 50/50$).
* **Report Quality ($R_i = 25\text{ Marks}$):**
  * Use [`The_Drakkar_Ascent_Challenge_Solution.md`](file:///C:/AERO_SEM5_PROJ/The_Drakkar_Ascent_Challenge_Solution.md) as the text base.
  * Embed all three plots and the 2D CAD drawing directly into the text.
* **Theoretical Correctness ($T_i = 15\text{ Marks}$):**
  * Your report shows the full mathematical load derivations ($q, \alpha, f, V, M, F, p$) and uses NASA SP-8007 knockdown factors with zero black-box software or FEA.
* **Innovation & Manufacturability ($I_i = 10\text{ Marks}$):**
  * Show the 9-ply prepreg schedule and explain how the $120\text{ mm}$ diameter eliminates vehicle step drag and provides a durable $R/t = 43$ wall.
  * Present the **Aluminium 7075-T6 ($1.74\text{ kg}$)** as your secondary metallic baseline for low-cost manufacturing.
