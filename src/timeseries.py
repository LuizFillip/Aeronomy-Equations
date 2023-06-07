import pandas as pd


def cond_from_models(ds, B = 0.25e-04):
    
    """Compute conductivities from in models."""
    
    return pd.DataFrame(compute_parameters(ds, B = B))



def timeseries():
    mag = mm.load_mag()
    
    out = []
    
    for dn in mag.index:
    
        lat, lon = sites["saa"]["coords"]
            
        kwargs = dict(
              dn = dn, 
              glat = lat, 
              glon = lon,
              hmin = 150 
              )
        
        B = mag[mag.index == dn]["F"].item()
        
        ds =  cond_from_models(altrange_models(**kwargs), B = B)
        ds["alt"] = ds.index
        ds.index = [dn] * len(ds)
        out.append(ds)
        
    ts = pd.concat(out)
    
    
    ts.to_csv("conds.txt")
    