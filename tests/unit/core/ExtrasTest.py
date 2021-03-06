import openpnm as op
import scipy as sp
import pytest


class ExtrasTest:

    def setup_class(self):
        ws = op.Workspace()

    def teardown_class(self):
        ws = op.Workspace()
        ws.clear()

    def test_initialize_GenericNetwork_without_args(self):
        net = op.network.GenericNetwork()
        assert set(net.keys()) == set(['pore.all', 'throat.all'])
        assert net.Np == 0
        assert net.Nt == 0

    def test_initialize_GenericGeometry_without_args(self):
        obj = op.geometry.GenericGeometry()
        assert set(obj.keys()) == set(['pore.all', 'throat.all'])
        assert obj.Np == 0
        assert obj.Nt == 0
        assert len(obj.project) == 1

    def test_initialize_StickAndBall_without_args(self):
        obj = op.geometry.StickAndBall(settings={'freeze_models': True})
        assert set(obj.keys()) == set(['pore.all', 'throat.all'])
        assert len(obj.models.keys()) > 0
        assert obj.Np == 0
        assert obj.Nt == 0
        assert len(obj.project) == 1

    def test_initialize_GenericPhase_without_args(self):
        obj = op.phases.GenericPhase()
        assert obj.Np == 0
        assert obj.Nt == 0
        assert len(obj.project) == 1

    def test_initialize_Air_without_args(self):
        obj = op.phases.Air(settings={'freeze_models': True})
        assert len(obj.keys()) > 4
        assert len(obj.models.keys()) > 0
        assert obj.Np == 0
        assert obj.Nt == 0
        assert len(obj.project) == 1

    def test_initialize_GenericPhysics_without_args(self):
        obj = op.physics.GenericPhysics()
        assert set(obj.keys()) == set(['pore.all', 'throat.all'])
        assert obj.Np == 0
        assert obj.Nt == 0
        assert len(obj.project) == 1

    def test_init_Standard_physics_without_args(self):
        obj = op.physics.Standard(settings={'freeze_models': True})
        assert len(obj.models) > 0

    def test_init_geometris_without_args(self):
        obj = op.geometry.StickAndBall(settings={'freeze_models': True})
        assert len(obj.models) > 0

    def test_init_phases_without_args(self):
        obj = op.phases.Water(settings={'freeze_models': True})
        assert len(obj.models) > 0
        obj = op.phases.Air(settings={'freeze_models': True})
        assert len(obj.models) > 0
        obj = op.phases.Mercury(settings={'freeze_models': True})
        assert len(obj.models) > 0


if __name__ == '__main__':

    t = ExtrasTest()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()
