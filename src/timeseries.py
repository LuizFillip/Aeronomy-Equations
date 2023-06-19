import pandas as pd
import os
import ionosphere as io
from common import load_by_time

def scale_gradient():
    infile = 'D:\\database\\IRI2016Pyglow\\2013\\'
    files = os.listdir(infile)


    out = []
    for filename in files:
        df = load_by_time(infile + filename)
        
        df['L'] = io.scale_gradient(df['Ne'], df['alt'])
        print(filename)
        out.append(df.loc[df['alt'] == 300, ['Ne', 'L']])
        
    df = pd.concat(out)

    df.to_csv('scale_gradient.txt')
    return
    
