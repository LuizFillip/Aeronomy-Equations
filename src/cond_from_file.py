from GEO import sites
import pandas as pd
import ionosphere as io
from models import altrange_models, point_msis, point_models
from utils import datetime_from_fn
import atmosphere as atm
    
infile = "database/Digisonde/SAA0K_20130319(078)_pro"
# process_sites(infile)

df = pd.read_csv(infile, index_col = 0)

df.index= pd.to_datetime(df.index)


# nui = nu.ion_neutrals(
#     df["Tn"], df["O"], 
#     df["O2"], df["N2"]
#     )
    
def load_mag():

    df = pd.read_csv("mag.txt", index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    df = df.resample("10min").asfreq()
    
    df["F"] = df["F"] * 1e-9
    return df

# 
mag = load_mag()

lat, lon = sites["saa"]["coords"]

out = {"perd": [], "hall": [], 
        "B": [], "dn": [], "ne": [], 
        "alt": []}

for i in range(len(df)):
    dn = df.index[i]
    zeq = df.iloc[i, 0]
    ne = df.iloc[i, 2]
    
    kwargs = dict(dn = dn, 
                  zeq = zeq, 
                  glat = lat, 
                  glon = lon)
    
    B = mag[mag.index == dn]["F"].item()
    
    msi = point_models(**kwargs)
    
    nu = io.collision_frequencies()


    nui = nu.ion_neutrals(msi["Tn"], msi["O"], msi["O2"], msi["N2"])
    nue = nu.electrons_neutrals(
        msi["O"], msi["O2"], msi["N2"],
        msi["He"], msi["H"], msi["te"]
    )

    c = io.conductivity(B = B)
    out["B"].append(B)
    out["dn"].append(dn)
    out["alt"].append(zeq)
    out["ne"].append(ne)
    out["perd"].append( c.pedersen(ne, nui, nue))
    out["hall"].append(c.hall(ne, nui, nue))
    
    
ds = pd.DataFrame(out)

ds.to_csv("cond_iono.txt")

