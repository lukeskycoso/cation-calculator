#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Introduction
print('Welcome to cation calculator for anhydrous phases, this is a free to use software for calculating cations from EMP raw data')
print('This software supports the calculation for the following oxides:')
print('SiO2, TiO2, ZrO2, Al2O3, V2O3, Cr2O3, FeO, MnO, NiO, MgO, CaO, SrO, BaO, ZnO, Na2O, K2O, Rb2O, Cs2O, Fe2O3, V2O5, SO3, P2O5')
print('-----------------------------------------------------------')
print('If you already did a run, copy the results from "output.xlsx" to another spreadsheet, or they will be overwritten and lost!')
print('-----------------------------------------------------------')

print('--------------------CATION CALCULATOR----------------------')
print('How many cations are in the ideal formula?')
input_cations = int(input())
print('How many oxygens are in the ideal formula?')
input_oxygens = int(input())
print('I will calculate the formula for', input_cations, 'cations and', input_oxygens, 'oxygens')


# In[3]:


# Things to import
import pandas as pd
import numpy as np


# In[5]:


# Loading the dataset

print('Please, now paste the path of the spreadsheet you want to process INCLUDING the spreadsheet name.extension')
print('Example: C:/User/Desktop/example_spreadsheet.xlsx')
# Example for myself, REMEMBER TO DELETE ##################################################
# C:\Users\lucar\OneDrive\coding\python\cation_calculator\data\test.xlsx
df = pd.read_excel(input('Paste the path and the name, as in the example:'))
print('Loading the spreadsheet...')
#print(df)


# In[6]:


# Identification of the oxides
# Elements constants dictionary of all the most common oxide molecules in geology
# Format: 'oxide_fomula':[molecular_mass(0), cation_count(1), oxygen_count(2),_cation_name(3)]
element_constants={
'SiO2':[60.08431,1.0,2,'Si'], #leave always FIRST!
'TiO2':[79.865,1.0,2,'Ti'],
'ZrO2':[123.2228,1.0,2,'Zr'],
'Al2O3':[101.960076,2.0,3,'Al'],
'V2O3':[149.881,2.0,3,'V3+'],
'Cr2O3':[151.989,2.0,3,'Cr'],
'Fe2O3':[159.687,2.0,3,'Fe3+'],
'FeO':[71.844,1.0,1,'Fe2+'],
'MnO':[70.937,1.0,1,'Mn'],
'NiO':[74.692,1.0,1,'Ni'],
'MgO':[40.304,1.0,1,'Mg'],
'CaO':[56.077,1.0,1,'Ca'],
'SrO':[103.6194,1.0,1,'Sr'],
'BaO':[153.3264,1.0,1,'Ba'],
'ZnO':[81.379,1.0,1,'Zn'],
'Na2O':[61.9786,2.0,1,'Na'],
'K2O':[94.195,2.0,1,'K'],
'Rb2O':[186.935,2.0,1,'Rb'],
'Cs2O':[281.8103,2.0,1,'Cs'],
'V2O5':[181.88,2.0,5,'V5+'],
'SO3':[80.06302,1.0,3,'S'],
'P2O5':[141.9445,2.0,5,'P'] # Leave always LAST!
}

df_element_constants = pd.DataFrame.from_dict(element_constants)
#print(df_element_constants)
#print('Atomic mass of commonly measured oxides:')
#print(df_mass)


# In[7]:


# Selecting the oxides
df_oxides = df.select_dtypes(include=['float64']) # Only float numbers are filtered, it is suggested to avoid using numbers as 1.1 for analysis. Please use 1-1 or another method of classification.

collected_oxides = list(df_oxides.columns.values) # Selects the headers and creates a new dataframe for the calculation of the molar mass of each element.
oxides_list_length = len(collected_oxides)
df_oxides = df_oxides.replace(np.nan,0.00)
#print(df_oxides)
print('A total of', oxides_list_length, 'different oxides have been found.')
print('They are the following:', collected_oxides)
print('IF SOME ARE MISSING, CHECK THE SPREADSHEET!')


# In[8]:


# Reordering oxides according to the list provided 
df_calc = df_oxides.reindex(df_element_constants.columns, fill_value=0.00, axis=1)
#df_calc=pd.DataFrame(df_calc_obj[:])
#print(df_calc)
#print(df_calc)


# In[9]:


# Calculate total percentage.
print('Calculating, it will take a few seconds...')
df_totals = df_calc.copy()
df_totals['Total wt%']= df_calc.sum(axis=1)
#print(df_totals)


# In[10]:


# Calculating molecular proportions
# molecular_proportion = cation_count(1) * df_calc / molecular_mass(0)
# Defining the variables
molecular_mass = df_element_constants.loc[0]
molecular_mass.to_frame()
#print(molecular_mass)
cation_count = df_element_constants.loc[1]
cation_count.to_frame()
oxygen_count = df_element_constants.loc[2]
oxygen_count.to_frame()
element_label = df_element_constants.loc[3]
element_label.to_frame()
# Calculation of the cation ratio
#cation_mol_ratio = np.divide(df_calc, molecular_mass)
#print(cation_mol_ratio)

# Calculation of the molecular proportion
df_molecular_proportion = pd.DataFrame()
df_molecular_proportion =  np.divide(df_calc, molecular_mass)

#print(df_molecular_proportion)


# In[11]:


# Calculating oxygen atomic proportions
# df_molecular_proportion * oxygen_count

df_oxygen_proportion = pd.DataFrame()
df_oxygen_proportion = np.multiply(df_molecular_proportion, oxygen_count)
#print(df_oxygen_proportion)

df_oxygen_proportion['sum_oxy'] = df_oxygen_proportion.sum(axis=1) #there is a problem in sum_oxy calculation
#df_oxygen_proportion.to_excel('oxygens_proportions.xlsx')

#print(df_oxygen_proportion)


# In[12]:


# Calculating oxygen moles
# molecular_proportions * cation_count
df_oxygen_mol = pd.DataFrame()
df_oxygen_mol = np.multiply(df_molecular_proportion, cation_count)

#print(df_oxygen_mol)


# In[13]:


# Calculation of cations
#  (df_oxygen_mol * input_oxygens)/'sum_oxy'
cation_1 = pd.DataFrame()
cation_1 = np.multiply(df_oxygen_mol, input_oxygens)

#print(cation_1)
#sum_oxygen_proportion = df_oxygen_proportion['sum_oxy']
#sum_oxygen_proportion.to_numpy()
#print(sum_oxygen_proportion)


# In[14]:


# Calculation the final cations
#cation_final = np.divide(cation_1,sum_oxygen_proportion)
#cation_final = cation_1.iloc[:, 0:-1].divide(cation_1.iloc[:,-1], axis = 'rows')
cation_final = pd.DataFrame()

cation_final['Si'] = cation_1['SiO2']/df_oxygen_proportion['sum_oxy']
cation_final['Ti'] = cation_1['TiO2']/df_oxygen_proportion['sum_oxy']
cation_final['Zr'] = cation_1['ZrO2']/df_oxygen_proportion['sum_oxy']
cation_final['Al'] = cation_1['Al2O3']/df_oxygen_proportion['sum_oxy']
cation_final['V3+'] = cation_1['V2O3']/df_oxygen_proportion['sum_oxy']
cation_final['Cr'] = cation_1['Cr2O3']/df_oxygen_proportion['sum_oxy']
cation_final['Fe3+'] = cation_1['Fe2O3']/df_oxygen_proportion['sum_oxy']
cation_final['Fe2+'] = cation_1['FeO']/df_oxygen_proportion['sum_oxy']
cation_final['Mn'] = cation_1['MnO']/df_oxygen_proportion['sum_oxy']
cation_final['Ni'] = cation_1['NiO']/df_oxygen_proportion['sum_oxy']
cation_final['Mg'] = cation_1['MgO']/df_oxygen_proportion['sum_oxy']
cation_final['Ca'] = cation_1['CaO']/df_oxygen_proportion['sum_oxy']
cation_final['Sr'] = cation_1['SrO']/df_oxygen_proportion['sum_oxy']
cation_final['Ba'] = cation_1['BaO']/df_oxygen_proportion['sum_oxy']
cation_final['Zn'] = cation_1['ZnO']/df_oxygen_proportion['sum_oxy']
cation_final['Na'] = cation_1['Na2O']/df_oxygen_proportion['sum_oxy']
cation_final['K'] = cation_1['K2O']/df_oxygen_proportion['sum_oxy']
cation_final['Rb'] = cation_1['Rb2O']/df_oxygen_proportion['sum_oxy']
cation_final['Cs'] = cation_1['Cs2O']/df_oxygen_proportion['sum_oxy']
cation_final['V5+'] = cation_1['V2O5']/df_oxygen_proportion['sum_oxy']
cation_final['S'] = cation_1['SO3']/df_oxygen_proportion['sum_oxy']
cation_final['P'] = cation_1['P2O5']/df_oxygen_proportion['sum_oxy']

#print(cation_final)


# In[15]:


# Sum of cations
cation_final['Total cations, ideal =', input_cations] = cation_final.sum(axis=1)
#print(cation_final)


# In[16]:


# Creating output organised dataframe
# Selecting non float columns of df
df_labels = df.select_dtypes(exclude=['float64'])
# print(df_labels)
# Adding df_calc and adding cation_final
df_concat = pd.concat([df_labels,df_calc, cation_final], axis=1)
print('-----------------------------Starting calculation-----------------------------')
print(df_concat)
print('-----------------------------Calculation finished-----------------------------')


# In[17]:


# Saving df_concat to xlsx
print('----------------------------------------------------------------')
print('Calculation completed.')
print('The file "output.xlsx" containing your data, ')
import os
cwd = os.getcwd()
path = cwd + "/output.csv"
df_concat.to_csv(path)
print('Thank you for using this program. For any issue do not hesitate to contact me at reato1@uniba.sk')


# In[ ]:




