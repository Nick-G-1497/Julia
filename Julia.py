## 
#  @package Julia
#  A library for generating various collections of Julia Sets
#  @todo Get 4K images rendering and have it have a time resolution of every second (360 Julia sets per unit circle).
#  This will take a lot of computation however we know that it is in fact finite and will take fewer than 
#  183 trillion z squared plus c's, however, in practice it is much lower since most of the unit circle compromises
#  Fatou Dust and therefore diverges pretty quickly.
#  @todo dynamic color grading - Currently the image rendering is handled by matplotlib pyplot. It is apparent the 
#  color grading happens in discrete boundaries as such so much of the resolution of the julia sets are lost via 
#  the color grading as much of the unit circle compromises Fatou Dust. As such a better implementation would be 
#  to implement color grading manually so that the colors fade more gradually and the resolution is maximized. 24
#  different color gradings need to be created - one for each how of the day.
#  @todo imploment multi-threading so it builds multiple unit circle collections 
#  at the same time (can either uses mutexes have each rotation be its own independant
#  resource)
#  @todo figure out why unit test succeed locally but fail when run with github actions 
#  @todo collaborate with someone who has a strong background in algorithms to make it run faster
#  @todo eliminate the white borders surrounding the plot so it looks better as a background

from matplotlib.image import BboxImage
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import iterable
from EulersSpiral import EulersSpiral
from Spiral import Spiral
from UnitCircle import *
from math import *
from PIL import Image
from numpy import complex, array
import colorsys
import os
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
		
	_resolution_x = 1600
	_resolution_y = 900
	_max_itt = 64
	_c = complex(-0.6, 0.4)
	_cmap = 'Purples'

	def plot_all_sets_on_the_eulers_spiral(self, resolution_in_time, cmap, path):
		spiral_t = EulersSpiral(resolution_in_time )
		
		S, C = spiral_t.getValues()
		
		step = resolution_in_time 
		for i in range(resolution_in_time):
			julia.set_constant(complex(S[i], C[i]))
			julia.set_color_map(cmap)
			julia.plot_julia_set_with_matplotlib(cmap, step, path)
			step -= 1
	


	def plot_all_sets_on_spiral(self, resolution_in_time, cmap, path):
		spiral_t = Spiral()
		
		spiral = spiral_t.getValues(resolution_in_time)
		
		step = 0 
		for i in range(resolution_in_time):
			self.set_constant(complex(spiral[i].real, spiral[i].imag))
			self.set_color_map(cmap)
			self.plot_julia_set_with_matplotlib(cmap, step, path)
			step += 1

	


	## 
	# Function enabled to test whether the constant value defined is within this specific julia set that pertains to the constant value we defined for the set. 
	# @param h_range - height range, number of pixels in the vertical axis
	# @param w_range - width range, number of pixels in the horizontal axis
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
		plt.savefig(path + cmap + str(step_number) +'.jpg', 
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
	# @param resolution number of steps in time/phase to take along the unit circle
	# @param cmap color map to plot the rotation as
	def plot_all_sets_on_the_unit_circle(self, resolution_in_time, cmap, path):
		circle = UnitCircle(resolution_in_time )
		
		unit_circle = circle.getValues()
		
		step = 59 
		for z_value in unit_circle:
		    self.set_constant(z_value)
		    self.set_color_map(cmap)
		    self.plot_julia_set_with_matplotlib(cmap, step, path)
		    step -= 1

	##
	# Define a subset 2 -> -2 of the real number space \mathbb{R}. Then find all of the julia sets for all of the values
	# @param resolution_in_time - parameter setting how many increments to take on the path
	# @param cmap - matplot lib color mapping to apply
	# @param path - path and naming convention to store the files
	def plot_some_sets_on_real_number_space(self, resolution_in_time, cmap, path): 
		real_line = [-i/resolution_in_time for i in range(-2 * resolution_in_time, 2 * resolution_in_time, 1)]
		index = 4 * resolution_in_time
		# print(real_line)
		for z_value in real_line:
			self.set_constant(z_value)
			print(z_value)
			self.set_color_map(cmap)
			self.plot_julia_set_with_matplotlib(cmap, index, path)
			index -= 1


	##
	# Define a line in the complex plane ranging from 2 to -2. Then find every corresponding julia set on that line.
	# @param resolution_in_time - degree of resolution that the line should have. number of steps is equal to resolution_in_time
	# times four
	# @param cmap - color map
	# @param path - file path and naming convention to store the files. 
	def plot_some_sets_on_imaginary_number_space (self, resolution_in_time, cmap, path):
		imaginary_line = [complex(0,-i)/resolution_in_time for i in range(-2 * resolution_in_time, 2 * resolution_in_time, 1)]
		index = 4*resolution_in_time
		
		for z_value in imaginary_line:
			self.set_constant(z_value)
			print(z_value)
			self.set_color_map(cmap)
			self.plot_julia_set_with_matplotlib(cmap, index, path)
			index -= 1

	
                    

##
#Main Block of code that gets executed if you call it directly otherwise you can just import the class and not bring this code with ut 		
if __name__ == '__main__':

	
	##
	# Create an instance of the Julia object
	julia = Julia()	
	
	resolution_in_time = 500
	cmap = 'gist_earth'
	type_of_path = 'real_number_line'

	# cmap = 'cubehelix'
	# type_of_path = 'imaginary_line'


	path_and_file_naming_convention = type_of_path + '_' + cmap + '_Julia_Set/' + cmap + '_'
	# os.system('mkdir ' + type_of_path + '_' + cmap + '_Julia_Set/')
	##
	#Find all the sets for all of the points on the unit circle
	# julia.plot_some_sets_on_imaginary_number_space(resolution_in_time, cmap, path_and_file_naming_convention)
	# input()
	julia.plot_some_sets_on_real_number_space(resolution_in_time, cmap, path_and_file_naming_convention)



	
