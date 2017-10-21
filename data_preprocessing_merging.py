# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 18:18:59 2017

@author: Agustin Velazquez

"""
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

#%% 
archivos = np.arange(1,7,1)

strain={}
for i in archivos:
    strain[i] = pd.read_csv('strain_E'+str(i)+'.csv', index_col = 0)

stress={}
for i in archivos:
    stress[i] = pd.read_csv('stress_S'+str(i)+'.csv', index_col = 0)
        

#%% Boxplot graph
boxplot_index = np.arange(1,107,10)
boxplot_strain = strain[1]['Gauss Point'] #initialization of the matrix
for i in archivos:
    strain_col_name = 'Strain_E%d'%i
    concatenation = pd.concat([strain[i][strain_col_name]], axis = 1)
    boxplot_strain = pd.concat([boxplot_strain, concatenation], axis = 1)

boxplot_strain = boxplot_strain.iloc[:,1:-1]
fig = plt.figure()
bx1 = fig.add_subplot(111)
bx1 = sns.boxplot(data = boxplot_strain)
bx1.set_title('Strain dispersion')
bx1.set_ylabel('Strain')
bx1.set_xlabel('Times')

#%% Preprocessing
for i in archivos:
    #Stress dictionary
    stress[i] = stress[i].transpose()
    stress[i].columns = stress[i].iloc[0]
    stress[i] = stress[i].drop(['Gauss Point'], axis = 0)
    stress[i] = pd.melt(stress[i])
    stress[i] = stress[i].rename(columns = {'Gauss Point':'Gauss Point', 'value':'Stress_S'+str(i)})
    #Strain dictionary
    strain[i] = strain[i].transpose()
    strain[i].columns = strain[i].iloc[0]
    strain[i] = strain[i].drop(['Gauus Point'], axis = 0)
    strain[i] = pd.melt(strain[i])
    strain[i] = strain[i].rename(columns = {'Gauus Point':'Gauss Point', 'value':'Strain_E'+str(i)})

#%% Merging & Saving 
data_all_components = stress[1]['Gauss Point'] #initialization of the matrix
for i in archivos:
    stress_col_name = 'Stress_S%d'%i
    strain_col_name = 'Strain_E%d'%i
    concatenation = pd.concat([stress[i][stress_col_name],strain[i][strain_col_name]], axis=1)
    data_all_components = pd.concat([data_all_components,concatenation], axis=1)
data_all_components.to_csv('data_all_components.csv')

