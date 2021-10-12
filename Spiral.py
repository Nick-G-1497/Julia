import matplotlib.pyplot as plt
import numpy as np
from math import *



j = complex(0, 1)
pi = 3.14

class Spiral:
    def __init__ (self):
        pass

    def _spiral(self, resolution_in_time):
        increments = np.linspace(0, 1, num = resolution_in_time)
        magnitude = [1 - increment for increment in increments]

        time = np.linspace(0, resolution_in_time, num = resolution_in_time)


        spiral = []
        i = 0
        for t in time:
            z = magnitude[i] * e**(j*t)
            spiral.append(z)
            i+=1
            

        return np.array(spiral)

    def getValues(self, resolution_in_time):
        return self._spiral(resolution_in_time)

    
    def plot (self):
        fig = plt.figure()


        spiral = self._spiral(10)
        plt.plot(spiral.real, spiral.imag)

        plt.show()



if __name__ == '__main__':
    s = Spiral()
    s.plot()