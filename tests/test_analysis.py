import csv,json,math,random,unittest
from pathlib import Path
import analysis as model

ROOT=Path(__file__).resolve().parents[1]

class MechanicsTests(unittest.TestCase):
    def test_exact_notice_properties(self):
        expected=[(71.7,402,0,0,0),(113.8,704,0,0,0),(205,368,0,0,0),(45,176,0,0,0),
                  (52.3,0,480,400,160),(23.8,0,240,200,80),(33.3,0,160,240,64)]
        for b,values in zip(model.MATERIALS,expected):
            self.assertEqual((b.E/1e9,b.yield_stress/1e6,b.Xc/1e6,b.Yt/1e6,b.S/1e6),values)

    def test_loads_and_section(self):
        loads=model.flight_loads()
        self.assertAlmostEqual(loads['q'],24500)
        self.assertAlmostEqual(loads['V'],1465.12919162,places=7)
        self.assertAlmostEqual(loads['M'],2197.69378743,places=7)
        section=model.section(.120,.0014)
        self.assertAlmostEqual(section['r'],.0593)
        self.assertAlmostEqual(section['A']*1.5*1600,1.2519121060849192)

    def test_strength_extrema_against_direct_scan(self):
        section=model.section(.120,.002)
        for mat in [model.MATERIALS[0],model.MATERIALS[4]]:
            for path in ['wall_only','closed_end']:
                P,M,p,V=45000,4000,450000,2198
                function=model.composite_envelope if mat.composite else model.metal_strength
                actual=function(mat,section,.002,P,M,p,V,path)
                relief=p*math.pi*section['ri']**2/section['A'] if path=='closed_end' else 0.
                dense=0
                for i in range(12001):
                    theta=i*math.pi/12000
                    x=-P/section['A']+relief+M*section['ro']/section['I']*math.cos(theta)
                    h=p*section['ro']/.002
                    tau=V/(math.pi*section['r']*.002)*math.sin(theta)
                    value=(abs(x)/(mat.Xc if x<0 else mat.Yt)+h/mat.Yt+abs(tau)/mat.S
                           if mat.composite else math.sqrt(x*x+h*h-x*h+3*tau*tau)/mat.yield_stress)
                    dense=max(dense,value)
                self.assertGreaterEqual(actual['utilisation']+1e-12,dense)
                self.assertAlmostEqual(actual['utilisation'],dense,places=6)

    def test_load_factor_and_transfer_moment(self):
        a=model.evaluate(model.MATERIALS[4],122,1.52,'primary')
        b=model.evaluate(model.MATERIALS[4],122,1.52,'transfer')
        loads=model.flight_loads()
        for key,value in [('P',loads['F']),('V',loads['V']),('p',loads['p'])]:
            self.assertEqual(a['applied'][key],1.1*value)
        self.assertEqual(b['applied']['first_order_M'],1.1*(loads['M']+loads['V']*1.5))

    def test_pressure_shear_energy_inequality(self):
        random.seed(2106)
        for _ in range(2000):
            c,s,h=(random.uniform(.01,20) for _ in range(3))
            x,y=(random.uniform(-5,5) for _ in range(2))
            actual=c*x*x+2*s*x*y-h*y*y
            bound=(c+s*s/h)*x*x
            self.assertLessEqual(actual,bound+1e-10)
            self.assertAlmostEqual(bound-actual,h*(y-s*x/h)**2,places=8)
        with self.assertRaises(ValueError):model.compression_bound(1,2,3,0)

    def test_compression_envelope_against_dense_circumference(self):
        for a,b,s,h in [(2,8,1,3),(2,1,9,3),(1,0,2,1)]:
            exact,c=model.compression_bound(a,b,s,h)
            dense=max(a-b*math.cos(i*math.pi/10000)+s*s/h*math.sin(i*math.pi/10000)**2 for i in range(10001))
            self.assertGreaterEqual(exact+1e-10,dense)
            self.assertAlmostEqual(exact,dense,places=5)

    def test_composite_bound_for_psd_interactions(self):
        random.seed(14)
        for _ in range(100):
            columns=[[random.uniform(-1,1) for _ in range(3)] for j in range(3)]
            unit=[[v/math.sqrt(sum(x*x for x in col)) for v in col] for col in columns]
            z=[random.uniform(-2,2) for j in range(3)]
            quadratic=sum(sum(unit[i][k]*z[i] for i in range(3))**2 for k in range(3))
            self.assertLessEqual(quadratic,sum(abs(v) for v in z)**2+1e-10)

    def test_beam_solution_against_fourier_series(self):
        E,I,L=71700.,1e6,1500.
        pcr=math.pi**2*E*I/L**2
        for fraction in [0,.05,.25,.75]:
            P=fraction*pcr;M0=2e6
            actual=model.beam_envelope(P,M0,E,I,L)
            y=sum(4*M0*(-1)**i/((2*i+1)*math.pi*(E*I*((2*i+1)*math.pi/L)**2-P)) for i in range(2000))
            self.assertAlmostEqual(actual[0]/(M0+P*y),1,places=9)
        self.assertIsNone(model.beam_envelope(pcr,1,E,I,L))

    def test_gust_does_not_scale_thrust_or_pressure(self):
        mat=model.MATERIALS[0]
        a=model.evaluate(mat,140,1.3,gust=20);b=model.evaluate(mat,140,1.3,gust=24)
        self.assertEqual(a['applied']['P'],b['applied']['P'])
        self.assertEqual(a['applied']['p'],b['applied']['p'])
        self.assertAlmostEqual(b['applied']['V']/a['applied']['V'],math.atan(.12)/math.atan(.1))

    def test_no_yield_cap_acceptance(self):
        mat=model.MATERIALS[0]
        x=model.evaluate(mat,100,4)
        self.assertFalse(x['applicability']['elastic_capacity'])
        self.assertGreater(x['critical_axial_stress'],mat.yield_stress)
        self.assertFalse(x['passes'])

    def test_integer_search_against_exhaustive_search(self):
        for mat in model.MATERIALS:
            for case in ['primary','transfer']:
                for D in [70,90,110,130,150,200,250,300]:
                    found=None
                    for j in range(1,math.floor(model.maximum_wall(mat,D)/.01+1e-10)+1):
                        x=model.evaluate(mat,D,j*.01,case)
                        if x['passes']:found=x;break
                    fast=model.minimum_wall(mat,D,case)
                    self.assertEqual(None if found is None else found['nominal_t_mm'],None if fast is None else fast['nominal_t_mm'])

class SavedSolutionTests(unittest.TestCase):
    def test_selected_geometry_and_search(self):
        d=json.loads((ROOT/'data/solution.json').read_text())
        with (ROOT/'data/trade_study.csv').open() as f:rows=list(csv.DictReader(f))
        for row in d['search']['material_minima']:
            mat=next(m for m in model.MATERIALS if m.name==row['material'])
            actual=model.evaluate(mat,row['diameter_mm'],row['nominal_t_mm'],'transfer')
            self.assertTrue(actual['passes'])
            self.assertAlmostEqual(row['shell_mass'],actual['shell_mass'])
            self.assertEqual(row['shell_mass'],min(float(r['shell_mass']) for r in rows if r['material']==mat.name))
            self.assertFalse(model.evaluate(mat,row['diameter_mm'],row['nominal_t_mm']-.01,'transfer')['passes'])
        self.assertEqual(d['selected']['shell_mass'],min(r['shell_mass'] for r in d['search']['material_minima']))
        for case,row in d['load_cases'].items():
            self.assertTrue(row['passes'])
            self.assertEqual((row['diameter_mm'],row['nominal_t_mm']),(d['selected']['diameter_mm'],d['selected']['nominal_t_mm']))
        for coarse,fine in zip(d['search']['material_minima'],d['search']['refined_minima']):
            self.assertTrue(fine['passes'])
            self.assertLessEqual(fine['shell_mass'],coarse['shell_mass']+1e-10)

    def test_report_verification_is_current(self):
        import hashlib
        result=ROOT/'data/solution.json'
        verification=json.loads((ROOT/'data/verification.json').read_text())
        self.assertTrue(verification['checks_passed'])
        self.assertEqual(hashlib.sha256(result.read_bytes()).hexdigest(),verification['input_sha256'])

if __name__=='__main__':unittest.main()
