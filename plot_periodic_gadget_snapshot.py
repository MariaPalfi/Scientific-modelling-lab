#!/usr/bin/python3

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
#import scipy as sp
import sphviewer as sph
import sys
import time
from pygadgetreader import *

#---------------------------------------------------------------------------------------------------#
# plot_periodic_gadget_snapshot.py -    A simple python script for plotting GADGET snapshots        #
#                                       with sphviewer                                              #
#   Copyright (C) 2020 Gabor Racz                                                                   #
#                                                                                                   #
#    This program is free software; you can redistribute it and/or modify                           #
#    it under the terms of the GNU General Public License as published by                           #
#    the Free Software Foundation; either version 2 of the License, or                              #
#    (at your option) any later version.                                                            #
#                                                                                                   #
#    This program is distributed in the hope that it will be useful,                                #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of                                 #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                  #
#    GNU General Public License for more details.                                                   #
#---------------------------------------------------------------------------------------------------#

cmap='inferno' #colormap

#Beginning of the script
if (len(sys.argv) != 6) and (len(sys.argv) != 7):
    print("Error:")
    print("usage: ./plot_periodic_gadget_snapshot.py <input GADGET snapshot file> <x or y or z> <height of the slice in Mpc/h> <resolution> <'scatter' or 'sph'> <output file (optional)>\nExiting.")
    sys.exit(2)

#Parameters of the plot
INFILE = sys.argv[1]
SLICE = str(sys.argv[2])
HEIGHT = np.double(sys.argv[3])
RES = np.int(sys.argv[4])
MODE = str(sys.argv[5])
if len(sys.argv) == 7:
    OUTFILE = str(sys.argv[6])

if (SLICE != 'x') and (SLICE != 'y') and (SLICE != 'z'):
    print("Error:")
    print("Unknown axis: %s" % SLICE)
    sys.exit(2)

#reading the header of the snapshot
print(readheader(INFILE, 'header'))
#reading the input data
Coordinates = readsnap(INFILE, 'pos', 'dm')/1000 #in Mpc
Masses =  readsnap(INFILE, 'mass', 'dm')
L_box = np.double(readheader(INFILE, 'boxsize'))/1000 #in Mpc
#computing the slice
if SLICE == 'x':
    indexes = np.logical_and((Coordinates[:,0]<(HEIGHT+L_box/30)), ((Coordinates[:,0]>(HEIGHT-L_box/30))))
elif SLICE == 'y':
    indexes = np.logical_and((Coordinates[:,1]<(HEIGHT+L_box/30)), ((Coordinates[:,1]>(HEIGHT-L_box/30))))
elif SLICE == 'z':
    indexes = np.logical_and((Coordinates[:,2]<(HEIGHT+L_box/30)), ((Coordinates[:,2]>(HEIGHT-L_box/30))))

if MODE=='scatter':
    plt.figure(figsize=[5,5])
    plt.xlim([0,L_box])
    plt.ylim([0,L_box])
    if SLICE == 'x':
        plt.scatter(Coordinates[indexes][:,1],Coordinates[indexes][:,2],s=1,c='black')
        plt.xlabel('y[Mpc/h]')
        plt.ylabel('z[Mpc/h]')
    if SLICE == 'y':
        plt.scatter(Coordinates[indexes][:,0],Coordinates[indexes][:,2],s=1,c='black')
        plt.xlabel('x[Mpc/h]')
        plt.ylabel('z[Mpc/h]')
    if SLICE == 'z':
        plt.scatter(Coordinates[indexes][:,0],Coordinates[indexes][:,1],s=1,c='black')
        plt.xlabel('x[Mpc/h]')
        plt.ylabel('y[Mpc/h]')
    if len(sys.argv) == 7:
        plt.savefig(OUTFILE)
    else:
        plt.show()

if MODE=='sph':
    extent=[0,L_box,0,L_box]
    Particles = sph.Particles(Coordinates[indexes,:].T+L_box/2, Masses[indexes].T)
    Scene = sph.Scene(Particles)
    if SLICE == 'x':
        Scene.update_camera(x=L_box/2,y=L_box/2,z=L_box/2,r='infinity',xsize=RES,ysize=RES,extent=extent,t=90,p=90)
    if SLICE == 'y':
        Scene.update_camera(x=L_box/2,y=L_box/2,z=L_box/2,r='infinity',xsize=RES,ysize=RES,extent=extent,t=90,p=0)
    if SLICE == 'z':
        Scene.update_camera(x=L_box/2,y=L_box/2,z=L_box/2,r='infinity',xsize=RES,ysize=RES,extent=extent,t=0,p=0)
    Render = sph.Render(Scene)
    Render.set_logscale()
    img = Render.get_image()
    fig = plt.figure(1,figsize=(6,6))
    ax1 = fig.add_subplot(111)
    ax1.imshow(img, extent=extent, origin='lower', cmap=cmap)
    if SLICE == 'x':
        ax1.set_xlabel(r'$y$[Mpc$/h$]', size=10)
        ax1.set_ylabel(r'$z$[Mpc$/h$]', size=10)
    if SLICE == 'y':
        ax1.set_xlabel(r'$x$[Mpc$/h$]', size=10)
        ax1.set_ylabel(r'$z$[Mpc$/h$]', size=10)
    if SLICE == 'z':
        ax1.set_xlabel(r'$x$[Mpc$/h$]', size=10)
        ax1.set_ylabel(r'$y$[Mpc$/h$]', size=10)
    if len(sys.argv) == 7:
        plt.savefig(OUTFILE)
    else:
        plt.show()
