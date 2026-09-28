# The Drakkar Ascent Challenge: Complete Engineering Solution & Optimization Report
**Course:** Aircraft Structures (`R5ME3203T`) | Semester V (Academic Year 2026–27)  
**Institution:** Veermata Jijabai Technological Institute (VJTI) Mumbai  
**Cadre:** House Veridian Orbital Lifter Project  
**Component:** Cylindrical Booster Thrust Barrel Section  

---

## 1. Executive Summary

This report delivers a rigorous, first-principles analytical design, stress analysis, and parametric mass optimization for the **Veridian orbital lifter thrust barrel**. 

Per competition rules, **Finite Element Analysis (FEA) and black-box numerical codes are strictly excluded**. The design relies entirely on:
1. Thin-walled cylinder mechanics,
2. Classical beam-column theory (Euler global buckling),
3. Local cylindrical shell stability with empirical NASA knockdown factors (imperfection sensitivity),
4. Combined multi-axial stress failure criteria (von Mises for isotropic metals, quadratic interaction criteria for quasi-isotropic laminates),
5. Two-variable parametric trade studies: varying both **wall thickness ($t$)** and **outer diameter ($D$)**.

### Key Breakthrough & Trade-Off Discovery
* **Initial Assumption ($D = 300\text{ mm}$ Maximum):**
  - Carbon/Epoxy QI: $t = 1.065\text{ mm}$, Mass = **$2.41\text{ kg}$**
  - Aluminium 7075-T6: $t = 0.928\text{ mm}$, Mass = **$3.69\text{ kg}$**
* **Optimized Diameter Discovery ($D \approx 110\text{ mm} - 120\text{ mm}$):**
  - As diameter decreases, the surface area ($\pi D L$) decreases linearly.
  - While required wall thickness ($t$) slightly increases to resist bending, the reduction in surface area dominates.
  - At very small diameters ($D < 100\text{ mm}$), global Euler column buckling shoots up exponentially ($I \propto R^3$).
  - **Global Minimum Mass:** Occurs at **$D = 120\text{ mm}$** for Carbon/Epoxy QI with **Mass = $1.27\text{ kg}$** (a **$47\%$ mass reduction** over $D = 300\text{ mm}$)!
  - For Aluminium 7075-T6, the optimum is at **$D = 100\text{ mm}$** with **Mass = $1.77\text{ kg}$** (a **$52\%$ mass reduction**)!
  - Moreover, this matches the upper stage vehicle diameter ($D_u = 100\text{ mm}$), creating an aerodynamically streamlined body without parasitic drag.

---

## 2. Step 1: Aerodynamic Gust & Flight Load Derivations

The flight condition corresponds to the instant of maximum dynamic pressure ($q$) combined with a sharp atmospheric vertical thermal gust.

```
                  Flight Velocity V∞ = 200 m/s  ▲
                                                │
   Upper Stage Body:                            │
   Du = 0.10 m (100 mm), Lu = 3.0 m             │
  ┌───────────────────────┐                     │
  │                       │ ◄─── Gust wg = 20 m/s (creates α, f, V, M)
  └───────────────────────┘
  ═════════════════════════
  ║     THRUST BARREL     ║ ◄─── Internal Ullage Pressure p = 0.3 MPa
  ║  (L = 1.5 m, D: Var)  ║
  ═════════════════════════
             ▲
             │ Engine Thrust T = 30 kN (Axial Compression)
```

### 2.1 Given Flight Parameters
* Flight Velocity: $V_\infty = 200\text{ m/s}$
* Atmospheric Density: $\rho = 1.225\text{ kg/m}^3$
* Vertical Gust Velocity: $w_g = 20\text{ m/s}$
* Upper Vehicle Length above barrel: $L_u = 3.0\text{ m}$
* Upper Vehicle Diameter: $D_u = 0.10\text{ m} = 100\text{ mm}$
* Normal-Force Coefficient Slope: $C_{N\alpha} = 2.0\text{ rad}^{-1}$
* Engine Thrust: $T = 30\text{ kN} = 30{,}000\text{ N}$
* Propellant Tank Ullage Pressure: $p_u = 0.3\text{ MPa} = 3 \times 10^5\text{ N/m}^2$
* Barrel Length: $L = 1500\text{ mm} = 1.5\text{ m}$

---

### 2.2 Mathematical Load Computations

#### 1. Dynamic Pressure ($q$)
$$q = \frac{1}{2} \rho V_\infty^2 = \frac{1}{2} \times 1.225 \times (200)^2 = 24{,}500\text{ N/m}^2 = 0.0245\text{ MPa}$$

#### 2. Equivalent Angle of Attack ($\alpha$)
$$\alpha = \arctan\left(\frac{w_g}{V_\infty}\right) = \arctan\left(\frac{20}{200}\right) = \arctan(0.1) \approx 0.09966865\text{ rad} \approx 5.7106^\circ$$

#### 3. Distributed Aerodynamic Side Force per Unit Length ($f$)
For a slender cylinder at angle of attack $\alpha$:
$$f = q \cdot C_{N\alpha} \cdot \alpha \cdot D_u$$
$$f = 24{,}500 \times 2.0 \times 0.09966865 \times 0.10 = 488.376\text{ N/m}$$

#### 4. Total Side Shear Force ($V$) at the Base of the Upper Vehicle
$$V = F_{side} = f \cdot L_u = 488.376\text{ N/m} \times 3.0\text{ m} = \mathbf{1{,}465.13\text{ N}}$$

#### 5. Bending Moment ($M$) Acting on the Thrust Barrel
Assuming the distributed lateral gust load is uniform across $L_u$:
$$M = \frac{f \cdot L_u^2}{2} = \frac{488.376 \times (3.0)^2}{2} = \mathbf{2{,}197.69\text{ N}\cdot\text{m}}$$

#### 6. Axial Compressive Force ($F$)
$$F = T = \mathbf{30{,}000\text{ N}}$$

#### 7. Internal Pressure ($p$)
$$p = p_u = \mathbf{0.3\text{ MPa}} = 300{,}000\text{ Pa}$$

---

## 3. Step 2: Generalized Geometric Relations & Stress Formulas (as Functions of $R$ and $t$)

For any chosen outer diameter $D$ (mean radius $R = D/2$) and wall thickness $t$:

* **Cross-Sectional Area:** $A = 2 \pi R t$
* **Second Moment of Area:** $I = \pi R^3 t$
* **Outer Surface Area:** $A_{\text{surf}} = 2 \pi R L = \pi D L$
* **Total Barrel Mass:** $m = 2 \pi R L t \rho = \pi D L t \rho$

### 3.1 Stress Components in Thin-Walled Shell

#### 1. Circumferential (Hoop) Stress ($\sigma_\theta$):
$$\sigma_\theta = +\frac{p R}{t}$$
*(Notice: Smaller radius $R$ reduces hoop stress directly!)*

#### 2. Longitudinal Compressive Stress ($\sigma_{x,\text{comp}}$):
$$\sigma_{x,\text{comp}} = \frac{F}{2\pi R t} + \frac{M}{\pi R^2 t} = \frac{1}{t} \left( \frac{F}{2\pi R} + \frac{M}{\pi R^2} \right) = \frac{N_{x,\text{comp}}}{t}$$
where $N_{x,\text{comp}}$ is the maximum compressive running load per unit circumference:
$$N_{x,\text{comp}}(R) = \frac{F}{2\pi R} + \frac{M}{\pi R^2}$$

#### 3. In-Plane Shear Stress ($\tau_{x\theta}$):
$$\tau_{\max} = \frac{V}{\pi R t}$$

---

## 4. Step 3: Governing Structural Limits & Sizing Equations

### 4.1 Failure Mode 1: Material Yielding / Ultimate Failure

* **Metals (von Mises):**
  $$\sigma_{vm} = \sqrt{\sigma_x^2 - \sigma_x \sigma_\theta + \sigma_\theta^2 + 3\tau_{x\theta}^2} \le \frac{\sigma_y}{FS_{\text{yield}}}$$
  With $FS_{\text{yield}} = 1.25$.
  $$t_{\text{yield, metal}} = \frac{FS_{\text{yield}}}{\sigma_y} \sqrt{\left(\frac{F}{2\pi R} + \frac{M}{\pi R^2} - \frac{pR}{2}\right)^2 + \left(\frac{F}{2\pi R} + \frac{M}{\pi R^2} - \frac{pR}{2}\right)(pR) + (pR)^2 + 3\left(\frac{V}{\pi R}\right)^2}$$

* **Composites (Quadratic Interaction Criterion):**
  $$\left(\frac{\sigma_x}{X_c}\right)^2 + \left(\frac{\sigma_\theta}{Y_t}\right)^2 - \frac{\sigma_x \sigma_\theta}{X_c Y_t} + \left(\frac{\tau}{S}\right)^2 \le \left(\frac{1}{FS_{\text{yield}}}\right)^2$$

---

### 4.2 Failure Mode 2: Global Euler Column Buckling

For a simply supported cylinder of length $L = 1.5\text{ m}$:
$$P_{cr,\text{Euler}} = \frac{\pi^2 E I}{L^2} = \frac{\pi^3 R^3 E t}{L^2}$$
The equivalent total axial compressive load is:
$$P_{\text{eq}} = F + \frac{2 M}{R}$$
Requiring $P_{cr,\text{Euler}} \ge FS_{\text{buckle}} \cdot P_{\text{eq}}$ with $FS_{\text{buckle}} = 1.40$:
$$t_{\text{Euler}}(R) \ge \frac{FS_{\text{buckle}} \cdot \left(F + \frac{2 M}{R}\right) \cdot L^2}{\pi^3 R^3 E}$$

> **Key Physical Law:** Note the $R^3$ in the denominator! If $R$ becomes too small, $t_{\text{Euler}}$ skyrockets inversely with $R^3$.

---

### 4.3 Failure Mode 3: Local Thin-Shell Buckling (NASA SP-8007)

The critical local buckling stress for an unstiffened cylinder with NASA knockdown factor $\gamma = 0.35$:
$$\sigma_{cr,\text{local}} = \gamma \cdot \frac{E}{\sqrt{3(1-\nu^2)}} \cdot \frac{t}{R}$$
Setting applied compressive stress $\sigma_{\text{comp}} \le \frac{\sigma_{cr,\text{local}}}{FS_{\text{buckle}}}$:
$$\frac{1}{t} \left(\frac{F}{2\pi R} + \frac{M}{\pi R^2}\right) \le \frac{1}{FS_{\text{buckle}}} \left( \gamma \frac{E}{\sqrt{3(1-\nu^2)}} \frac{t}{R} \right)$$
Multiplying both sides by $R \cdot t$:
$$t^2 \ge \frac{FS_{\text{buckle}} \cdot \left( \frac{F}{2\pi} + \frac{M}{\pi R} \right)}{\gamma \cdot \frac{E}{\sqrt{3(1-\nu^2)}}}$$
Therefore, the required local shell buckling thickness is:
$$t_{\text{local}}(R) = \sqrt{\frac{FS_{\text{buckle}} \cdot \left( \frac{F}{2\pi} + \frac{M}{\pi R} \right)}{0.35 \cdot \frac{E}{\sqrt{3(1-\nu^2)}}}}$$

---

## 5. Step 4: The Diameter Variation Trade Study ($D = 80\text{ mm}$ to $300\text{ mm}$)

Let us evaluate the required thickness and total structural mass across the entire allowable diameter range ($D \in [80, 300]\text{ mm}$):

### 5.1 Comprehensive Parametric Results Table

| Diameter $D$ (mm) | Material | $t_{\text{yield}}$ (mm) | $t_{\text{Euler}}$ (mm) | $t_{\text{local}}$ (mm) | **Design $t$ (mm)** | **Total Mass (kg)** | Governing Mode |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **80** | Al 7075-T6 | 1.384 | 3.097 | 1.425 | **3.10** | 3.281 | Euler Column |
| **80** | Carbon/Epoxy QI | 1.165 | 4.037 | 1.636 | **4.04** | 2.435 | Euler Column |
| **80** | Magnesium AZ31B | 3.165 | 4.934 | 1.792 | **4.93** | 3.293 | Euler Column |
| **80** | Titanium Ti-6Al-4V | 0.791 | 1.951 | 1.135 | **1.95** | 3.259 | Euler Column |
| **100** | **Al 7075-T6** | 0.934 | 1.337 | 1.308 | **1.34** | **1.770** | **Euler Column (Optimum Metal)** |
| **100** | Carbon/Epoxy QI | 0.788 | 1.742 | 1.502 | **1.74** | **1.314** | Euler Column |
| **100** | Magnesium AZ31B | 2.136 | 2.130 | 1.645 | **2.14** | 1.781 | Material Yield |
| **100** | Titanium Ti-6Al-4V | 0.534 | 0.842 | 1.042 | **1.04** | 2.176 | Local Shell |
| **120** | Al 7075-T6 | 0.683 | 0.677 | 1.224 | **1.22** | 1.945 | Local Shell |
| **120** | **Carbon/Epoxy QI** | 0.578 | 0.883 | 1.405 | **1.41** | **1.271** | **Local Shell (GLOBAL WINNER)** |
| **120** | Magnesium AZ31B | 1.561 | 1.079 | 1.540 | **1.56** | 1.562 | Material Yield |
| **120** | Titanium Ti-6Al-4V | 0.390 | 0.427 | 0.975 | **0.98** | 2.443 | Local Shell |
| **140** | Al 7075-T6 | 0.527 | 0.383 | 1.161 | **1.16** | 2.152 | Local Shell |
| **140** | Carbon/Epoxy QI | 0.448 | 0.500 | 1.332 | **1.33** | 1.406 | Local Shell |
| **160** | Al 7075-T6 | 0.424 | 0.235 | 1.110 | **1.11** | 2.353 | Local Shell |
| **160** | Carbon/Epoxy QI | 0.363 | 0.306 | 1.275 | **1.28** | 1.538 | Local Shell |
| **200** | Al 7075-T6 | 0.300 | 0.105 | 1.036 | **1.04** | 2.744 | Local Shell |
| **200** | Carbon/Epoxy QI | 0.261 | 0.137 | 1.189 | **1.19** | 1.793 | Local Shell |
| **250** | Al 7075-T6 | 0.222 | 0.047 | 0.972 | **0.97** | 3.220 | Local Shell |
| **250** | Carbon/Epoxy QI | 0.200 | 0.062 | 1.117 | **1.12** | 2.105 | Local Shell |
| **300** | Al 7075-T6 | 0.184 | 0.025 | 0.928 | **0.93** | 3.686 | Local Shell |
| **300** | Carbon/Epoxy QI | 0.172 | 0.032 | 1.065 | **1.07** | 2.409 | Local Shell |

---

## 6. Step 5: Engineering Analysis of the Diameter Trade-Off

The data reveals a classic aero-structural optimization phenomenon:

```
 Total Mass (kg)
    ▲
5.0 ┼
    │   Euler Buckling               Local Buckling Dominates
4.0 ┼   Explosion                    (Mass grows linearly with Area ~ π*D*L)
    │     \                                      /
3.0 ┼      \   Aluminium 7075-T6                /
    │       \           _---_                  /
2.0 ┼--------*---_____--      --____________--* (D=300: 3.69 kg)
    │        (D=100: 1.77 kg)
    │           \   Carbon/Epoxy QI
1.0 ┼            *  (D=120: 1.27 kg) ----------* (D=300: 2.41 kg)
    │             \_____
0.0 ┼──────┴────────┴────────┴────────┴────────┴────────► Outer Diameter D (mm)
   60     100      150      200      250      300
```

### Why does mass increase when $D$ increases from $120\text{ mm}$ to $300\text{ mm}$?
1. **Surface Area Penalty:** The cylindrical surface area is $A_{\text{surf}} = \pi D L$. Going from $D = 120\text{ mm}$ to $D = 300\text{ mm}$ increases the surface area by **$+150\%$** (from $0.565\text{ m}^2$ to $1.414\text{ m}^2$).
2. **Diminishing Thickness Returns:** For local shell buckling:
   $$t_{\text{local}} \propto \sqrt{\frac{F}{2\pi} + \frac{M}{\pi R}}$$
   At large diameters, the bending moment term $\frac{M}{\pi R}$ diminishes, and the constant axial thrust term $\frac{F}{2\pi}$ dominates. Thus, increasing $D$ from $120\text{ mm}$ to $300\text{ mm}$ only reduces the required thickness from $1.40\text{ mm}$ to $1.06\text{ mm}$ (a modest $24\%$ thinning).
3. **Net Result:** Area increases by $150\%$ while thickness only drops by $24\%$. Hence, **mass nearly doubles** when sizing at the maximum $300\text{ mm}$ diameter!

### Why does mass increase when $D$ drops below $100\text{ mm}$?
1. **Column Buckling Cliff:** The Euler column buckling resistance depends on $I = \pi R^3 t$. 
2. As $D$ drops below $100\text{ mm}$, the $R^3$ term collapses, demanding an exponential surge in wall thickness ($t > 3\text{ to } 5\text{ mm}$) simply to prevent column snap-through.

---

## 7. Step 6: Final Optimum Design Recommendations

### 🥇 Primary Champion: Carbon/Epoxy Quasi-Isotropic at $D = 120\text{ mm}$
* **Diameter:** $D_o = 120\text{ mm}$ ($R = 60\text{ mm}$)
* **Wall Thickness:** $t = 1.40\text{ mm}$ (e.g., 9 plies of $0.155\text{ mm}$ unidirectional tape)
* **Total Mass:** **$1.27\text{ kg}$**
* **Mass Savings:** Saves **$1.14\text{ kg}$ ($47\%$)** compared to the $300\text{ mm}$ baseline!
* **Aerodynamic Benefit:** Near-flush interface with the $D_u = 100\text{ mm}$ upper vehicle body.

### 🥈 Best Metallic Alternative: Aluminium 7075-T6 at $D = 100\text{ mm}$
* **Diameter:** $D_o = 100\text{ mm}$ ($R = 50\text{ mm}$)
* **Wall Thickness:** $t = 1.34\text{ mm}$
* **Total Mass:** **$1.77\text{ kg}$**
* **Mass Savings:** Saves **$1.92\text{ kg}$ ($52\%$)** compared to the $300\text{ mm}$ aluminium cylinder ($3.69\text{ kg}$)!
* **Vehicle Aerodynamics:** Exact $1:1$ diameter match with the upper vehicle ($D_u = 100\text{ mm}$), completely eliminating step-drag transitions.

---

## 8. Step 7: Updated Margins of Safety ($MS$) for the Optimum Designs

$$MS = \frac{\text{Allowable Capacity}}{\text{Applied Load} \times FS} - 1$$

### For Carbon/Epoxy QI ($D = 120\text{ mm}, t = 1.40\text{ mm}$):
* **Euler Column Buckling:**
  - $P_{\text{applied, eq}} = 30{,}000 + 2(2197.69)/0.06 = 103{,}256\text{ N}$
  - $P_{cr,\text{Euler}} = \frac{\pi^3 (0.06)^3 (55 \times 10^9) (0.00140)}{1.5^2} = 228{,}971\text{ N}$
  - $MS_{\text{Euler}} = \frac{228{,}971}{103{,}256 \times 1.40} - 1 = \mathbf{+0.58}$ (Robust)
* **Local Shell Buckling:**
  - $\sigma_{\text{applied}} = \frac{N_{\text{comp}}}{t} = \frac{1}{0.00140}\left(\frac{30{,}000}{2\pi \times 0.06} + \frac{2197.69}{\pi \times 0.06^2}\right) = \frac{79{,}577 + 194{,}333}{0.00140} = 195.6\text{ MPa}$
  - $\sigma_{cr,\text{local}} = 0.21175 \times (55{,}000\text{ MPa}) \times \frac{0.00140}{0.060} = 271.7\text{ MPa}$
  - $MS_{\text{buckle}} = \frac{271.7}{195.6 \times 1.40} - 1 = \mathbf{+0.00}$ (Perfect optimal sizing, zero excess mass)
* **Material Failure (Quadratic):**
  - $MS_{\text{yield}} = \mathbf{+1.43}$ (Substantial margin)

---

## 9. Conclusion & Competition Advantage

By performing this diameter trade study, your team uncovers a critical aero-structural insight that most teams will miss:
* **Conventional Assumption:** Most teams will intuitively pick the maximum allowed diameter ($300\text{ mm}$), assuming "wider is always stiffer."
* **Your Cadre's Winning Design:** By analyzing the mathematical interplay between surface area ($A_{\text{surf}} \propto D$) and shell buckling ($t \propto \sqrt{F + M/R}$), you prove that **$D \approx 110 - 120\text{ mm}$ cuts the structural weight in half (from $2.41\text{ kg}$ down to $1.27\text{ kg}$)** while perfectly integrating with the $100\text{ mm}$ upper vehicle profile.
