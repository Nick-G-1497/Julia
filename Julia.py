## 
#  @package Julia
#  A library for building clocks based on the Julia Sets
#  @todo Get 4K images rendering
#  @todo Get a way to combine the pngs into a gif for README.md page
#  @todo dynamic color grading 
#  @todo impolement multiplrocessing so it builds multiple unit circle collections 
#  at the same time (can either uses mutexes have each rotation be its own independant
#  resource)
#  @todo write some unit test making sure whatever implementation that gets 
#  @todo collaborate with someone who has a strong background in algorithms to make it run faster
#  @todo eliminate the white borders surrounding the plot so it looks better as a background


from matplotlib.image import BboxImage
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import iterable
from UnitCircle import *
from math import *
from PIL import Image
from numpy import complex, array
import colorsys
# from multiprocessing import Poll

##
# Lambda function used to get the phase of a point in the complex plane
# @param z_value point in the complex plane with a real and imaginary attribute
phase = lambda z_value : atan(z_value.imag/ z_value.real) 
		
##
# Julia is a tool built for generatinpythg various julia sets. A julia set is defined by a function repeated or itterated numerous time. If due to the starting point the funtion diverges over itteration then the point is said not to be in the set. If remains inside an arbitrary finite space we define then it is said to be in the set.
#
# @note A Julia set is defined for a point in the complex plane by itterating over the following equation. If the Z value blow up beyond a certain
# magnitude then we exclude it from the set. However, if it stays arbitrarily finite then we in clude it in the set 
# @note https://www.desmos.com/calculator/n1698xdz63
# ``` 
# Znext = Zprev * Zprev + constant 
# ```
#  - where c is a constant we define in the complex plane or in any arbitrary 2D vector space if you are thinking about it graphically
class Julia ():
		
	_resolution_x = 3840
	_resolution_y = 2160
	_max_itt = 70
	_c = complex(-0.6, 0.4)
	_cmap = 'Purples'

	


	## 
	# Function enabled to test whether the constant value defined is within this specific julia set that pertains to the constant value we defined for the set. 
	def _julia_set(self, h_range, w_range, max_iterations):
		y, x = np.ogrid[1.4: -1.4: h_range*1j, -2.8: 2.8: w_range*1j]
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
		
	##  
	# The Mandelbrot Set is a special case Julia set the contant value you itterate with is the value you start with. The Mandelbrot set is said to be a map of all Julia sets
	#  - ``` z_next = z_prev * z_prev + z_initial ````
	# @note Benoit Mandelbrot recently passed away however here is a Ted Talks from 2010 
	# @param h_range number of pixels in the height
	# @param w_range number of pixels in the width
	# @param max_iterations is the maximum number of iterations to try to see if the point diverges before giving up and moving on
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
		
	

	##
	# Apply some sort of mapping from the number of itterations the point in the complex
	# plane does before diverging to an RGB value that the pixel will take on
	# @param itterations_til_divergence array of measurement of how many iterations each 
	# point lasted untill it diverged
	# @todo fix spelling mistake
	def color_map_PIL (self, itterations_til_divergence):
    		return itterations_til_divergence % 255




	##
	# Function used to render an image of the specific julia set defined by the constant value given by the user
	# using to PIL library
	#
	# @note For a more detailed explaination of what a Julia set is please see - https://youtu.be/dctJ7ISkU-4
	# @param dir directory the file should be saved in
	# @param phase current phase in radians of where the constant value is regards to the unitcircle
	def plot_with_PIL (self, dir = './', phase = ''):

		bitmap = Image.new("RGB", (self._resolution_x, self._resolution_y))
		pixels = bitmap.load()

		dir = dir + '_'


		itterations_till_divergence = self._julia_set(self._resolution_y, 
															self._resolution_x,
															self._max_itt)

		color_mapped_array = self.color_map(itterations_till_divergence)


		x_pixels = self._resolution_x - 10
		y_pixels = self._resolution_y - 10
		for x in range( x_pixels ):
    			for y in range( y_pixels ):
    					pixels[x, y] = int(color_mapped_array[x, y])
		
		bitmap.show()
	
	##
	# Function used to render an image of the specific julia set defined by the constant value given by the user
	# using to matplotlib library
	#
	# @note For a more detailed explaination of what a Julia set is please see - https://youtu.be/dctJ7ISkU-4
	# @param dir directory the file should be saved in
	# @param phase current phase in radians of where the constant value is regards to the unitcircle
	def plot_julia_set_with_matplotlib(self, cmap, step_number, path):
		fig = plt.figure()
		plt.imshow(self._julia_set(
			self._resolution_y,
			self._resolution_x, 
			255
		), cmap = cmap)
		plt.axis('off')
		plt.tight_layout()
		plt.savefig(path + str(step_number) +'.jpg', 
			bbox_inches = 'tight',
			)
		# plt.show()
		plt.close()
		
 

	##
	# Plot but for the Mandelbrot use case
	#
	# @note For explaination of what the Mandelbrot Set is see - https://youtu.be/NGMRB4O922I 
	# @note Benoit Mandelbrot is a recent enough mathematician for you to find his Ted Talk on youtube: https://www.youtube.com/watch?v=ay8OMOsf6AQ
	def plot_mandelbrot (self):
		fig = plt.figure()

		plt.imshow(self._mandelbrot_set(
			self._resolution, 
			self._resolution,
			self._max_itt),
			cmap='Purples')

		axes = fig.add_subplot(1,1,1)	

		plt.tight_layout()
		plt.show()
		plt.close()
		
	##
	# User accessable function that allows them to set what resolution to set the generated photo 
	def set_resolution(self, resolution):
		self._resolution = resolution
	
	## 
	# Function enabled to let the user set the constant value of the constant that is used in the itterative definition of the set
	def set_constant(self, c):
		self._c = c
		
	##
	# Function enabled to let the end use set the color map they like best 
	#
	# @param cmap string refering to which color map we should use
	# supported by the matplotlib library
	# @details Options supportted by native matplotlib:
	# 	afmhot, autumn, bone, binary, bwr, brg, CMRmap, 
	#   cool, copper, cubehelix, flag, gnuplot, gnuplot2, 
	#   gray, hot, hsv, jet, ocean, pink, prism, rainbow, 
	#   seismic, spring, summer, terrain, winter, 
	#   nipy_spectral, spectral, Accent, Blues, BrBG, 
	#   BuGn, BuPu, Dark2, GnBu, Greens, Greys, Oranges, 
	#   OrRd, Paired, Pastel1, Pastel2, PiYG, PRGn, PuBu, 
	#   PuBuGn, PuOr, PuRd, Purples, RdBu, RdGy, RdPu,  
	#   RdYlBu, RdYlGn, Reds, Set1, Set2, Set3, Spectral, 
	#   YlGn, YlGnBu, YlOrBr, YlOrRd, gist_earth, gist_gray, 
	#  gist_heat, gist_ncar, gist_rainbow, gist_stern, 
	#  gist_yarg, coolwarm, Wistia, afmhot_r, autumn_r, bone_r, 
	#  binary_r, bwr_r, brg_r, CMRmap_r, cool_r, copper_r, 
	#  cubehelix_r, flag_r, gnuplot_r, gnuplot2_r, gray_r, 
	#  hot_r, hsv_r, jet_r, ocean_r, pink_r, prism_r, 
	#  rainbow_r, seismic_r, spring_r, summer_r, terrain_r, 
	#  winter_r, nipy_spectral_r, spectral_r, Accent_r, 
	#  Blues_r, BrBG_r, BuGn_r, BuPu_r, Dark2_r, GnBu_r, 
	#  Greens_r, Greys_r, Oranges_r, OrRd_r, Paired_r, 
	#  Pastel1_r, Pastel2_r, PiYG_r, PRGn_r, PuBu_r, 
	#  PuBuGn_r, PuOr_r, PuRd_r, Purples_r, RdBu_r, RdGy_r, 
	#  RdPu_r, RdYlBu_r, RdYlGn_r, Reds_r, Set1_r, Set2_r, 
	#  Set3_r, Spectral_r, YlGn_r, YlGnBu_r, YlOrBr_r, YlOrRd_r, 
	#  gist_earth_r, gist_gray_r, gist_heat_r, gist_ncar_r, 
	#  gist_rainbow_r, gist_stern_r, gist_yarg_r, coolwarm_r, 
	#  Wistia_r
	def set_color_map(self, cmap):
		self._cmap = cmap
		

	##
	# Define a unit circle, transcribe it in the complex plane, and find all of the julia set for all of the value 
	# @params resolution number of steps in time/phase to take along the unit circle
	# @params cmap color map to plot the rotation as
	def plot_all_sets_on_the_unit_circle(self, resolution_in_time, cmap, path):
		circle = UnitCircle(resolution_in_time)
		
		unit_circle = circle.getValues()
		
		step = 60
		for z_value in unit_circle:
			julia.set_constant(z_value)
			julia.set_color_map(cmap)
			julia.plot_julia_set_with_matplotlib(cmap, step, path)
			step -= 1
		

##
#Main Block of code that gets executed if you call it directly otherwise you can just import the class and not bring this code with ut 		
if __name__ == '__main__':

	
	##
	# Create an instance of the Julia object
	julia = Julia()
	
	##
	#Collection of Julia Sets a list of points in the complex plane which create cool looking Julia set 
	 
	collection_of_julia_sets = []
	# collection_of_julia_sets.append(0 -.8*j)
	# collection_of_julia_sets.append(-0.1 + 0.651*j)
	# collection_of_julia_sets.append(-0.835 - 0.2321*j)
	# collection_of_julia_sets.append(.32-.11*j)
	# collection_of_julia_sets.append(.32-.25*j)
	# collection_of_julia_sets.append(.32 + .32*j)
	# collection_of_julia_sets.append(0 + .99*j)
	
	
	steps = 60
	cmap = 'Blues_r'
	path_and_file_naming_convention = 'Blues_r' + '_Julia_Set/Blue_'
	##
	#Find all the sets for all of the points on the unit circle
	julia.plot_all_sets_on_the_unit_circle(steps, cmap, path_and_file_naming_convention)

	''' 
		Then plot the Mandelbrot Set
	'''
	# julia.plot_mandelbrot()
