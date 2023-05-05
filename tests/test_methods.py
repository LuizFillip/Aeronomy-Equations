# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:55:54 2023

@author: Luiz
"""

import numpy as np
import matplotlib.pyplot as plt
x = np.arange(10)

y = x**2


grad = []
for i in range(len(x) - 1):
    num = (y[i + 1] - y[i - 1]) 
    den = 2 *(x[i + 1] - x[i - 1])
    grad.append(num / den)
    

# np.gradient(x, y)

plt.plot(x, y)
plt.plot(x, np.gradient(y, x, edge_order=2))
plt.plot(x[1:], grad)
