# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:47:35 2017

@author: Agustin Velazquez
"""

import numpy  as np
import pandas as pd
import os 

os.getcwd()

#data = np.genfromtxt('new_Stress_data.txt', dtype = 'str')
data = pd.read_csv('new_Stress_data.tsv', sep='\t', header=None, index_col = False)

#Parameters
n_times  = 100  #numero de "tiempos" que se midio el experimentos
n_points = 2029 #numero de puntos en la proveta
set      = 7    #el numero de elementos + 1(por el tiempo)
archivos = np.arange(1,7,1) #S11,S22,S33,S12,S13,S23
limite   = n_points*set
data_split = np.array_split(data,n_times)

#%% Stress loop
for j in archivos:
    #First columns
    bricks_indexes = np.arange(1,limite,set)
    stress = data_split[0].iloc[bricks_indexes]
    stress = stress.reset_index(drop = True)
    stress = stress.rename(columns = {0:'Point'})
    stress['Point'] = stress['Point'].str.slice_replace(1,8) #string replacing according to the file
    stress['Point'] = stress['Point'].str.slice_replace(7,20,'') #strin replacing according to the file
    stress['Point'] = pd.to_numeric(stress['Point'])
    for i in range(0, n_times, 1):
        time = data_split[i]
        time = time.drop(time.index[0])
        time = time.reset_index(drop = True)
        S_indexes = np.arange(j,limite,set)
        S = time.iloc[S_indexes]
        S = S.reset_index(drop = True)
        S = S.rename(columns = {0:'Stress_S23'})
        S = pd.to_numeric(S['Stress_S23'])    
        stress = pd.concat([stress,S], axis = 1, ignore_index = True)    
    #Save data
    stress = stress.rename(columns = {0:'Gauss Point'})
    filename = 'stress_S%d.csv'%j
    stress.to_csv(filename)
