# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 16:44:45 2017

@author: Agus Velazquez
"""
import pandas as pd
import numpy as np
import os 

os.chdir('D:\\Sistema\\Santiago\\Desktop\\Stage\\Demo\\DATA\\Tensile\\Strain and Stress Data')

#%% Parameters
time_selected = str(1) #pick the time at which is made the analysis 
archivos = archivos = np.arange(1,7,1)
        
        
#%% load 
strain={}
for i in archivos:
    strain[i] = pd.read_csv('strain_E'+str(i)+'.csv', index_col = 0)

stress={}
for i in archivos:
    stress[i] = pd.read_csv('stress_S'+str(i)+'.csv', index_col = 0)

#%% Strain at time_selected

strain_time = strain[1]['Gauss Point']
for i in archivos:
    time = strain[i][time_selected]
    strain_time = pd.concat([strain_time,time], axis = 1, ignore_index = True)
    
for i in range(1,7,1):
    strain_time = strain_time.rename(columns={i:'Strain_E'+str(i)})
    
strain_time = strain_time.rename(columns={0:'Gauss Point'})

#%% Stress at time_selected
 
stress_time = stress[1]['Gauss Point']
for i in archivos:
    time = stress[i][time_selected]
    stress_time = pd.concat([stress_time,time], axis = 1, ignore_index = True)
    
for i in range(1,7,1):
    stress_time = stress_time.rename(columns={i:'Stress_S'+str(i)})
    
stress_time = stress_time.rename(columns={0:'Gauss Point'})
#%% Concatenation
stress_time = stress_time.drop(['Gauss Point'], axis = 1)
all_components_at_time = pd.concat([strain_time,stress_time], axis = 1)

#%% Data Saving
filename = 'all_components_at_time_'+str(time_selected)+'.csv'
all_components_at_time.to_csv(filename)