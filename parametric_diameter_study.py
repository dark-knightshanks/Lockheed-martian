import math

# Flight Loads
F = 30000.0         # Axial thrust [N]
p = 300000.0        # Ullage internal pressure [Pa]
M = 2197.69         # Bending moment from gust [N.m]
V = 1465.13         # Shear force from gust [N]
L = 1.5             # Barrel length [m]

FS_yield = 1.25     # Safety factor for yield
FS_buckle = 1.40    # Safety factor for buckling
gamma = 0.35        # NASA SP-8007 shell knockdown factor

materials = {
    'Al 7075-T6': {
        'E': 71.7e9, 'sigma_y': 503e6, 'rho': 2810, 'nu': 0.33, 'type': 'metal'
    },
    'Carbon/Epoxy QI': {
        'E': 55.0e9, 'Xc': 600e6, 'Yt': 500e6, 'S': 200e6, 'rho': 1600, 'nu': 0.30, 'type': 'composite'
    },
    'Magnesium AZ31B': {
        'E': 45.0e9, 'sigma_y': 220e6, 'rho': 1770, 'nu': 0.35, 'type': 'metal'
    },
    'Titanium Ti-6Al-4V': {
        'E': 113.8e9, 'sigma_y': 880e6, 'rho': 4430, 'nu': 0.31, 'type': 'metal'
    }
}

diameters_mm = [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]

print(f"{'D (mm)':<8} {'Material':<18} {'t_yield(mm)':<12} {'t_euler(mm)':<12} {'t_local(mm)':<12} {'t_req(mm)':<10} {'Mass (kg)':<10} {'Governing'}")
print("-" * 95)

results = []

for D_mm in diameters_mm:
    D = D_mm / 1000.0
    R = D / 2.0
    
    for mat_name, props in materials.items():
        E = props['E']
        rho = props['rho']
        nu = props['nu']
        
        # 1. Global Euler Column Buckling:
        # P_cr = pi^3 * R^3 * E * t / L^2 >= FS_buckle * P_eq
        # P_eq = F + 2*M/R
        P_eq = F + (2.0 * M / R)
        t_euler = (FS_buckle * P_eq * (L**2)) / (math.pi**3 * (R**3) * E)
        
        # 2. Local Shell Buckling:
        # sigma_comp_max = F / (2*pi*R*t) + M / (pi*R^2*t) = N_comp / t
        # sigma_cr = gamma * (E / sqrt(3*(1-nu^2))) * (t / R)
        # Requirement: sigma_comp_max <= sigma_cr / FS_buckle
        # => t^2 >= (FS_buckle * (F/(2*pi) + M/(pi*R))) / (gamma * E / sqrt(3*(1-nu^2)))
        coeff = gamma * E / math.sqrt(3.0 * (1.0 - nu**2))
        N_comp_R = (F / (2.0 * math.pi)) + (M / (math.pi * R))
        t_local = math.sqrt((FS_buckle * N_comp_R) / coeff)
        
        # 3. Material Yield / Failure:
        # A_x = sigma_x * t = - [F/(2*pi*R) + M/(pi*R^2) - p*R/2]
        # B_th = sigma_theta * t = p*R
        # Tau = V / (pi * R)
        A_x = (F / (2.0 * math.pi * R)) + (M / (math.pi * (R**2))) - (p * R / 2.0)
        B_th = p * R
        tau_val = V / (math.pi * R)
        
        if props['type'] == 'metal':
            # von Mises: sqrt(sigma_x^2 + sigma_theta^2 - sigma_x*sigma_theta + 3*tau^2) <= sigma_y / FS
            # Note on compressive side: sigma_x = -A_x / t, sigma_theta = +B_th / t
            # sigma_x^2 - sigma_x*sigma_theta + sigma_theta^2 = A_x^2 - (-A_x)*B_th + B_th^2 = A_x^2 + A_x*B_th + B_th^2
            vm_bracket = A_x**2 + (A_x * B_th) + B_th**2 + (3.0 * tau_val**2)
            t_yield = (math.sqrt(vm_bracket) * FS_yield) / props['sigma_y']
        else:
            # Composite quadratic interaction:
            # (sigma_x / Xc)^2 + (sigma_theta / Yt)^2 - (sigma_x * sigma_theta)/(Xc * Yt) + (tau / S)^2 <= (1 / FS)^2
            # With sigma_x = -A_x / t (compressive), -(-A_x)*B_th = +A_x * B_th
            term = ((A_x / props['Xc'])**2 + 
                    (B_th / props['Yt'])**2 + 
                    (A_x * B_th) / (props['Xc'] * props['Yt']) + 
                    (tau_val / props['S'])**2)
            t_yield = math.sqrt(term) * FS_yield
            
        t_req = max(t_yield, t_euler, t_local)
        
        if t_req == t_local:
            gov = "Local Shell"
        elif t_req == t_euler:
            gov = "Euler Column"
        else:
            gov = "Material Yield"
            
        # Cylinder mass
        mass = 2.0 * math.pi * R * L * t_req * rho
        
        results.append({
            'D_mm': D_mm, 'mat': mat_name,
            't_yield': t_yield * 1000, 't_euler': t_euler * 1000,
            't_local': t_local * 1000, 't_req': t_req * 1000,
            'mass': mass, 'gov': gov
        })
        
        print(f"{D_mm:<8} {mat_name:<18} {t_yield*1000:<12.3f} {t_euler*1000:<12.3f} {t_local*1000:<12.3f} {t_req*1000:<10.3f} {mass:<10.3f} {gov}")
