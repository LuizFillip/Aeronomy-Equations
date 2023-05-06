import numpy as np
import matplotlib.pyplot as plt
x = np.arange(10)

y = x**2


def gradient_cen_diff(x, y):
    """
    Compute the gradient of y with respect to x using central differences.
    
    Parameters:
        x (numpy.ndarray): 1D array of x values.
        y (numpy.ndarray): 1D array of y values.
    
    Returns:
        numpy.ndarray: 1D array of gradient values.
    """
    n = len(x)
    dx = np.diff(x)
    dy = np.diff(y)
    gradient = np.zeros(n)
    gradient[0] = dy[0] / dx[0]
    gradient[-1] = dy[-1] / dx[-1]
    gradient[1:-1] = (dy[1:] / dx[1:] + dy[:-1] / dx[:-1]) / 2
    #for i in range(1, n - 2):
    #    gradient[i] = (y[i+1] - y[i-1]) / (x[i+1] - x[i-1])
    
    return gradient
    

# np.gradient(x, y)
grad =  gradient_cen_diff(x, y)
plt.plot(x, y)
plt.plot(x, np.gradient(x, y, edge_order = 1))
plt.plot(x, grad)

def gradient_integrated(Ne, apex):
    Re = 6370.0
    L = 1 + (apex / Re)
    const = (1 / (Ne * Re * pow(L, 3)) )
    return (const * 
            np.gradient(Ne * pow(L, 3), 
                        apex, edge_order = 2))

