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
        moment,_=model.amplified_moment(0,2000,55e9,1e-6,1.5,.0015)
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
            for name,pressure,relief in [('wall_only',p,0),('closed_end',p,p*math.pi*s['ri']**2/s['A']),('unpressurised',0,0)]:
                for i in range(3601):
                    theta=i*math.pi/1800
                    x=-P/s['A']+relief+M*s['ro']/s['I']*math.cos(theta)
                    h=pressure*s['ro']/.002
                    tau=V/(math.pi*s['r']*.002)*math.sin(theta)
                    if mat.composite:
                        X=mat.Xc if x<0 else mat.Yt
                        fi=(x/X)**2+(h/mat.Yt)**2+abs(x*h)/(X*mat.Yt)+(tau/mat.S)**2
                    else:
                        fi=(x*x+h*h-x*h+3*tau*tau)/mat.yield_stress**2
                    dense=max(dense,fi)
            self.assertGreaterEqual(best['index']+1e-12,dense)
            self.assertAlmostEqual(best['index'],dense,places=5)

    def test_original_selected_design_not_accepted(self):
        x=model.shell_check(model.MATERIALS[4],.120,.0014)
        self.assertFalse(x['passes'])

    def test_thickness_tolerance_affects_capacity(self):
        nominal=model.shell_check(model.MATERIALS[0],.180,.002,replace(model.Basis(),thickness_retention=1))
        reduced=model.shell_check(model.MATERIALS[0],.180,.002)
        self.assertLess(reduced['pcr'],nominal['pcr'])
        self.assertGreater(reduced['utilisation'],nominal['utilisation'])

    def test_transfer_load_definition(self):
        self.assertAlmostEqual(model.moment_envelope(replace(model.Basis(),moment_case='transfer')),2*model.LOADS['M'])

    def test_composite_connection_is_explicitly_unresolved(self):
        x=model.shell_check(model.MATERIALS[4],.120,.003)
        self.assertIsNone(model.end_connection(model.MATERIALS[4],x))

class GeneratedResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((Path(__file__).parents[1]/'results/design.json').read_text())

    def test_selected_designs_pass_every_implemented_check(self):
        for key,bkey in [('selected','basis'),('transfer_selected','transfer_basis')]:
            saved=self.data[key]
            material=next(m for m in model.MATERIALS if m.name==saved['material'])
            basis=model.Basis(**self.data[bkey])
            actual=model.shell_check(material,saved['diameter_mm']/1000,saved['nominal_t_mm']/1000,basis)
            self.assertTrue(actual['passes'])
            for margin in actual['margins'].values():self.assertGreaterEqual(margin,0)
            joint=model.end_connection(material,actual,basis)
            for margin in joint['margins'].values():self.assertGreaterEqual(margin,0)
            self.assertAlmostEqual(joint['total_mass'],saved['objective_mass'])

    def test_connection_holes_and_washers_fit(self):
        for key in ['selected', 'transfer_selected']:
            j=self.data[key]['connection']
            d=j['bolt_d_mm']; rb=j['bolt_circle_mm']/2
            self.assertGreaterEqual(2*rb*math.sin(math.pi/j['bolts_per_end']),3*d)
            self.assertGreaterEqual(j['flange_width_mm'],2.2*d)
            self.assertGreaterEqual(j['flange_width_mm']/2,1.5*d)
            self.assertGreater(j['flange_width_mm'],j['hole_mm'])

    def test_discrete_bolt_group_recovers_force_and_moment(self):
        for key in ['selected', 'transfer_selected']:
            x=self.data[key];j=x['connection'];n=j['bolts_per_end']
            rb=j['bolt_circle_mm']/2000
            pressure_force=x['applied']['p']*math.pi*x['section']['ri']**2
            # Unclipped signed forces before the assumed prying multiplier.
            angles=[2*math.pi*k/n for k in range(n)]
            forces=[pressure_force/n+2*x['applied']['M']*math.cos(a)/(n*rb) for a in angles]
            self.assertAlmostEqual(sum(forces),pressure_force,places=7)
            self.assertAlmostEqual(sum(f*rb*math.cos(a) for f,a in zip(forces,angles)),x['applied']['M'],places=7)
            self.assertAlmostEqual(j['bolt_tension'],2*max(forces),places=7)

    def test_mass_budget_closes(self):
        for row in self.data['winners']:
            if row['connection']:
                j=row['connection']
                mass=row['shell_mass']+j['ring_extra_mass']+j['root_band_extra_mass']+j['fastener_mass']
                self.assertAlmostEqual(mass,row['objective_mass'])
                self.assertGreater(mass,row['shell_mass'])

    def test_all_seven_materials_reported(self):
        self.assertEqual({x['material'] for x in self.data['winners']},{m.name for m in model.MATERIALS})

    def test_manufacturing_grids(self):
        for row in self.data['winners']:
            mat=next(m for m in model.MATERIALS if m.name==row['material'])
            step=1 if mat.composite else .05
            self.assertAlmostEqual(row['nominal_t_mm']/step,round(row['nominal_t_mm']/step))

if __name__=='__main__':unittest.main()
