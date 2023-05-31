# -*- coding: utf-8 -*-
"""
Created on Mon May 29 15:29:55 2023

@author: Luiz
"""

import matplotlib.pyplot as plt
import numpy as np
import settings as s
import ionosphere as io
from GEO import sites 
import datetime as dt
import pandas as pd

df = pd.read_csv("conds.txt", index_col=0)
df.index = pd.to_datetime(df.index)

df = df.loc[(df["alt"] > 200) & (df["alt"] < 300)]

df["r"] = df["hall"] / df["perd"]
ts = pd.pivot_table(
    df, columns = df.index, 
    index = "alt", 
    values = "r")

fig, ax = plt.subplots()

ax.contourf(
    ts.columns, ts.index, ts.values, 50, cmap = "rainbow")

s.format_time_axes(ax)