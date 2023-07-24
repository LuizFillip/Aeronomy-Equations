import pandas as pd
import ionosphere as io

class split_regions:
    
    def __init__(self, df, names = None):
        
        
        if names is None:
            self.names = [
                "perd", "zeq", "mlat",
                 "glon", "glat", "apex"]
        
        self.c = io.conductivity()
        self.df = df
        
    @staticmethod
    def filter_layers(df, base, top):
        ds = df.copy()
        return ds.loc[
            (ds["zeq"] >= base) & (ds["zeq"] <= top)
            ]

    @property
    def lower_region_E(self):
        
        lower_E = self.filter_layers(self.df, 75, 100)
            
        lower_E["perd"] = self.c.electron_term(
            lower_E["Ne"], 
            lower_E["nue"]
            )
        return lower_E.loc[:, self.names]
    
    @property
    def upper_region_E(self):
        
        upper_E = self.filter_layers(self.df, 100, 150)
        
        upper_E["perd"] = self.c.ion_term(
            upper_E["Ne"], 
            upper_E["nui"]
            )
                
        return upper_E.loc[:, self.names]
    
    @property
    def region_E(self):
        return pd.concat(
            [self.lower_region_E, self.upper_region_E]
            )
    
    @property
    def region_F(self):
                
        region_F = self.filter_layers(self.df, 150, 1000)
                
        region_F["perd"] = self.c.pedersen_F(
            region_F["Ne"], region_F["nui"]
            )
        
        return region_F.loc[:, self.names]
    
    def total(self):
        ds = self.df.copy()
        ds["perd"] = self.c.pedersen(
            ds["Ne"], ds["nui"], ds["nue"]
            )
        return ds.loc[:, self.names]




