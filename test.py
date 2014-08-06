import numpy as np
import matplotlib.pyplot as plt

N = 100
x = np.linspace(-10.0,10.0,N)
y  = 50.0*np.exp(-x**2)
size = 100.0*np.abs(np.sin(x))
plt.plot(x,y)
print len(size)
print len(x)
print type(size)
plt.scatter(x,y,s=size)

plt.show()