import matplotlib.pyplot as plt
import numpy as np
from math import *

'''
The ratio of a circle's circumferance to its diameter for every circle
'''
pi = 3.14

''' 
j is equal to the square root of negative one. Using j instead of i because "imaginary" is a terrible name for describing the behavior of complex numbers. Historically it has also been used by electrical engineers because i is already current. 
'''
j = complex(0, 1)

'''
Module used for calculating the unit circle
'''
class UnitCircle:
	def __init__(self, resolution):
		self._resolution = resolution
		
	'''
	Calculate the unit circle with a variable resolution using Euler's method and complex numbers. 
	Very inefficent to calculate it in this way but were thinking in terms of complex numbers and the math is pretty.
	
	https://observablehq.com/@jonhelfman/unit-circle-complex-plane
	'''
	def getValues(self):
		phases = np.linspace(pi/4, 5*pi/4, self._resolution)
		
		real = []
		imaginary = []
		
		# real = [complex(( exp(j*phase) + exp(-j*phase) ) / 2 ) for phase in phases]
		
		# imaginary = [complex(( exp(j*phase) + exp(-j*phase) ) / (2*j)) for phase in phases]
		
		self._circle = [e**(j*phase) for phase in phases]
		
		return self._circle
		
	'''
	Plot the unit circle
	'''
	def plot(self):
		fig = plt.figure()
		
		self.getValues()
		real = [point.real for point in self._circle]
		imag = [point.imag for point in self._circle]
		plt.plot(real, imag)
		
		plt.show()




		
''' 
Julia is a tool built for generating various julia sets. A julia set is defined by a function repeated or itterated numerous time. If due to the starting point the funtion diverges over itteration then the point is said not to be in the set. If remains inside an arbitrary finite space we define then it is said to be in the set.

Z = Zprev * Zprev + c
where c is a constant we define in the complex plane and we do this a bunch of times and see if i goes to infinity
'''
class Julia ():
		
	_resolution = 512
	_max_itt = 70
	_c = complex(-0.6, 0.4)
	_cmap = 'Purples'

	''' 
	Function enabled to test whether the constant value defined is within this specific julia set that pertains to the constant value we defined for the set. 
	'''
	def _julia_set(self, h_range, w_range, max_iterations):
		y, x = np.ogrid[1.4: -1.4: h_range*1j, -1.4: 1.4: w_range*1j]
		z_array = x + y*1j
		a = self._c
		iterations_till_divergence = max_iterations + np.zeros(z_array.shape)
		
			
		for h in range(h_range):
				for w in range(w_range):
					z = z_array[h][w]
					for i in range(max_iterations):
						z = z**2 + a
						if z * np.conj(z) > 4:
							iterations_till_divergence[h][w] = i
							break

		return iterations_till_divergence
		
	''' 
	The Mandelbrot Set is a special case Julia set the contant value you itterate with is the value you start with. The Mandelbrot set is said to be a map of all Julia sets
	
	z_next = z_prev * z_prev + z0
	'''
	def _mandelbrot_set(self, h_range, w_range, max_iterations):
		y, x = np.ogrid[1.4: -1.4: h_range*1j, -1.4: 1.4: w_range*1j]
		z_array = x + y*1j
		iterations_till_divergence = max_iterations + np.zeros(z_array.shape)
		
			
		for h in range(h_range):
				for w in range(w_range):
					z0 = z_array[h][w] 
					z = z0
					for i in range(max_iterations):
						z = z**2 + z0
						if z * np.conj(z) > 4:
							iterations_till_divergence[h][w] = i
							break

		return iterations_till_divergence
		
		
	''' 
	Function used to render an image of the specific julia set defined by the constant value given by the user
	
	For a more detailed explaination of what a Julia set is please see - https://youtu.be/dctJ7ISkU-4
	'''
	def plot (self):
		plt.imshow(self._julia_set(self._resolution, 
															self._resolution,
															self._max_itt), cmap=self._cmap)
		plt.axis('off')
		plt.show()
		plt.close()
	
	''' 
	Plot but for the Mandelbrot use case
	
	For explaination of what the Mandelbrot Set is see - https://youtu.be/NGMRB4O922I 
	'''
	def plot_mandelbrot (self):
		plt.imshow(self._mandelbrot_set(
			self._resolution, 
			self._resolution,
			self._max_itt),
			cmap='Purples')
			
		plt.axis('off')
		plt.show()
		plt.close()
		
	''' 
	User accessable function that allows them to set what resolution to set the generated photo 
	'''
	def set_resolution(self, resolution):
		self._resolution = resolution
	
	''' 
	Function enabled to let the user set the constant value of the constant that is used in the itterative definition of the set
	''' 
	def set_constant(self, c):
		self._c = c
		
	'''
	Function enabled to let the end use set the color map they like best 
	
	Options supportted by native matplotlib:
		afmhot, autumn, bone, binary, bwr, brg, CMRmap, cool, copper, cubehelix, flag, gnuplot, gnuplot2, gray, hot, hsv, jet, ocean, pink, prism, rainbow, seismic, spring, summer, terrain, winter, nipy_spectral, spectral, Accent, Blues, BrBG, BuGn, BuPu, Dark2, GnBu, Greens, Greys, Oranges, OrRd, Paired, Pastel1, Pastel2, PiYG, PRGn, PuBu, PuBuGn, PuOr, PuRd, Purples, RdBu, RdGy, RdPu, RdYlBu, RdYlGn, Reds, Set1, Set2, Set3, Spectral, YlGn, YlGnBu, YlOrBr, YlOrRd, gist_earth, gist_gray, gist_heat, gist_ncar, gist_rainbow, gist_stern, gist_yarg, coolwarm, Wistia, afmhot_r, autumn_r, bone_r, binary_r, bwr_r, brg_r, CMRmap_r, cool_r, copper_r, cubehelix_r, flag_r, gnuplot_r, gnuplot2_r, gray_r, hot_r, hsv_r, jet_r, ocean_r, pink_r, prism_r, rainbow_r, seismic_r, spring_r, summer_r, terrain_r, winter_r, nipy_spectral_r, spectral_r, Accent_r, Blues_r, BrBG_r, BuGn_r, BuPu_r, Dark2_r, GnBu_r, Greens_r, Greys_r, Oranges_r, OrRd_r, Paired_r, Pastel1_r, Pastel2_r, PiYG_r, PRGn_r, PuBu_r, PuBuGn_r, PuOr_r, PuRd_r, Purples_r, RdBu_r, RdGy_r, RdPu_r, RdYlBu_r, RdYlGn_r, Reds_r, Set1_r, Set2_r, Set3_r, Spectral_r, YlGn_r, YlGnBu_r, YlOrBr_r, YlOrRd_r, gist_earth_r, gist_gray_r, gist_heat_r, gist_ncar_r, gist_rainbow_r, gist_stern_r, gist_yarg_r, coolwarm_r, Wistia_r
	'''
	def set_color_map(self, cmap):
		self._cmap = cmap
		

	'''
	Define a unit circle, transcribe it in the complex plane, and find all of the julia set for all of the value 
	'''
	def plot_all_sets_on_the_unit_circle(self, resolution, cmap):
		circle = UnitCircle(resolution)
		
		unit_circle = circle.getValues()
		
		julia_sets = []
		for z_value in unit_circle:
			julia.set_constant(z_value)
			julia.set_color_map(cmap)
			julia.plot() 
		
	
if __name__ == '__main__':
	''' 
	Main Block of code that gets executed if you call it directly otherwise you can just import the class and not bring this code with ut 
	'''
	

	julia = Julia()
	
	''' 
	Collection of Julia Sets a list of points in the complex plane which create cool looking Julia set 
	''' 
	collection_of_julia_sets = []
	# collection_of_julia_sets.append(0 -.8*j)
	# collection_of_julia_sets.append(-0.1 + 0.651*j)
	# collection_of_julia_sets.append(-0.835 - 0.2321*j)
	# collection_of_julia_sets.append(.32-.11*j)
	# collection_of_julia_sets.append(.32-.25*j)
	# collection_of_julia_sets.append(.32 + .32*j)
	# collection_of_julia_sets.append(0 + .99*j)
	
	'''
	Find all the sets for all of the points on the unit circle
	'''
	julia.plot_all_sets_on_the_unit_circle(100, 'Blues_r')
	
	''' 
	Plot the entire collection of Julia Sets  
	'''
	for z_value in collection_of_julia_sets:
		julia.set_constant(z_value)
		julia.set_color_map('Blues_r')
		julia.plot() 
	
	'''
	Then plot the Mandelbrot Set
	'''
	# julia.plot_mandelbrot()
