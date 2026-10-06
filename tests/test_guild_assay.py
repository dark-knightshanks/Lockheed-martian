import csv,json,math,random,unittest
from pathlib import Path
import revised_analysis as model

ROOT=Path(__file__).resolve().parents[1]

class RevisedMechanicsTests(unittest.TestCase):
    def test_exact_notice_properties(self):
        expected=[(71.7,402,0,0,0),(113.8,704,0,0,0),(205,368,0,0,0),(45,176,0,0,0),
                  (52.3,0,480,400,160),(23.8,0,240,200,80),(33.3,0,160,240,64)]
        for a,b,values in zip(model.MATERIALS,model.B_MATERIALS,expected):
            self.assertEqual((b.E/1e9,b.yield_stress/1e6,b.Xc/1e6,b.Yt/1e6,b.S/1e6),values)
            self.assertEqual((a.density,a.nu),(b.density,b.nu))

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
        mat=model.B_MATERIALS[0]
        a=model.evaluate(mat,140,1.3,gust=20);b=model.evaluate(mat,140,1.3,gust=24)
        self.assertEqual(a['applied']['P'],b['applied']['P'])
        self.assertEqual(a['applied']['p'],b['applied']['p'])
        self.assertAlmostEqual(b['applied']['V']/a['applied']['V'],math.atan(.12)/math.atan(.1))

    def test_no_yield_cap_acceptance(self):
        mat=model.B_MATERIALS[0]
        x=model.evaluate(mat,100,4)
        self.assertFalse(x['applicability']['elastic_capacity'])
        self.assertGreater(x['critical_axial_stress'],mat.yield_stress)
        self.assertFalse(x['passes'])

    def test_integer_search_against_exhaustive_search(self):
        for mat in model.B_MATERIALS:
            for case in ['primary','transfer']:
                for D in [70,90,110,130,150,200,250,300]:
                    found=None
                    for j in range(1,math.floor(model.maximum_wall(mat,D,'B')/.01+1e-10)+1):
                        x=model.evaluate(mat,D,j*.01,case)
                        if x['passes']:found=x;break
                    fast=model.minimum_wall(mat,D,case)
                    self.assertEqual(None if found is None else found['nominal_t_mm'],None if fast is None else fast['nominal_t_mm'])

class SavedRevisionTests(unittest.TestCase):
    def test_saved_winners_and_sweep_minima(self):
        data=json.loads((ROOT/'data/guild_assay/response.json').read_text())
        for case,c in data['cases'].items():
            with (ROOT/f'data/guild_assay/{case}_trade_study.csv').open() as f:
                rows=list(csv.DictReader(f))
            for row in c['winners']:
                mat=next(m for m in model.B_MATERIALS if m.name==row['material'])
                actual=model.evaluate(mat,row['diameter_mm'],row['nominal_t_mm'],case)
                self.assertTrue(actual['passes'])
                self.assertAlmostEqual(row['shell_mass'],actual['shell_mass'])
                self.assertEqual(row['shell_mass'],min(float(r['shell_mass']) for r in rows if r['material']==mat.name))
                self.assertFalse(model.evaluate(mat,row['diameter_mm'],row['nominal_t_mm']-.01,case)['passes'])
            self.assertEqual(c['selected']['shell_mass'],min(r['shell_mass'] for r in c['winners']))
            self.assertTrue(all(r['passes'] for r in c['fine_winners']))
            # Finer grid contains every nominal-grid design.
            for coarse,fine in zip(c['winners'],c['fine_winners']):
                self.assertLessEqual(fine['shell_mass'],coarse['shell_mass']+1e-10)
        self.assertTrue(data['transfer_design_under_primary']['passes'])

if __name__=='__main__':unittest.main()
