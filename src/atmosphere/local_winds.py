import GEO as gg
import pyIGRF
import atmosphere as atm 


def local_eff_wind(df, site = "saa"):
    lat, lon = gg.sites[site]["coords"]
    dec = []
    inc = []
    total = []
    dn = df.index[0]
    for alt in df.alt:
        
        d, i, _, _, _, _, f = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = alt, 
            year = gg.year_fraction(dn)
            )
        
        dec.append(d)
        inc.append(i)
        total.append(f)
        
    df["d"] = dec
    df["i"] = inc
    df['Bf'] = total
    
    wind = atm.effective_wind()
    
    df["zon_ef"] = wind.zonal(
        df["zon"], df["mer"], df["d"]
        )
    df["mer_ef"] = wind.meridional_perp(
        df["zon"], df["mer"], 
        df["d"], df["i"]
        )
    
    return df