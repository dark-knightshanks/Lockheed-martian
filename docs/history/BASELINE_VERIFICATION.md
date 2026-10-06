# Revision A calculation verification

**Verdict: the audited arithmetic reproduces the Revision A model. A complete structural pass is NOT verified.** The model has unresolved applicability issues, and the Revision A selected shell is a factor-1.1 result, not a factor-1.5 design.

This audit independently uses N/mm/MPa rather than the production model's SI units. It does not import the production calculation functions. Section properties use factored diameter formulas; material failure uses 7,200 angular samples. A 1,000-term analytical sine-series solution of EI*y'' + P*y = -M0 independently checks the secant beam moment. No FEA is used. Largest relative moment difference across the 35 load-scenario checks: 1.558e-11.

Scope: 14 stored baseline/transfer finalists checked against their detailed outputs; 35 load-scenario candidate masses and numerical passes rechecked; saved CSV minima compared with JSON. This is not a proof of an unrestricted global optimum or a fresh exhaustive search over every possible architecture.

## 1. Load derivation

```text
q = 0.5*1.225*200^2 = 24500.000000 N/m^2
alpha = atan(20/200) = 0.099668652491 rad
f = q*2*alpha*0.1 = 488.376397207 N/m
V = f*3 = 1465.129191620 N
M = f*3^2/2 = 2197.693787430 N m
F = 30000 N
p = 0.3 MPa = 0.3 N/mm^2
Separate transfer scenario: M+V*1.5 = 4395.387574860 N m
```

## 2. All-material factor-1.1 results

| Material | D mm | t mm | kg shell | Strength U | Euler U | Local U | Oval U |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Aluminium 7075-T6 | 119 | 0.96 | 1.500541 | 0.783024 | 0.169212 | 0.996228 | 0.742542 |
| Titanium Ti-6Al-4V | 96 | 0.84 | 1.668701 | 0.798686 | 0.232551 | 0.997777 | 0.838892 |
| Steel 4130 | 154 | 0.58 | 3.291704 | 0.828725 | 0.044617 | 0.999880 | 0.468665 |
| Magnesium AZ31B | 169 | 1.10 | 1.540486 | 0.826306 | 0.081764 | 0.997834 | 0.557203 |
| Carbon/Epoxy QI | 101 | 1.20 | 0.902969 | 0.803813 | 0.291970 | 0.993611 | 0.894534 |
| Glass/Epoxy QI | 125 | 1.60 | 1.767787 | 0.786806 | 0.254835 | 0.995485 | 0.843180 |
| Aramid/Epoxy QI | 169 | 1.23 | 1.361409 | 0.763659 | 0.094232 | 0.995141 | 0.585302 |

U <= 1 means a pass of the implemented numerical screen only. All masses exclude rings and connections. QI candidates are equivalent-material screens, not established ply-level laminate designs.

## 3. Verification findings

- **Safety-factor distinction:** the saved baseline multiplier is 1.1, adopted by the team. The factor 1.5 is a sensitivity case only. Keeping D = 119 mm and t = 0.96 mm while multiplying all loads by 1.5 gives strength U = 1.143172, local U = 1.433975, oval U = 1.109593: numerical FAIL.
- **Elastic/plastic capacity issue:** the selected aluminium elastic bending-buckling prediction is 511.291734 MPa, compared with the supplied 503 MPa yield. The code caps predicted capacities at yield when exceeded. That reproduces the code but is not the tangent/secant-modulus plasticity treatment described by NASA. Stress-strain/proportional-limit data or an appropriately justified alternative are needed. A cap cannot establish conservative inelastic capacity.
- **Long-shell applicability:** L/r = 25.415114. NASA warns about its axial correlation beyond L/r = 5 and calls for global/local interaction assessment. A separate Euler check plus secant amplification does not prove that coupled shell-column instability is covered.
- **Transverse-shear surrogate:** the imported shear capacity is for torsion. The sum of compression, bending and peak transverse-shear ratios is not demonstrated to be an exact or validated combined-load criterion for this barrel. The Air Force manual distinguishes transverse shear and torsion.
- **Pressure and ovalisation:** pressure enters strength. Buckling/ovalisation benefits are omitted; the ideal Brazier diagnostic does not solve the full pressurised finite-length response.
- **Composite failure:** a diagonal quadratic equation and QI tensile equivalence are declared choices. Uniaxial allowables alone do not verify the selected interaction coefficients or ply failure.
- **Output terminology:** JSON `validity: true` only tests the coded geometry/shear-formula ranges. It does not establish the long-shell, inelastic or composite applicability conditions above. `passes: true` is explicitly only a screen; competition compliance remains unresolved.
- **Missing assembly:** no ring/connection/manufacturing mass is established; 1.1 is the adopted team factor, not an instructor-specified value.

These findings prevent a claim that the Revision A establishes complete assembly compliance, despite numerical agreement. This audit verifies the archived Revision A numerical dataset. Revision C is specified in docs/METHOD.md.

## 4. Fully substituted factor-1.1 calculations

### Aluminium 7075-T6 - brief, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 71700; nu = 0.33; density = 2810 kg/m^3
D = 119.000; t = 0.960; L = 1500
Di = D - 2t = 117.080000
r = (D + Di)/4 = 59.020000
A = pi*t*(D-t) = 356.000252957
I = A*(D^2+Di^2)/16 = 620079.602998555
m = A*1500*density/10^9 = 1.500541066 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 2417463.166173
Pcr = pi^2*E*I/1500^2 = 195022.100070
beta = (pi/2)*sqrt(P/Pcr) = 0.646152357
M = M0/cos(beta) = 3027860.298199
amplification = 1.252494905
Midpoint beam deflection from Fourier check = 18.496883 mm
Euler U = P/Pcr = 0.169211592

Compression stress P/A = 92.696563
Bending stress M*(D/2)/I = 290.539613
Hoop stress p*(D/2)/t = 20.453125
Peak transverse shear 2V/A = 9.054163
sx(theta) = -92.696563 + 290.539613*cos(theta)
tau(theta) = 9.054163*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-383.236176)^2 + (20.453125)^2 - (-383.236176)*(20.453125)] / 503
                    = 0.783024329
Squared material utilisation = 0.613127100

r/t = 61.479167; L/r = 25.415114
phi = sqrt(r/t)/16 = 0.490054073
gx = 1-0.901*(1-exp(-phi)) = 0.650946535
gb = 1-0.731*(1-exp(-phi)) = 0.716805679
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 713.291969
raw axial buckling stress = gx*classical = 464.314936
raw bending buckling stress = gb*classical = 511.291734
Code's capped axial / bending capacities = 464.314936 / 503.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 37486.535232
gamma_s^(3/4) = 0.67; gamma_s*Z = 21977.335532
Moderate-length torsion range: 50 < gamma_s*Z < 262710.233605
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 41.348387
Code's local interaction = compression + bending + shear ratios
                        = 0.199641571 + 0.577613544 + 0.218972576
                        = 0.996227692
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 4077695.179174
U_oval = M/M_Brazier = 0.742542089
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Titanium Ti-6Al-4V - brief, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 113800; nu = 0.31; density = 4430 kg/m^3
D = 96.000; t = 0.840; L = 1500
Di = D - 2t = 94.320000
r = (D + Di)/4 = 47.580000
A = pi*t*(D-t) = 251.121323809
I = A*(D^2+Di^2)/16 = 284273.456941621
m = A*1500*density/10^9 = 1.668701197 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 2417463.166173
Pcr = pi^2*E*I/1500^2 = 141904.379878
beta = (pi/2)*sqrt(P/Pcr) = 0.757493563
M = M0/cos(beta) = 3327270.427948
amplification = 1.376347931
Midpoint beam deflection from Fourier check = 27.569917 mm
Euler U = P/Pcr = 0.232550962

Compression stress P/A = 131.410585
Bending stress M*(D/2)/I = 561.814607
Hoop stress p*(D/2)/t = 18.857143
Peak transverse shear 2V/A = 12.835566
sx(theta) = -131.410585 + 561.814607*cos(theta)
tau(theta) = 12.835566*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-693.225192)^2 + (18.857143)^2 - (-693.225192)*(18.857143)] / 880
                    = 0.798685811
Squared material utilisation = 0.637899025

r/t = 56.642857; L/r = 31.525851
phi = sqrt(r/t)/16 = 0.470384057
gx = 1-0.901*(1-exp(-phi)) = 0.661910813
gb = 1-0.731*(1-exp(-phi)) = 0.725701225
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 1220.046237
raw axial buckling stress = gx*classical = 807.561796
raw bending buckling stress = gb*classical = 885.389049
Code's capped axial / bending capacities = 807.561796 / 880.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 53522.820020
gamma_s^(3/4) = 0.67; gamma_s*Z = 31378.972927
Moderate-length torsion range: 50 < gamma_s*Z < 226206.610540
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 65.278898
Code's local interaction = compression + bending + shear ratios
                        = 0.162725113 + 0.638425690 + 0.196626566
                        = 0.997777369
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 3966269.600940
U_oval = M/M_Brazier = 0.838891644
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Steel 4130 - brief, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 205000; nu = 0.29; density = 7850 kg/m^3
D = 154.000; t = 0.580; L = 1500
Di = D - 2t = 152.840000
r = (D + Di)/4 = 76.710000
A = pi*t*(D-t) = 279.550224050
I = A*(D^2+Di^2)/16 = 822507.792866951
m = A*1500*density/10^9 = 3.291703888 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 2417463.166173
Pcr = pi^2*E*I/1500^2 = 739624.195175
beta = (pi/2)*sqrt(P/Pcr) = 0.331796112
M = M0/cos(beta) = 2556920.687699
amplification = 1.057687548
Midpoint beam deflection from Fourier check = 4.225986 mm
Euler U = P/Pcr = 0.044617253

Compression stress P/A = 118.046766
Bending stress M*(D/2)/I = 239.369030
Hoop stress p*(D/2)/t = 43.810345
Peak transverse shear 2V/A = 11.530251
sx(theta) = -118.046766 + 239.369030*cos(theta)
tau(theta) = 11.530251*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-357.415797)^2 + (43.810345)^2 - (-357.415797)*(43.810345)] / 460
                    = 0.828725499
Squared material utilisation = 0.686785952

r/t = 132.258621; L/r = 19.554165
phi = sqrt(r/t)/16 = 0.718773425
gx = 1-0.901*(1-exp(-phi)) = 0.538102044
gb = 1-0.731*(1-exp(-phi)) = 0.625252602
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 935.072350
raw axial buckling stress = gx*classical = 503.164343
raw bending buckling stress = gb*classical = 584.656419
Code's capped axial / bending capacities = 460.000000 / 460.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 48397.905954
gamma_s^(3/4) = 0.67; gamma_s*Z = 28374.375268
Moderate-length torsion range: 50 < gamma_s*Z < 1249656.464295
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 51.730853
Code's local interaction = compression + bending + shear ratios
                        = 0.256623405 + 0.520367458 + 0.222889247
                        = 0.999880110
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 5455756.190125
U_oval = M/M_Brazier = 0.468664764
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Magnesium AZ31B - brief, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 45000; nu = 0.35; density = 1770 kg/m^3
D = 169.000; t = 1.100; L = 1500
Di = D - 2t = 166.800000
r = (D + Di)/4 = 83.950000
A = pi*t*(D-t) = 580.220747191
I = A*(D^2+Di^2)/16 = 2044670.352617351
m = A*1500*density/10^9 = 1.540486084 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 2417463.166173
Pcr = pi^2*E*I/1500^2 = 403601.750219
beta = (pi/2)*sqrt(P/Pcr) = 0.449159228
M = M0/cos(beta) = 2683647.474249
amplification = 1.110108941
Midpoint beam deflection from Fourier check = 8.066191 mm
Euler U = P/Pcr = 0.081763768

Compression stress P/A = 56.874905
Bending stress M*(D/2)/I = 110.906979
Hoop stress p*(D/2)/t = 25.350000
Peak transverse shear 2V/A = 5.555272
sx(theta) = -56.874905 + 110.906979*cos(theta)
tau(theta) = 5.555272*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-167.781884)^2 + (25.350000)^2 - (-167.781884)*(25.350000)] / 220
                    = 0.826306302
Squared material utilisation = 0.682782105

r/t = 76.318182; L/r = 17.867778
phi = sqrt(r/t)/16 = 0.546001738
gx = 1-0.901*(1-exp(-phi)) = 0.620914363
gb = 1-0.731*(1-exp(-phi)) = 0.692439955
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 363.412874
raw axial buckling stress = gx*classical = 225.648273
raw bending buckling stress = gb*classical = 251.641594
Code's capped axial / bending capacities = 220.000000 / 220.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 22824.049212
gamma_s^(3/4) = 0.67; gamma_s*Z = 13381.118970
Moderate-length torsion range: 50 < gamma_s*Z < 398655.498440
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 23.620420
Code's local interaction = compression + bending + shear ratios
                        = 0.258522296 + 0.504122631 + 0.235189391
                        = 0.997834319
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 4816284.962415
U_oval = M/M_Brazier = 0.557202802
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Carbon/Epoxy QI - brief, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 55000; nu = 0.3; density = 1600 kg/m^3
D = 101.000; t = 1.200; L = 1500
Di = D - 2t = 98.600000
r = (D + Di)/4 = 49.900000
A = pi*t*(D-t) = 376.237136194
I = A*(D^2+Di^2)/16 = 468484.838431618
m = A*1500*density/10^9 = 0.902969127 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 2417463.166173
Pcr = pi^2*E*I/1500^2 = 113025.245012
beta = (pi/2)*sqrt(P/Pcr) = 0.848768236
M = M0/cos(beta) = 3657790.496559
amplification = 1.513069795
Midpoint beam deflection from Fourier check = 37.585677 mm
Euler U = P/Pcr = 0.291970170

Compression stress P/A = 87.710640
Bending stress M*(D/2)/I = 394.289003
Hoop stress p*(D/2)/t = 13.887500
Peak transverse shear 2V/A = 8.567161
sx(theta) = -87.710640 + 394.289003*cos(theta)
tau(theta) = 8.567161*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-481.999643)/600)^2 + (13.887500/500)^2]
                    = 0.803812752
Squared material utilisation = 0.646114940

r/t = 41.583333; L/r = 30.060120
phi = sqrt(r/t)/16 = 0.403032128
gx = 1-0.901*(1-exp(-phi)) = 0.701129856
gb = 1-0.731*(1-exp(-phi)) = 0.757520449
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 800.501346
raw axial buckling stress = gx*classical = 561.255393
raw bending buckling stress = gb*classical = 606.396139
Code's capped axial / bending capacities = 561.255393 / 600.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 35844.408871
gamma_s^(3/4) = 0.67; gamma_s*Z = 21014.601531
Moderate-length torsion range: 50 < gamma_s*Z < 122736.742917
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 47.545959
Code's local interaction = compression + bending + shear ratios
                        = 0.156275808 + 0.657148339 + 0.180186948
                        = 0.993611095
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 4089047.765524
U_oval = M/M_Brazier = 0.894533570
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Glass/Epoxy QI - brief, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 25000; nu = 0.3; density = 1900 kg/m^3
D = 125.000; t = 1.600; L = 1500
Di = D - 2t = 121.800000
r = (D + Di)/4 = 61.700000
A = pi*t*(D-t) = 620.276053525
I = A*(D^2+Di^2)/16 = 1180859.841038581
m = A*1500*density/10^9 = 1.767786753 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 2417463.166173
Pcr = pi^2*E*I/1500^2 = 129495.772046
beta = (pi/2)*sqrt(P/Pcr) = 0.792955932
M = M0/cos(beta) = 3444943.420394
amplification = 1.425024161
Midpoint beam deflection from Fourier check = 31.135765 mm
Euler U = P/Pcr = 0.254834575

Compression stress P/A = 53.202118
Bending stress M*(D/2)/I = 182.332362
Hoop stress p*(D/2)/t = 12.890625
Peak transverse shear 2V/A = 5.196532
sx(theta) = -53.202118 + 182.332362*cos(theta)
tau(theta) = 5.196532*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-235.534480)/300)^2 + (12.890625/250)^2]
                    = 0.786806298
Squared material utilisation = 0.619064151

r/t = 38.562500; L/r = 24.311183
phi = sqrt(r/t)/16 = 0.388116948
gx = 1-0.901*(1-exp(-phi)) = 0.710178041
gb = 1-0.731*(1-exp(-phi)) = 0.764861429
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 392.367930
raw axial buckling stress = gx*classical = 278.651088
raw bending buckling stress = gb*classical = 300.107096
Code's capped axial / bending capacities = 278.651088 / 300.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 21741.928719
gamma_s^(3/4) = 0.67; gamma_s*Z = 12746.701172
Moderate-length torsion range: 50 < gamma_s*Z < 105551.973516
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 26.407415
Code's local interaction = compression + bending + shear ratios
                        = 0.190927366 + 0.607774539 + 0.196783055
                        = 0.995484960
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 4085654.090125
U_oval = M/M_Brazier = 0.843180393
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Aramid/Epoxy QI - brief, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 35000; nu = 0.34; density = 1400 kg/m^3
D = 169.000; t = 1.230; L = 1500
Di = D - 2t = 166.540000
r = (D + Di)/4 = 83.885000
A = pi*t*(D-t) = 648.289949376
I = A*(D^2+Di^2)/16 = 2281031.347038229
m = A*1500*density/10^9 = 1.361408894 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 2417463.166173
Pcr = pi^2*E*I/1500^2 = 350200.309227
beta = (pi/2)*sqrt(P/Pcr) = 0.482190427
M = M0/cos(beta) = 2728571.315048
amplification = 1.128691991
Midpoint beam deflection from Fourier check = 9.427520 mm
Euler U = P/Pcr = 0.094231784

Compression stress P/A = 50.903149
Bending stress M*(D/2)/I = 101.078960
Hoop stress p*(D/2)/t = 22.670732
Peak transverse shear 2V/A = 4.971979
sx(theta) = -50.903149 + 101.078960*cos(theta)
tau(theta) = 4.971979*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-151.982109)/200)^2 + (22.670732/300)^2]
                    = 0.763658776
Squared material utilisation = 0.583174727

r/t = 68.199187; L/r = 17.881624
phi = sqrt(r/t)/16 = 0.516142494
gx = 1-0.901*(1-exp(-phi)) = 0.636733328
gb = 1-0.731*(1-exp(-phi)) = 0.705274209
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 315.067678
raw axial buckling stress = gx*classical = 200.614091
raw bending buckling stress = gb*classical = 222.209108
Code's capped axial / bending capacities = 200.000000 / 200.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 20507.724039
gamma_s^(3/4) = 0.67; gamma_s*Z = 12023.120553
Moderate-length torsion range: 50 < gamma_s*Z < 320849.769369
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 21.136641
Code's local interaction = compression + bending + shear ratios
                        = 0.254515746 + 0.505394800 + 0.235230340
                        = 0.995140886
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 4661818.508775
U_oval = M/M_Brazier = 0.585301918
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

## 5. Fully substituted transfer-moment calculations

### Aluminium 7075-T6 - transfer, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 71700; nu = 0.33; density = 2810 kg/m^3
D = 137.000; t = 1.100; L = 1500
Di = D - 2t = 134.800000
r = (D + Di)/4 = 67.950000
A = pi*t*(D-t) = 469.636685785
I = A*(D^2+Di^2)/16 = 1084274.872398153
m = A*1500*density/10^9 = 1.979518631 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 4834926.332346
Pcr = pi^2*E*I/1500^2 = 341016.801143
beta = (pi/2)*sqrt(P/Pcr) = 0.488639936
M = M0/cos(beta) = 5475740.630628
amplification = 1.132538586
Midpoint beam deflection from Fourier check = 19.418615 mm
Euler U = P/Pcr = 0.096769426

Compression stress P/A = 70.267083
Bending stress M*(D/2)/I = 345.934636
Hoop stress p*(D/2)/t = 20.550000
Peak transverse shear 2V/A = 6.863357
sx(theta) = -70.267083 + 345.934636*cos(theta)
tau(theta) = 6.863357*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-416.201719)^2 + (20.550000)^2 - (-416.201719)*(20.550000)] / 503
                    = 0.848604149
Squared material utilisation = 0.720129002

r/t = 61.772727; L/r = 22.075055
phi = sqrt(r/t)/16 = 0.491222674
gx = 1-0.901*(1-exp(-phi)) = 0.650301906
gb = 1-0.731*(1-exp(-phi)) = 0.716282679
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 709.902214
raw axial buckling stress = gx*classical = 461.650763
raw bending buckling stress = gb*classical = 508.490659
Code's capped axial / bending capacities = 461.650763 / 503.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 28416.042505
gamma_s^(3/4) = 0.67; gamma_s*Z = 16659.552470
Moderate-length torsion range: 50 < gamma_s*Z < 265225.085557
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 44.102955
Code's local interaction = compression + bending + shear ratios
                        = 0.152208311 + 0.687742815 + 0.155621249
                        = 0.995572375
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 6163791.191900
U_oval = M/M_Brazier = 0.888372182
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Titanium Ti-6Al-4V - transfer, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 113800; nu = 0.31; density = 4430 kg/m^3
D = 111.000; t = 0.960; L = 1500
Di = D - 2t = 109.080000
r = (D + Di)/4 = 55.020000
A = pi*t*(D-t) = 331.872821377
I = A*(D^2+Di^2)/16 = 502361.000559784
m = A*1500*density/10^9 = 2.205294898 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 4834926.332346
Pcr = pi^2*E*I/1500^2 = 250769.899612
beta = (pi/2)*sqrt(P/Pcr) = 0.569821910
M = M0/cos(beta) = 5742212.809553
amplification = 1.187652596
Midpoint beam deflection from Fourier check = 27.493530 mm
Euler U = P/Pcr = 0.131594741

Compression stress P/A = 99.435681
Bending stress M*(D/2)/I = 634.390031
Hoop stress p*(D/2)/t = 19.078125
Peak transverse shear 2V/A = 9.712408
sx(theta) = -99.435681 + 634.390031*cos(theta)
tau(theta) = 9.712408*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-733.825712)^2 + (19.078125)^2 - (-733.825712)*(19.078125)] / 880
                    = 0.844941323
Squared material utilisation = 0.713925839

r/t = 57.312500; L/r = 27.262814
phi = sqrt(r/t)/16 = 0.473156373
gx = 1-0.901*(1-exp(-phi)) = 0.660352407
gb = 1-0.731*(1-exp(-phi)) = 0.724436859
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 1205.791140
raw axial buckling stress = gx*classical = 796.247082
raw bending buckling stress = gb*classical = 873.519546
Code's capped axial / bending capacities = 796.247082 / 873.519546
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 40499.614767
gamma_s^(3/4) = 0.67; gamma_s*Z = 23743.822071
Moderate-length torsion range: 50 < gamma_s*Z < 231586.743101
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 69.173642
Code's local interaction = compression + bending + shear ratios
                        = 0.124880434 + 0.726245949 + 0.140406197
                        = 0.991532580
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 5990488.981135
U_oval = M/M_Brazier = 0.958554941
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Steel 4130 - transfer, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 205000; nu = 0.29; density = 7850 kg/m^3
D = 183.000; t = 0.650; L = 1500
Di = D - 2t = 181.700000
r = (D + Di)/4 = 91.175000
A = pi*t*(D-t) = 372.365123248
I = A*(D^2+Di^2)/16 = 1547733.074771604
m = A*1500*density/10^9 = 4.384599326 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 4834926.332346
Pcr = pi^2*E*I/1500^2 = 1391768.977390
beta = (pi/2)*sqrt(P/Pcr) = 0.241876275
M = M0/cos(beta) = 4979889.573530
amplification = 1.029982513
Midpoint beam deflection from Fourier check = 4.392825 mm
Euler U = P/Pcr = 0.023710832

Compression stress P/A = 88.622693
Bending stress M*(D/2)/I = 294.404703
Hoop stress p*(D/2)/t = 46.453846
Peak transverse shear 2V/A = 8.656246
sx(theta) = -88.622693 + 294.404703*cos(theta)
tau(theta) = 8.656246*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-383.027396)^2 + (46.453846)^2 - (-383.027396)*(46.453846)] / 460
                    = 0.887481307
Squared material utilisation = 0.787623070

r/t = 140.269231; L/r = 16.451878
phi = sqrt(r/t)/16 = 0.740220699
gx = 1-0.901*(1-exp(-phi)) = 0.528784775
gb = 1-0.731*(1-exp(-phi)) = 0.617693308
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 881.671472
raw axial buckling stress = gx*classical = 466.214451
raw bending buckling stress = gb*classical = 544.602568
Code's capped axial / bending capacities = 460.000000 / 460.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 36334.351980
gamma_s^(3/4) = 0.67; gamma_s*Z = 21301.841844
Moderate-length torsion range: 50 < gamma_s*Z < 1405618.590358
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 52.400871
Code's local interaction = compression + bending + shear ratios
                        = 0.192658028 + 0.640010224 + 0.165192795
                        = 0.997861047
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 8144219.488611
U_oval = M/M_Brazier = 0.611463085
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Magnesium AZ31B - transfer, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 45000; nu = 0.35; density = 1770 kg/m^3
D = 199.000; t = 1.230; L = 1500
Di = D - 2t = 196.540000
r = (D + Di)/4 = 98.885000
A = pi*t*(D-t) = 764.214718294
I = A*(D^2+Di^2)/16 = 3736483.218355546
m = A*1500*density/10^9 = 2.028990077 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 4834926.332346
Pcr = pi^2*E*I/1500^2 = 737552.224330
beta = (pi/2)*sqrt(P/Pcr) = 0.332261834
M = M0/cos(beta) = 5114662.612624
amplification = 1.057857403
Midpoint beam deflection from Fourier check = 8.476857 mm
Euler U = P/Pcr = 0.044742594

Compression stress P/A = 43.181581
Bending stress M*(D/2)/I = 136.199977
Hoop stress p*(D/2)/t = 26.695122
Peak transverse shear 2V/A = 4.217773
sx(theta) = -43.181581 + 136.199977*cos(theta)
tau(theta) = 4.217773*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-179.381559)^2 + (26.695122)^2 - (-179.381559)*(26.695122)] / 220
                    = 0.882321620
Squared material utilisation = 0.778491441

r/t = 80.394309; L/r = 15.169136
phi = sqrt(r/t)/16 = 0.560392960
gx = 1-0.901*(1-exp(-phi)) = 0.613457166
gb = 1-0.731*(1-exp(-phi)) = 0.686389776
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 344.987228
raw axial buckling stress = gx*classical = 211.634887
raw bending buckling stress = gb*classical = 236.795706
Code's capped axial / bending capacities = 211.634887 / 220.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 17328.882277
gamma_s^(3/4) = 0.67; gamma_s*Z = 10159.452129
Moderate-length torsion range: 50 < gamma_s*Z < 442376.797895
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 24.021264
Code's local interaction = compression + bending + shear ratios
                        = 0.204038105 + 0.619090806 + 0.175584971
                        = 0.998713882
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 7093274.138280
U_oval = M/M_Brazier = 0.721058077
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Carbon/Epoxy QI - transfer, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 55000; nu = 0.3; density = 1600 kg/m^3
D = 113.000; t = 1.400; L = 1500
Di = D - 2t = 110.200000
r = (D + Di)/4 = 55.800000
A = pi*t*(D-t) = 490.842436197
I = A*(D^2+Di^2)/16 = 764273.577916878
m = A*1500*density/10^9 = 1.178021847 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 4834926.332346
Pcr = pi^2*E*I/1500^2 = 184386.347890
beta = (pi/2)*sqrt(P/Pcr) = 0.664526747
M = M0/cos(beta) = 6141860.724146
amplification = 1.270311128
Midpoint beam deflection from Fourier check = 39.604072 mm
Euler U = P/Pcr = 0.178972035

Compression stress P/A = 67.231351
Bending stress M*(D/2)/I = 454.045699
Hoop stress p*(D/2)/t = 13.317857
Peak transverse shear 2V/A = 6.566841
sx(theta) = -67.231351 + 454.045699*cos(theta)
tau(theta) = 6.566841*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-521.277050)/600)^2 + (13.317857/500)^2]
                    = 0.869203289
Squared material utilisation = 0.755514357

r/t = 39.857143; L/r = 26.881720
phi = sqrt(r/t)/16 = 0.394578211
gx = 1-0.901*(1-exp(-phi)) = 0.706241790
gb = 1-0.731*(1-exp(-phi)) = 0.761667867
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 835.170610
raw axial buckling stress = gx*classical = 589.832386
raw bending buckling stress = gb*classical = 636.122617
Code's capped axial / bending capacities = 589.832386 / 600.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 27475.207414
gamma_s^(3/4) = 0.67; gamma_s*Z = 16107.966458
Moderate-length torsion range: 50 < gamma_s*Z < 112758.248571
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 53.014767
Code's local interaction = compression + bending + shear ratios
                        = 0.113983824 + 0.756742832 + 0.123868147
                        = 0.994594802
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 6223710.977787
U_oval = M/M_Brazier = 0.986848642
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Glass/Epoxy QI - transfer, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 25000; nu = 0.3; density = 1900 kg/m^3
D = 141.000; t = 1.840; L = 1500
Di = D - 2t = 137.320000
r = (D + Di)/4 = 69.580000
A = pi*t*(D-t) = 804.418621959
I = A*(D^2+Di^2)/16 = 1947587.095998054
m = A*1500*density/10^9 = 2.292593073 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 4834926.332346
Pcr = pi^2*E*I/1500^2 = 213576.824157
beta = (pi/2)*sqrt(P/Pcr) = 0.617447142
M = M0/cos(beta) = 5929812.169066
amplification = 1.226453468
Midpoint beam deflection from Fourier check = 33.178359 mm
Euler U = P/Pcr = 0.154511147

Compression stress P/A = 41.023416
Bending stress M*(D/2)/I = 214.651123
Hoop stress p*(D/2)/t = 12.644022
Peak transverse shear 2V/A = 4.006974
sx(theta) = -41.023416 + 214.651123*cos(theta)
tau(theta) = 4.006974*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-255.674540)/300)^2 + (12.644022/250)^2]
                    = 0.853747848
Squared material utilisation = 0.728885387

r/t = 37.815217; L/r = 21.557919
phi = sqrt(r/t)/16 = 0.384337993
gx = 1-0.901*(1-exp(-phi)) = 0.712492025
gb = 1-0.731*(1-exp(-phi)) = 0.766738813
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 400.121680
raw axial buckling stress = gx*classical = 285.083506
raw bending buckling stress = gb*classical = 306.788822
Code's capped axial / bending capacities = 285.083506 / 300.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 16764.899984
gamma_s^(3/4) = 0.67; gamma_s*Z = 9828.804658
Moderate-length torsion range: 50 < gamma_s*Z < 101500.737498
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 28.737484
Code's local interaction = compression + bending + shear ratios
                        = 0.143899648 + 0.715503744 + 0.139433697
                        = 0.998837090
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 6093355.767082
U_oval = M/M_Brazier = 0.973160340
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Aramid/Epoxy QI - transfer, multiplier 1.1

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 35000; nu = 0.34; density = 1400 kg/m^3
D = 195.000; t = 1.400; L = 1500
Di = D - 2t = 192.200000
r = (D + Di)/4 = 96.800000
A = pi*t*(D-t) = 851.497272829
I = A*(D^2+Di^2)/16 = 3989575.519708342
m = A*1500*density/10^9 = 1.788144273 kg

P = 33000.000000; V = 1611.642111; p = 0.330000
M0 = 4834926.332346
Pcr = pi^2*E*I/1500^2 = 612508.277232
beta = (pi/2)*sqrt(P/Pcr) = 0.364603527
M = M0/cos(beta) = 5175111.188019
amplification = 1.070359884
Midpoint beam deflection from Fourier check = 10.308632 mm
Euler U = P/Pcr = 0.053876823

Compression stress P/A = 38.755262
Bending stress M*(D/2)/I = 126.472939
Hoop stress p*(D/2)/t = 22.982143
Peak transverse shear 2V/A = 3.785431
sx(theta) = -38.755262 + 126.472939*cos(theta)
tau(theta) = 3.785431*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-165.228201)/200)^2 + (22.982143/300)^2]
                    = 0.829685250
Squared material utilisation = 0.688377614

r/t = 69.142857; L/r = 15.495868
phi = sqrt(r/t)/16 = 0.519701150
gx = 1-0.901*(1-exp(-phi)) = 0.634823120
gb = 1-0.731*(1-exp(-phi)) = 0.703724418
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 310.767596
raw axial buckling stress = gx*classical = 197.282455
raw bending buckling stress = gb*classical = 218.694746
Code's capped axial / bending capacities = 197.282455 / 200.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 15613.615925
gamma_s^(3/4) = 0.67; gamma_s*Z = 9153.838143
Moderate-length torsion range: 50 < gamma_s*Z < 329790.377535
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 22.318826
Code's local interaction = compression + bending + shear ratios
                        = 0.196445559 + 0.632364694 + 0.169607087
                        = 0.998417340
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 6969349.734288
U_oval = M/M_Brazier = 0.742552948
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

## 6. Illustrative 1.5-times-load candidates - not an assigned course requirement

### Aluminium 7075-T6 - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 71700; nu = 0.33; density = 2810 kg/m^3
D = 130.000; t = 1.090; L = 1500
Di = D - 2t = 127.820000
r = (D + Di)/4 = 64.455000
A = pi*t*(D-t) = 441.431152782
I = A*(D^2+Di^2)/16 = 917016.727752710
m = A*1500*density/10^9 = 1.860632309 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 288412.208983
beta = (pi/2)*sqrt(P/Pcr) = 0.620467893
M = M0/cos(beta) = 4051762.935208
amplification = 1.229095384
Midpoint beam deflection from Fourier check = 16.782717 mm
Euler U = P/Pcr = 0.156026682

Compression stress P/A = 101.941151
Bending stress M*(D/2)/I = 287.197150
Hoop stress p*(D/2)/t = 26.834862
Peak transverse shear 2V/A = 9.957130
sx(theta) = -101.941151 + 287.197150*cos(theta)
tau(theta) = 9.957130*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-389.138302)^2 + (26.834862)^2 - (-389.138302)*(26.834862)] / 503
                    = 0.801642130
Squared material utilisation = 0.642630105

r/t = 59.133028; L/r = 23.272050
phi = sqrt(r/t)/16 = 0.480612514
gx = 1-0.901*(1-exp(-phi)) = 0.656182449
gb = 1-0.731*(1-exp(-phi)) = 0.721053685
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 741.592266
raw axial buckling stress = gx*classical = 486.619829
raw bending buckling stress = gb*classical = 534.727836
Code's capped axial / bending capacities = 486.619829 / 503.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 30231.704176
gamma_s^(3/4) = 0.67; gamma_s*Z = 17724.025500
Moderate-length torsion range: 50 < gamma_s*Z < 243041.969557
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 45.363817
Code's local interaction = compression + bending + shear ratios
                        = 0.209488281 + 0.570968489 + 0.219494986
                        = 0.999951756
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 5740935.864479
U_oval = M/M_Brazier = 0.705766974
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Titanium Ti-6Al-4V - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 113800; nu = 0.31; density = 4430 kg/m^3
D = 107.000; t = 0.930; L = 1500
Di = D - 2t = 105.140000
r = (D + Di)/4 = 53.035000
A = pi*t*(D-t) = 309.902721473
I = A*(D^2+Di^2)/16 = 435866.936030033
m = A*1500*density/10^9 = 2.059303584 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 217577.215728
beta = (pi/2)*sqrt(P/Pcr) = 0.714363780
M = M0/cos(beta) = 4363330.445148
amplification = 1.323608858
Midpoint beam deflection from Fourier check = 23.706439 mm
Euler U = P/Pcr = 0.206823126

Compression stress P/A = 145.206856
Bending stress M*(D/2)/I = 535.572120
Hoop stress p*(D/2)/t = 25.887097
Peak transverse shear 2V/A = 14.183120
sx(theta) = -145.206856 + 535.572120*cos(theta)
tau(theta) = 14.183120*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-680.778976)^2 + (25.887097)^2 - (-680.778976)*(25.887097)] / 880
                    = 0.788732594
Squared material utilisation = 0.622099106

r/t = 57.026882; L/r = 28.283209
phi = sqrt(r/t)/16 = 0.471975907
gx = 1-0.901*(1-exp(-phi)) = 0.661015456
gb = 1-0.731*(1-exp(-phi)) = 0.724974804
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 1211.830327
raw axial buckling stress = gx*classical = 801.038576
raw bending buckling stress = gb*classical = 878.546453
Code's capped axial / bending capacities = 801.038576 / 878.546453
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 43370.775685
gamma_s^(3/4) = 0.67; gamma_s*Z = 25427.105589
Moderate-length torsion range: 50 < gamma_s*Z < 229284.258006
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 68.339814
Code's local interaction = compression + bending + shear ratios
                        = 0.181273238 + 0.609611612 + 0.207538175
                        = 0.998423025
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 5419106.570853
U_oval = M/M_Brazier = 0.805175242
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Steel 4130 - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 205000; nu = 0.29; density = 7850 kg/m^3
D = 179.000; t = 0.630; L = 1500
Di = D - 2t = 177.740000
r = (D + Di)/4 = 89.185000
A = pi*t*(D-t) = 353.030505421
I = A*(D^2+Di^2)/16 = 1404013.519952544
m = A*1500*density/10^9 = 4.156934201 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 1262531.952543
beta = (pi/2)*sqrt(P/Pcr) = 0.296554791
M = M0/cos(beta) = 3447006.130875
amplification = 1.045643438
Midpoint beam deflection from Fourier check = 3.343677 mm
Euler U = P/Pcr = 0.035642662

Compression stress P/A = 127.467738
Bending stress M*(D/2)/I = 219.732249
Hoop stress p*(D/2)/t = 63.928571
Peak transverse shear 2V/A = 12.450447
sx(theta) = -127.467738 + 219.732249*cos(theta)
tau(theta) = 12.450447*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-347.199987)^2 + (63.928571)^2 - (-347.199987)*(63.928571)] / 460
                    = 0.833010723
Squared material utilisation = 0.693906865

r/t = 141.563492; L/r = 16.818972
phi = sqrt(r/t)/16 = 0.743627858
gx = 1-0.901*(1-exp(-phi)) = 0.527322921
gb = 1-0.731*(1-exp(-phi)) = 0.616507276
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 873.610685
raw axial buckling stress = gx*classical = 460.674938
raw bending buckling stress = gb*classical = 538.587343
Code's capped axial / bending capacities = 460.000000 / 460.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 38324.295621
gamma_s^(3/4) = 0.67; gamma_s*Z = 22468.491651
Moderate-length torsion range: 50 < gamma_s*Z < 1431677.488100
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 51.234259
Code's local interaction = compression + bending + shear ratios
                        = 0.277103778 + 0.477678803 + 0.243010188
                        = 0.997792769
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 7483760.832391
U_oval = M/M_Brazier = 0.460598115
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Magnesium AZ31B - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 45000; nu = 0.35; density = 1770 kg/m^3
D = 192.000; t = 1.220; L = 1500
Di = D - 2t = 189.560000
r = (D + Di)/4 = 95.390000
A = pi*t*(D-t) = 731.210716671
I = A*(D^2+Di^2)/16 = 3326871.366360617
m = A*1500*density/10^9 = 1.941364453 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 656698.085586
beta = (pi/2)*sqrt(P/Pcr) = 0.411190677
M = M0/cos(beta) = 3596309.011963
amplification = 1.090934213
Midpoint beam deflection from Fourier check = 6.661518 mm
Euler U = P/Pcr = 0.068524640

Compression stress P/A = 61.541768
Bending stress M*(D/2)/I = 103.774876
Hoop stress p*(D/2)/t = 35.409836
Peak transverse shear 2V/A = 6.011109
sx(theta) = -61.541768 + 103.774876*cos(theta)
tau(theta) = 6.011109*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-165.316644)^2 + (35.409836)^2 - (-165.316644)*(35.409836)] / 220
                    = 0.843512978
Squared material utilisation = 0.711514144

r/t = 78.188525; L/r = 15.724919
phi = sqrt(r/t)/16 = 0.552651721
gx = 1-0.901*(1-exp(-phi)) = 0.617455157
gb = 1-0.731*(1-exp(-phi)) = 0.689633429
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 354.719698
raw axial buckling stress = gx*classical = 219.023507
raw bending buckling stress = gb*classical = 244.626561
Code's capped axial / bending capacities = 219.023507 / 220.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 18111.040478
gamma_s^(3/4) = 0.67; gamma_s*Z = 10618.010199
Moderate-length torsion range: 50 < gamma_s*Z < 418434.768869
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 24.427833
Code's local interaction = compression + bending + shear ratios
                        = 0.280982478 + 0.471703984 + 0.246076243
                        = 0.998762705
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 6731759.842738
U_oval = M/M_Brazier = 0.534230141
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Carbon/Epoxy QI - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 55000; nu = 0.3; density = 1600 kg/m^3
D = 111.000; t = 1.340; L = 1500
Di = D - 2t = 108.320000
r = (D + Di)/4 = 54.830000
A = pi*t*(D-t) = 461.639447526
I = A*(D^2+Di^2)/16 = 694023.621212961
m = A*1500*density/10^9 = 1.107934674 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 167438.054334
beta = (pi/2)*sqrt(P/Pcr) = 0.814327403
M = M0/cos(beta) = 4802948.463215
amplification = 1.456966235
Midpoint beam deflection from Fourier check = 33.475728 mm
Euler U = P/Pcr = 0.268756109

Compression stress P/A = 97.478671
Bending stress M*(D/2)/I = 384.084391
Hoop stress p*(D/2)/t = 18.638060
Peak transverse shear 2V/A = 9.521256
sx(theta) = -97.478671 + 384.084391*cos(theta)
tau(theta) = 9.521256*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-481.563062)/600)^2 + (18.638060/500)^2]
                    = 0.803470262
Squared material utilisation = 0.645564461

r/t = 40.917910; L/r = 27.357286
phi = sqrt(r/t)/16 = 0.399794432
gx = 1-0.901*(1-exp(-phi)) = 0.703082529
gb = 1-0.731*(1-exp(-phi)) = 0.759104693
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 813.519408
raw axial buckling stress = gx*classical = 571.971283
raw bending buckling stress = gb*classical = 617.546401
Code's capped axial / bending capacities = 571.971283 / 600.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 29213.269824
gamma_s^(3/4) = 0.67; gamma_s*Z = 17126.945153
Moderate-length torsion range: 50 < gamma_s*Z < 118840.067566
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 50.854546
Code's local interaction = compression + bending + shear ratios
                        = 0.170425814 + 0.640140651 + 0.187225279
                        = 0.997791744
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 5602566.093564
U_oval = M/M_Brazier = 0.857276538
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Glass/Epoxy QI - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 25000; nu = 0.3; density = 1900 kg/m^3
D = 138.000; t = 1.790; L = 1500
Di = D - 2t = 134.420000
r = (D + Di)/4 = 68.105000
A = pi*t*(D-t) = 765.970240268
I = A*(D^2+Di^2)/16 = 1776703.226082824
m = A*1500*density/10^9 = 2.183015185 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 194837.310884
beta = (pi/2)*sqrt(P/Pcr) = 0.754901121
M = M0/cos(beta) = 4526105.732513
amplification = 1.372986464
Midpoint beam deflection from Fourier check = 27.323668 mm
Euler U = P/Pcr = 0.230961923

Compression stress P/A = 58.749019
Bending stress M*(D/2)/I = 175.775724
Hoop stress p*(D/2)/t = 17.346369
Peak transverse shear 2V/A = 5.738327
sx(theta) = -58.749019 + 175.775724*cos(theta)
tau(theta) = 5.738327*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-234.524743)/300)^2 + (17.346369/250)^2]
                    = 0.784822314
Squared material utilisation = 0.615946065

r/t = 38.047486; L/r = 22.024815
phi = sqrt(r/t)/16 = 0.385516527
gx = 1-0.901*(1-exp(-phi)) = 0.711769430
gb = 1-0.731*(1-exp(-phi)) = 0.766152556
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 397.679056
raw axial buckling stress = gx*classical = 283.055795
raw bending buckling stress = gb*classical = 304.682825
Code's capped axial / bending capacities = 283.055795 / 300.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 17606.425202
gamma_s^(3/4) = 0.67; gamma_s*Z = 10322.167994
Moderate-length torsion range: 50 < gamma_s*Z < 102751.442513
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 28.214465
Code's local interaction = compression + bending + shear ratios
                        = 0.207552786 + 0.585919079 + 0.203382441
                        = 0.996854306
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 5644448.623759
U_oval = M/M_Brazier = 0.801868532
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

### Aramid/Epoxy QI - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 35000; nu = 0.34; density = 1400 kg/m^3
D = 188.000; t = 1.390; L = 1500
Di = D - 2t = 185.220000
r = (D + Di)/4 = 93.305000
A = pi*t*(D-t) = 814.891121070
I = A*(D^2+Di^2)/16 = 3547345.748731877
m = A*1500*density/10^9 = 1.711271354 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 544613.987771
beta = (pi/2)*sqrt(P/Pcr) = 0.451524934
M = M0/cos(beta) = 3663707.309431
amplification = 1.111379371
Midpoint beam deflection from Fourier check = 8.159258 mm
Euler U = P/Pcr = 0.082627331

Compression stress P/A = 55.222101
Bending stress M*(D/2)/I = 97.083428
Hoop stress p*(D/2)/t = 30.431655
Peak transverse shear 2V/A = 5.393834
sx(theta) = -55.222101 + 97.083428*cos(theta)
tau(theta) = 5.393834*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[((-152.305530)/200)^2 + (30.431655/300)^2]
                    = 0.768253994
Squared material utilisation = 0.590214199

r/t = 67.125899; L/r = 16.076309
phi = sqrt(r/t)/16 = 0.512064980
gx = 1-0.901*(1-exp(-phi)) = 0.638930419
gb = 1-0.731*(1-exp(-phi)) = 0.707056755
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 320.105350
raw axial buckling stress = gx*classical = 204.525046
raw bending buckling stress = gb*classical = 226.332650
Code's capped axial / bending capacities = 200.000000 / 200.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 16315.003361
gamma_s^(3/4) = 0.67; gamma_s*Z = 9565.042511
Moderate-length torsion range: 50 < gamma_s*Z < 310830.459551
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 22.738281
Code's local interaction = compression + bending + shear ratios
                        = 0.276110506 + 0.485417142 + 0.237213804
                        = 0.998741453
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 6622094.099975
U_oval = M/M_Brazier = 0.553255096
Numerical screen passes: True
Competition compliance: NOT established by this calculation
```

## 7. Current selected shell tested at 1.5 times loads

### Aluminium 7075-T6 - brief, multiplier 1.5

All dimensions below are mm, forces N, stresses MPa = N/mm^2, moments N mm, and I in mm^4. Mass is kg. Shear is zero at theta = 180 degrees; its maximum occurs at a different angle.

```text
E = 71700; nu = 0.33; density = 2810 kg/m^3
D = 119.000; t = 0.960; L = 1500
Di = D - 2t = 117.080000
r = (D + Di)/4 = 59.020000
A = pi*t*(D-t) = 356.000252957
I = A*(D^2+Di^2)/16 = 620079.602998555
m = A*1500*density/10^9 = 1.500541066 kg

P = 45000.000000; V = 2197.693787; p = 0.450000
M0 = 3296540.681145
Pcr = pi^2*E*I/1500^2 = 195022.100070
beta = (pi/2)*sqrt(P/Pcr) = 0.754543391
M = M0/cos(beta) = 4524583.272559
amplification = 1.372524628
Midpoint beam deflection from Fourier check = 27.289835 mm
Euler U = P/Pcr = 0.230743080

Compression stress P/A = 126.404405
Bending stress M*(D/2)/I = 434.158297
Hoop stress p*(D/2)/t = 27.890625
Peak transverse shear 2V/A = 12.346586
sx(theta) = -126.404405 + 434.158297*cos(theta)
tau(theta) = 12.346586*sin(theta)
Worst material angle = 180.00 deg
Material utilisation = sqrt[(-560.562702)^2 + (27.890625)^2 - (-560.562702)*(27.890625)] / 503
                    = 1.143172052
Squared material utilisation = 1.306842341

r/t = 61.479167; L/r = 25.415114
phi = sqrt(r/t)/16 = 0.490054073
gx = 1-0.901*(1-exp(-phi)) = 0.650946535
gb = 1-0.731*(1-exp(-phi)) = 0.716805679
classical = E*(t/r)/sqrt(3*(1-nu^2)) = 713.291969
raw axial buckling stress = gx*classical = 464.314936
raw bending buckling stress = gb*classical = 511.291734
Code's capped axial / bending capacities = 464.314936 / 503.000000
NOTE: a yield cap does NOT validate inelastic buckling.

Z = L^2*sqrt(1-nu^2)/(r*t) = 37486.535232
gamma_s^(3/4) = 0.67; gamma_s*Z = 21977.335532
Moderate-length torsion range: 50 < gamma_s*Z < 262710.233605
tau_cr = 0.747*0.67*E*(t/r)^1.25/sqrt(L/r) = 41.348387
Code's local interaction = compression + bending + shear ratios
                        = 0.272238506 + 0.863137768 + 0.298598967
                        = 1.433975242
NOTE: peak transverse shear with torsional capacity is a surrogate.

M_Brazier = 0.987*E*r*t^2/sqrt(1-nu^2) = 4077695.179174
U_oval = M/M_Brazier = 1.109593305
Numerical screen passes: False
Competition compliance: NOT established by this calculation
```

## 8. Sources and reproduction

- Assignment sections 3-7: input loads, material properties and required methods.
- [NASA SP-8007 Rev 2](https://ntrs.nasa.gov/citations/20205011530): equations 7, 9-16, 34-35 and 41; printed pp. 25-26 discuss long cylinders, plasticity and ovalisation. Their use does not automatically validate this model's extra approximations.
- [Air Force beam-column methods](https://engineeringlibrary.org/reference/beam-columns-air-force-stress-manual): compression/bending coupling and boundary-dependent solutions.
- [Air Force thin pressure vessels, Table 8-5](https://engineeringlibrary.org/reference/simple-thin-pressure-vessels-air-force-stress-manual): transverse shear is distinguished from torsion in combined-load checks. A web transcription is not sufficient to resolve every printed equation; no replacement interaction has been adopted in this audit.

```sh
python3 src/verify_calculations.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
