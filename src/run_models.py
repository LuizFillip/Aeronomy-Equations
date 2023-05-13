# -*- coding: utf-8 -*-
"""
Created on Fri May 12 21:49:19 2023

@author: Luiz
"""

import pandas as pd
import ionosphere as io
from models import altrange_models

def test_data(**kwargs):
    
    df = altrange_models(**kwargs)

    nu = io.collision_frequencies()

    nui = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
        
    nue = nu.electrons_neutrals(
        df["O"], df["O2"], df["N2"],
        df["He"], df["H"], df["Te"]
    )    
    return pd.DataFrame({"ne": df["ne"].copy(), 
                         "nui": nui, 
                         "nue": nue})