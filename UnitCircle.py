##
# @package UnitCircle
# Module for creating the unit circle

import matplotlib.pyplot as plt
import numpy as np
from math import *

##
# The ratio of a circle's circumferance to its diameter for every circle
pi = 3.14

##
# The square root of negative one
# @details Using j instead of i because "imaginary" is a terrible name for describing the behavior of complex numbers. 
# The history of why we refer to imaginary numbers as follows: Renee Decartes ran into the issue of getting a 
# negative number in the radical. Convertionally, this would be regarded as unsolvable with the current doctrine 
# and state of mathematics. He asked the question if you pulled out the square root of negative one as a constant, 
# mechanically as conceptually how would you deal with this. He relized that you can graphically represent numbers 
# of these sort as 2 dimensional. He didn't think anyone would ever use this constant ever again because it made no s
# ense to him. There is written record that he came up with the most ridulous name he could think of so he named them 
# imaginary numbers. Euler late proposed a slight alternate naming which they are also refer to as complex number since 
# the have 2D properties.  Historically j has also been used by electrical engineers because i is already current. 
j = complex(0, 1)

##complex
# Module used for calculating the unit circle
class UnitCircle:
	
	## 
	# Constuctor of the class
	# @params resolution or number of discrete points in the returned unit circle vector
	def __init__(self, resolution):
		self._resolution = resolution
		
	##
	##Calculate the unit circle with a variable resolution using Euler's method and complex numbers. 
	# Very inefficent to calculate it in this way but were thinking in terms of complex numbers and the math is pretty.
	#
	# @note https://observablehq.com/@jonhelfman/unit-circle-complex-plane
	# @note the unit circle gets built starting at 12 o'clock and adding values in the counter clockwise direction 
	def getValues(self):
		phases = np.linspace(pi/2, 27*pi/2, self._resolution)
		
		# real = []
		# imaginary = []
		# real = [complex(( exp(j*phase) + exp(-j*phase) ) / 2 ) for phase in phases	
		# imaginary = [complex(( exp(j*phase) + exp(-j*phase) ) / (2*j)) for phase in phases]
		
		self._circle = [e**(j*phase) for phase in phases]
		
		return self._circle
		
	##
	# Plot the unit circle
	def plot(self):
		fig = plt.figure()
		
		self.getValues()
		real = [point.real for point in self._circle]
		imag = [point.imag for point in self._circle]
		plt.plot(real, imag)
		
		plt.show()


