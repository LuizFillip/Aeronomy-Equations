from ionosphere import conductivity, test_data
import datetime as dt
from GEO import sites
import pytest


glat, glon = sites["saa"]["coords"]

kwargs = dict(
    dn = dt.datetime(2013, 1, 1, 21), 
    glat = glat, 
    glon = glon,
    hmin = 75,
    hmax = 300
    )

ds = test_data(**kwargs)

ne, nui, nue = tuple(ds.loc[ds.index == 100, :].values[0])

c = conductivity()



def test_ion_term_ratio(nui):
    
    ion_term = c.ion_term(nui)
    r_ion = c.ion_ratio(nui) 

    assert r_ion / (1 + pow(r_ion, 2)) == ion_term
    
def test_electron_ratio(nue):
    
    el_term = c.electron_term(nue)

    r_el = c.electron_ratio(nue)

    assert r_el / (1 + pow(r_el, 2)) == el_term
    
def test_total_cond_pedersen(ne, nui, nue):
    
    total = c.pedersen(ne, nui, nue)    

    e_part =  c.electron_term(ne, nue)
    i_part =  c.ion_term(ne, nui)

    assert total == i_part + e_part


def test_pedersen_above_130km():
    assert ...


def test_ion_mass_ratio():
        
    eff_mass = (2.66e-26 + 5.31e-26 + 4.99e-26) / 3
    pro_mass = c.proton_mass
    assert (eff_mass / pro_mass) == pytest.approx(25.82)

