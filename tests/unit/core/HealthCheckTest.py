import openpnm as op
import numpy as np
import pytest


class HealthCheckTest:

    def setup_class(self):
        self.ws = op.core.Workspace()
        self.ws.clear()
        self.proj = self.ws.new_project()
        self.net = op.network.Cubic(shape=[2, 2, 2], project=self.proj)
        Ps = self.net.pores('top')
        Ts = self.net.find_neighbor_throats(pores=Ps)
        self.geo1 = op.geometry.GenericGeometry(network=self.net, pores=Ps,
                                                throats=Ts)
        Ps = self.net.pores('bottom')
        Ts = ~self.net.tomask(throats=Ts)
        self.geo2 = op.geometry.GenericGeometry(network=self.net, pores=Ps,
                                                throats=Ts)
        self.phase1 = op.phases.GenericPhase(network=self.net)
        self.phase2 = op.phases.GenericPhase(network=self.net)
        self.phys11 = op.physics.GenericPhysics(network=self.net,
                                                phase=self.phase1,
                                                geometry=self.geo1)
        self.phys12 = op.physics.GenericPhysics(network=self.net,
                                                phase=self.phase1,
                                                geometry=self.geo2)
        self.phys21 = op.physics.GenericPhysics(network=self.net,
                                                phase=self.phase2,
                                                geometry=self.geo1)
        self.phys22 = op.physics.GenericPhysics(network=self.net,
                                                phase=self.phase2,
                                                geometry=self.geo2)

    def test_check_geometry_health_good(self):
        proj = self.proj
        h = proj.check_geometry_health()
        a = list(h.keys())
        b = ['overlapping_pores', 'undefined_pores', 'overlapping_throats',
             'undefined_throats']
        # Ensure correct items are checked
        assert set(a) == set(b)
        # Ensure all items found no problems (0 length results)
        assert ~np.any([len(item) for item in h.values()])

    def test_check_geometry_health_undefined_pores(self):
        proj = self.ws.copy_project(self.proj)
        network = proj.network
        temp = np.copy(network['pore.geo_01'])
        network['pore.geo_01'] = False
        h = proj.check_geometry_health()
        assert np.all(h['undefined_pores'] == np.where(temp)[0])
        del self.ws[proj.name]

    def test_check_geometry_health_undefined_throats(self):
        proj = self.ws.copy_project(self.proj)
        network = proj.network
        temp = np.copy(network['throat.geo_01'])
        network['throat.geo_01'] = False
        h = proj.check_geometry_health()
        assert np.all(h['undefined_throats'] == np.where(temp)[0])
        del self.ws[proj.name]

    def test_check_geometry_health_overlapping_pores(self):
        proj = self.ws.copy_project(self.proj)
        network = proj.network
        temp = np.copy(network['pore.geo_02'])
        network['pore.geo_01'] = True
        h = proj.check_geometry_health()
        assert np.all(h['overlapping_pores'] == np.where(temp)[0])
        del self.ws[proj.name]

    def test_check_geometry_health_overlapping_throats(self):
        proj = self.ws.copy_project(self.proj)
        network = proj.network
        temp = np.copy(network['throat.geo_02'])
        network['throat.geo_01'] = True
        h = proj.check_geometry_health()
        assert np.all(h['overlapping_throats'] == np.where(temp)[0])
        del self.ws[proj.name]

    def test_check_physics_health_good(self):
        proj = self.proj
        h = proj.check_physics_health(self.phase1)
        a = list(h.keys())
        b = ['overlapping_pores', 'undefined_pores', 'overlapping_throats',
             'undefined_throats']
        # Ensure correct items are checked
        assert set(a) == set(b)
        # Ensure all items found no problems (0 length results)
        assert ~np.any([len(item) for item in h.values()])

    def test_check_physics_health_undefined_pores(self):
        proj = self.ws.copy_project(self.proj)
        phys = self.phys11
        phase = proj.find_phase(phys)
        temp = np.copy(phase['pore.'+phys.name])
        phase['pore.'+phys.name] = False
        h = proj.check_physics_health(phase)
        assert np.all(h['undefined_pores'] == np.where(temp)[0])
        del self.ws[proj.name]

    def test_check_physics_health_undefined_throats(self):
        proj = self.ws.copy_project(self.proj)
        phys = self.phys11
        phase = proj.find_phase(phys)
        temp = np.copy(phase['throat.'+phys.name])
        phase['throat.'+phys.name] = False
        h = proj.check_physics_health(phase)
        assert np.all(h['undefined_throats'] == np.where(temp)[0])
        del self.ws[proj.name]

    def test_check_physics_health_overlapping_pores(self):
        proj = self.ws.copy_project(self.proj)
        phys = self.phys11
        phase = proj.find_phase(phys)
        temp = np.copy(phase['pore.'+phys.name])
        phase['pore.'+phys.name] = True
        h = proj.check_physics_health(phase)
        assert np.all(h['overlapping_pores'] == np.where(temp == 0)[0])
        del self.ws[proj.name]

    def test_check_physics_health_overlapping_throats(self):
        proj = self.ws.copy_project(self.proj)
        phys = self.phys11
        phase = proj.find_phase(phys)
        temp = np.copy(phase['throat.'+phys.name])
        phase['throat.'+phys.name] = True
        h = proj.check_physics_health(phase)
        assert np.all(h['overlapping_throats'] == np.where(temp == 0)[0])
        del self.ws[proj.name]


if __name__ == '__main__':

    t = HealthCheckTest()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()
