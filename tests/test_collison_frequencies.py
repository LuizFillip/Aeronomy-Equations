import numpy as np
from ionosphere import collision_frequencies

def test_ion_neutrals():
    assert np.isclose(collision_frequencies.ion_neutrals(Tn=1e6, O=1e12, O2=1e12, N2=1e12), 2.05e+09, rtol=1e-2)
    assert np.isclose(collision_frequencies.ion_neutrals(Tn=1e5, O=1e10, O2=1e11, N2=1e12), 1.88e+08, rtol=1e-2)

def test_electrons_neutrals():
    assert np.isclose(collision_frequencies.electrons_neutrals(O=1e11, O2=1e10, N2=1e12, He=1e12, H=1e10, Te=1e4), 5.16e+08, rtol=1e-2)
    assert np.isclose(collision_frequencies.electrons_neutrals(O=1e12, O2=1e11, N2=1e12, He=1e11, H=1e10, Te=1e6), 2.26e+12, rtol=1e-2)
