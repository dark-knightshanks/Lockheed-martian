import json
import math
import unittest
from dataclasses import replace
from pathlib import Path
import parametric_diameter_study as model

class MechanicsTests(unittest.TestCase):
    def test_loads_from_brief(self):
        x=model.flight_loads()
        self.assertAlmostEqual(x['q'],24500)
        self.assertAlmostEqual(x['V'],1465.12919162,places=7)
        self.assertAlmostEqual(x['M'],2197.69378743,places=7)

    def test_known_annulus(self):
        s=model.section(.120,.0014)
        self.assertAlmostEqual(s['r'],.0593)
        self.assertAlmostEqual(s['A']*1.5*1600,1.2519121060849192)
        self.assertAlmostEqual(math.pi**2*55e9*s['I']/1.5**2,221300.51119495928,places=5)

    def test_zero_axial_load_has_no_amplification(self):
        moment,_=model.amplified_moment(0,2000,55e9,1e-6,1.5)
        self.assertEqual(moment,2000)

    def test_secant_known_quarter_critical_load(self):
        E,I,L=55e9,1e-6,1.5
        critical=math.pi**2*E*I/L**2
        moment,_=model.amplified_moment(critical/4,1000,E,I,L)
        self.assertAlmostEqual(moment,1000*math.sqrt(2))

    def test_euler_singularity_rejected(self):
        E,I,L=55e9,1e-6,1.5
        critical=math.pi**2*E*I/L**2
        self.assertTrue(math.isinf(model.amplified_moment(critical,1000,E,I,L)[0]))

    def test_pure_bending_has_zero_axial_resultant(self):
        # Numerically integrate prescribed thin-shell stress, independent of model.
        n=3600;r=.08;t=.002;M=2197.69378743
        force=sum(M/(math.pi*r*r*t)*math.cos(2*math.pi*i/n)*t*r*2*math.pi/n for i in range(n))
        self.assertAlmostEqual(force,0,places=7)

    def test_quadratic_maximum_finds_interior(self):
        v,c=model.quadratic_maximum(lambda x:5-(x-.3)**2,-1,1)
        self.assertAlmostEqual(v,5)
        self.assertAlmostEqual(c,.3)

    def test_angular_strength_matches_dense_independent_scan(self):
        s=model.section(.120,.002)
        for mat in [model.MATERIALS[0],model.MATERIALS[4]]:
            P,M,p,V=45000,4000,450000,2198
            best,states=model.strength_envelope(mat,s,.002,P,M,p,V)
            dense=0
            for name,pressure,relief in [('wall_only',p,0)]:
                for i in range(3601):
                    theta=i*math.pi/1800
                    x=-P/s['A']+relief+M*s['ro']/s['I']*math.cos(theta)
                    h=pressure*s['ro']/.002
                    tau=V/(math.pi*s['r']*.002)*math.sin(theta)
                    if mat.composite:
                        X=mat.Xc if x<0 else mat.Yt
                        fi=(x/X)**2+(h/mat.Yt)**2+(tau/mat.S)**2
                    else:
                        fi=(x*x+h*h-x*h+3*tau*tau)/mat.yield_stress**2
                    dense=max(dense,fi)
            self.assertGreaterEqual(best['index']+1e-12,dense)
            self.assertAlmostEqual(best['index'],dense,places=5)

    def test_team_factor_applies_once_without_extra_allowances(self):
        b=model.Basis();x=model.shell_check(model.MATERIALS[0],.180,.002,b)
        self.assertEqual(b.load_multiplier,1.1)
        self.assertEqual(b.required_safety_factor,1.1)
        self.assertEqual(x['minimum_t_mm'],2)
        self.assertEqual(x['applied']['P'],1.1*model.LOADS['F'])
        self.assertEqual(x['applied']['V'],1.1*model.LOADS['V'])
        self.assertEqual(x['applied']['first_order_M'],1.1*model.LOADS['M'])
        self.assertEqual(x['applied']['p'],1.1*model.LOADS['p'])
        phi=math.sqrt(x['r_over_t'])/16
        self.assertAlmostEqual(x['gx'],1-.901*(1-math.exp(-phi)))
        self.assertAlmostEqual(x['gb'],1-.731*(1-math.exp(-phi)))
        self.assertAlmostEqual(x['utilisations']['ovalisation'],x['applied']['M']/x['classical_brazier'])

    def test_only_prescribed_pressure_in_primary_strength_case(self):
        x=model.shell_check(model.MATERIALS[0],.180,.002)
        self.assertEqual([r['case'] for r in x['strength_states']],['wall_only'])

    def test_closed_end_strength_is_an_explicit_scenario(self):
        mat=model.MATERIALS[0];s=model.section(.18,.002)
        _,wall=model.strength_envelope(mat,s,.002,30000,2200,300000,1465)
        _,closed=model.strength_envelope(mat,s,.002,30000,2200,300000,1465,'closed_end')
        self.assertEqual(closed[0]['case'],'closed_end')
        self.assertNotEqual(wall[0]['index'],closed[0]['index'])

    def test_transfer_load_definition(self):
        self.assertAlmostEqual(model.moment_envelope(replace(model.Basis(),moment_case='transfer')),2*model.LOADS['M'])

class GeneratedResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((Path(__file__).parents[1]/'data/original/design.json').read_text())

    def test_all_candidates_recompute_and_total_mass_is_unresolved(self):
        for group,bkey in [('winners','basis'),('transfer_winners','transfer_basis')]:
            for saved in self.data[group]:
                mat=next(m for m in model.MATERIALS if m.name==saved['material'])
                basis=model.Basis(**self.data[bkey])
                actual=model.shell_check(mat,saved['diameter_mm']/1000,saved['nominal_t_mm']/1000,basis)
                self.assertTrue(actual['passes'])
                self.assertAlmostEqual(actual['shell_mass'],saved['shell_mass'])
                self.assertIsNone(saved['assembly_mass'])
                self.assertIsNone(saved['connection'])
                self.assertEqual(saved['competition_compliance'],'unresolved')
                # The immediately thinner point must fail or lie outside applicability.
                thinner=model.shell_check(mat,saved['diameter_mm']/1000,
                    (saved['nominal_t_mm']-basis.thickness_step_mm)/1000,basis)
                self.assertFalse(thinner['passes'])

    def test_all_seven_materials_in_every_scenario(self):
        names={m.name for m in model.MATERIALS}
        self.assertEqual({r['material'] for r in self.data['winners']},names)
        self.assertEqual({r['material'] for r in self.data['transfer_winners']},names)
        for f in [1,1.1,1.25,1.5,2]:
            self.assertEqual({r['material'] for r in self.data['sensitivities'] if r['load_multiplier']==f},names)

    def test_grid_is_numerical_not_an_invented_ply_schedule(self):
        for row in self.data['winners']:
            step=self.data['basis']['thickness_step_mm']
            self.assertAlmostEqual(row['nominal_t_mm']/step,round(row['nominal_t_mm']/step))

    def test_team_factor_is_not_full_structural_verification(self):
        self.assertEqual(self.data['required_safety_factor'],1.1)
        self.assertEqual(self.data['selected']['structural_verification'],'incomplete')
        self.assertIn('transverse_shear_surrogate',self.data['selected']['assumption_flags'])
        self.assertIsNone(self.data['assembly_mass'])
        self.assertIn('unresolved',self.data['status'])

if __name__=='__main__':unittest.main()
