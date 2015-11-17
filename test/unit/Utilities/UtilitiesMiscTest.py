import OpenPNM
import scipy as sp


class UtilitiesMiscTest:

    def setup_class(self):
        self.net = OpenPNM.Network.Cubic(shape=[10, 10, 10])

    def test_find_path_single_pore_pair(self):
        a = self.net.find_path([0, 1])
        assert sorted(list(a.keys())) == ['pores', 'throats']
        assert len(a['pores']) == 1
        assert len(a['throats']) == 1
        assert len(a['pores'][0]) == 2
        assert len(a['throats'][0]) == 1

    def test_find_path_multiple_pore_pairs(self):
        a = self.net.find_path(([0, 1], [3, 6], [0, 8]))
        assert len(a['pores']) == 3
        assert len(a['throats']) == 3

    def test_find_path_with_weights(self):
        w = sp.ones_like(self.net.Ts)
        w[0] = self.net.Nt + 1
        a = self.net.find_path(([0, 1]), weights=w)
        assert len(a['pores'][0]) > 2
        assert len(a['throats'][0]) > 1
