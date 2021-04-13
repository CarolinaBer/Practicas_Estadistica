#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import pandas as pd
import numpy as np


# In[2]:


det_s1b= pd.read_csv('Practica2_Estadistica/Neu_Det_S1B.csv',header=None, sep='\n')


# In[3]:


import csv
List = []
with open('Practica2_Estadistica/Neu_Det_S1B.csv','r') as f:
    reader = csv.reader(f,delimiter='\n')
    for i,line in enumerate(reader):
        List.append(line)
        #print ( 'line[{}]={}'.format(i,line))
#len(List)


# In[4]:


indices = []
for i in range(len(List)):
    if not List[i]:
        indices.append(i)
indices


# In[5]:


num1 = det_s1b[:50]
num2 = det_s1b[50:(60-1)]
num3 = det_s1b[(60-1):(71-2)]
num4 = det_s1b[(71-2):(82-3)]
num5 = det_s1b[(82-3):(93-4)]
num6 = det_s1b[(93-4):]


# In[1]:


def lectura_archivos_det(nombre_archivo):
    completo = pd.read_csv(nombre_archivo,header=None, sep='\n')
    
    List_archivo = []
    with open(nombre_archivo,'r') as f:
        reader = csv.reader(f,delimiter='\n')
        for i,line in enumerate(reader):
            List_archivo.append(line)
    
    indices_vacios = []
    for i in range(len(List_archivo)):
        if not List_archivo[i]:
            indices_vacios.append(i)

    bloque1 = completo[:indices_vacios[0]]
    bloque2 = completo[indices_vacios[0]:(indices_vacios[1]-1)]
    bloque3 = completo[(indices_vacios[1]-1):(indices_vacios[2]-2)]
    bloque4 = completo[(indices_vacios[2]-2):(indices_vacios[3]-3)]
    bloque5 = completo[(indices_vacios[3]-3):(indices_vacios[4]-4)]
    bloque6 = completo[(indices_vacios[4]-4):]
    
    #Separamos cada valor por comas de cada renglón para obtener nuestra tabla a analizar cada bloque
    bloque1_mod = bloque1[0].str.split(',', expand=True)
    bloque2_mod = bloque2[0].str.split(',', expand=True)
    bloque3_mod = bloque3[0].str.split(',', expand=True)
    bloque4_mod = bloque4[0].str.split(',', expand=True)
    bloque5_mod = bloque5[0].str.split(',', expand=True)
    bloque6_mod = bloque6[0].str.split(',', expand=True)
    
    #Es necesario modificar los valores None por valores NaN
    bloque1_mod.fillna(value=np.nan,inplace=True)
    bloque2_mod.fillna(value=np.nan,inplace=True)
    bloque3_mod.fillna(value=np.nan,inplace=True)
    bloque4_mod.fillna(value=np.nan,inplace=True)
    bloque5_mod.fillna(value=np.nan,inplace=True)
    bloque6_mod.fillna(value=np.nan,inplace=True)
    
     #Cambiamos el formato de str a float ya que no son cadenas de texto si no que son flotantes 
    #Número de columnas de cada dataframe
    columnas1 = bloque1_mod.shape[1]
    columnas2 = bloque2_mod.shape[1]
    columnas3 = bloque3_mod.shape[1]
    columnas4 = bloque4_mod.shape[1]
    columnas5 = bloque5_mod.shape[1]
    columnas6 = bloque6_mod.shape[1]
    
    for col in range(columnas1):
        bloque1_mod[col] = bloque1_mod[col].astype(float)

    for col in range(columnas2):
        bloque2_mod[col] = bloque2_mod[col].astype(float)

    for col in range(columnas3):
        bloque3_mod[col] = bloque3_mod[col].astype(float)

    for col in range(columnas4):
        bloque4_mod[col] = bloque4_mod[col].astype(float)
        
    for col in range(columnas5):
        bloque5_mod[col] = bloque5_mod[col].astype(float)    
    
    for col in range(columnas6):
        bloque6_mod[col] = bloque6_mod[col].astype(float)  
    
    return bloque1_mod,bloque2_mod,bloque3_mod,bloque4_mod,bloque5_mod,bloque6_mod


# In[ ]:




