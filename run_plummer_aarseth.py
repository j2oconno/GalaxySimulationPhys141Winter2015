import os
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PlummerGalaxy import PlummerGalaxy

# Settings:

createNewInitialConditions = True

MakePositionsVideo = True
MakeDistributionsVideo = False


#=================================================================================
if createNewInitialConditions:
	
	# Generate Plummer galaxy
	newGalaxy = PlummerGalaxy()
	newGalaxy.npts = 1000
	newGalaxy.R = 1.0
	newGalaxy.timestep = 0.1
	newGalaxy.timemax = 2.0
	newGalaxy.ZeroVelocities_Bool = True
	
	newGalaxy.GenerateInitialConditions(0,0,0)
	newGalaxy.WriteToFile("plummer.data")
	
	print("compiling Aarseth c code...")
	os.system("gcc -o Aarseth/aarseth Aarseth/nbody0-lab.c -lm")
	
	print("Running compiled Aarseth nbody code on Plummer initial conditions file")
	os.system("./Aarseth/aarseth plummer.data")


if MakePositionsVideo or MakeDistributionsVideo:
	#=================================================================================
	# Plot the results using matplotlib
	
	fin = open("out_aarseth_npts_1000.data", "r")
	npts = 1000
	
	
	ptsx = np.zeros(npts)
	ptsy = np.zeros(npts)
	ptsz = np.zeros(npts)
	
	partnum = 0
	timestepint = 0
	for line in fin:   # iterate over each line
	
		ptsx[partnum], ptsy[partnum], ptsz[partnum] = line.split()   # split line by whitespace
	
		#print("pt_"+str(partnum)+" == ("+str(ptsx[partnum])+", "+str(ptsy[partnum])+", "+str(ptsz[partnum])+")")
	
		if partnum >= (npts-1):
			if MakePositionsVideo:
				fig = plt.figure()
				ax = fig.add_subplot(1,1,1)
				
				ax.scatter(ptsx, ptsy, ptsz)
				
				ax.set_xlim(-5, 5)
				ax.set_ylim(-5, 5)
				ax.set_aspect(1)
				ax.set_xlabel('x (kpc)')
				ax.set_ylabel('y (kpc)')
				ax.set_title("time: "+str(timestepint))
				
				fname = "frames/_tmp%03d.png"%timestepint
				plt.savefig(fname)
				plt.clf()
				plt.close()
			
			elif MakeDistributionsVideo:
				radiiForPlotting = np.sqrt(np.power(ptsx,2.0) + np.power(ptsy,2.0) + np.power(ptsz,2.0))
				radiiForPlotting[radiiForPlotting > 9.9] = 9.9
				truthx = np.linspace(0,10,npts)
				
				fig = plt.figure()
				ax = fig.add_subplot(1,1,1)
				ax.plot(truthx, 3.0*np.power(truthx,2.0)*np.power(1.0+np.power(truthx,2.0),-5.0/2.0))
				ax.hist(radiiForPlotting, 100, normed=1, alpha=0.75, facecolor='green')
				ax.set_xlim(0, 10)
				ax.set_ylim(0, 1)
				ax.set_xlabel('r (kpc)')
				ax.set_ylabel('radial mass density: p(r) * 4 pi r^2   units: 10^11 Msol/kpc')
				ax.set_title("time: "+str(timestepint))
				fname = "frames/_tmp%03d.png"%timestepint
				plt.savefig(fname)
				plt.clf()
				plt.close()
		
			partnum = -1
			timestepint = (timestepint + 1)
		
		partnum = (partnum + 1)
	
	fin.close()
	
	print('Making movie video.avi - this make take a while')
	os.system("ffmpeg -r 15 -f image2 -i 'frames/_tmp%03d.png' -qscale 0 'video.avi'")
	os.system("rm frames/*.png")





