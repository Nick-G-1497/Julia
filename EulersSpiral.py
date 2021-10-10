##
# @package EulersSpiral
# Module for creating the parameteric curve that takes the path of a spiral in the complex plane

import matplotlib.pyplot as plt
import numpy as np
from math import *
from scipy.special import fresnel

##
# Module for creating the parameteric curve that takes the path of a spiral in the complex plane
# @todo transcibe this to the complex plains using identities 
# @todo find those identities
class EulersSpiral:
    def __init__ (self, resolution_in_time):
        self._resolution_in_time = resolution_in_time
        self.time = np.linspace(-10, 10, resolution_in_time)


    ##
    # Functions used to get all the points which ly on the curve
    def getValues(self):
        return fresnel(self.time) 

    ##
    # Function used to plot the curve and show the output to the user using a
    # distinct color mapping
    # @param cmap is the colormapping supported my matplotlib
    def show_plot(self, cmap):
        fig = plt.figure()
        plt.plot(*fresnel(self.time), c = cmap)
        plt.axis('off')
        plt.show()



if __name__ == '__main__':
    eulersSpiral = EulersSpiral(1000)

    eulersSpiral.show_plot('Red')
