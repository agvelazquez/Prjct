# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:47:35 2017

@author: Agustin Velazquez
"""

import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import os 
#%% Parameters 

data = pd.read_csv('new_Coord_data.tsv', sep='\t', header=None, index_col = False)
n_times  = 107  #numero de "tiempos" que se midio el experimentos
n_points = 2080 #numero de puntos en la proveta
set      = 4    #el numero de elementos + 1(por el tiempo)
archivos = np.arange(1,4,1) #numeracion de archivos a armar 
limite   = n_points*set
data_split = np.array_split(data,n_times)

#%% Strain loop 

for j in archivos:
    #First columns
    bricks_indexes = np.arange(1,limite,set)
    strain = data_split[0].iloc[bricks_indexes]
    strain = strain.reset_index(drop = True)
    strain = strain.rename(columns = {0:'Point'})
    strain['Point'] = strain['Point'].str.slice_replace(1,8)  #string replacement according to the original file
    strain['Point'] = strain['Point'].str.slice_replace(7,20,'')  #string replacement according to the original file
    strain['Point'] = pd.to_numeric(strain['Point'])
    #End of First Columns
    for i in range(0, n_times, 1):
        time = data_split[i]
        time = time.drop(time.index[0])
        time = time.reset_index(drop = True)
        coord_indexes = np.arange(j,limite,set) 
        coord = time.iloc[coord_indexes]
        coord = coord.reset_index(drop = True)
        coord = coord.rename(columns = {0:'Strain_X3'})
        coord = pd.to_numeric(X3['Strain_X3'])    
        strain = pd.concat([strain,coord], axis = 1, ignore_index = True)
    #Save data (change the name of the file)
    strain = strain.rename(columns = {0:'Gauss Point'})
    filename = 'coord_X%d_new.csv'%j
    strain.to_csv(filename)

#%% Plot coordinate and Gauss Point

#==============================================================================
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title('Gauss Point and its  X coordinate at initial time')
# ax1.set_ylabel('Gauss Point')
# ax1.set_xlabel('X coordinate')
# spec1 = ax1.scatter(strain[1], strain['Gauss Point'], c='b', s = 10)
#==============================================================================

#%% Plotting 3D scatter position at initial time 

#==============================================================================
# X1 = pd.read_csv('coord_X1.csv', index_col = 0)
# X1 = np.array(X1)
# X2 = pd.read_csv('coord_X2.csv', index_col = 0)
# X2 = np.array(X2)
# X3 = pd.read_csv('coord_X3.csv', index_col = 0)
# X3 = np.array(X3)
# 
# fig = plt.figure()
# ax1 = fig.add_subplot(111, projection='3d')
# ax1.scatter(X1[:,1],X2[:,1],X3[:,1])
# ax1.set_xlabel('X Label')
# ax1.set_ylabel('Y Label')
# ax1.set_zlabel('Z Label')
#==============================================================================
