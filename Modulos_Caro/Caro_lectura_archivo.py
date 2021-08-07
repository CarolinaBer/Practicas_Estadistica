#!/usr/bin/env python
# coding: utf-8

# In[1]:


#----------- Carolina Lectura de archivo --------------------------

#A continuación se crea una función que conforma el módulo de lectura del archivo para calcular las tasas
#de disparo que funcione para los archivos de Tiempos y Detección de manera optimizada. 


# In[2]:


import csv
import numpy as np


# In[3]:


#Leemos el archivo y colocamos su contenido dentro de una lista, cada elemento de esta lista está separado por /n 
#salto de línea, esta lista incluye en cada uno de sus índices, una fila del archivo de excel. 
import csv
List = []
with open('Practica2_Estadistica/Neu_Det_S1B.csv','r') as f:
    reader = csv.reader(f,delimiter='\n')
    f.close
    for i,line in enumerate(reader):
        List.append(line)  


# In[4]:


#Buscamos los índices que corresponden a elementos de la lista cuyo contenido es una lista vacía. Esto es por que en el 
#archivo separamos cada clase con una fila de excel en blanco 
indices = []
for i in range(len(List)):
    if not List[i]:
        indices.append(i)
indices


# In[5]:


#Eliminamos dichos elementos de nuestra lista original 
List = [i for j, i in enumerate(List) if j not in indices]
len(List)


# In[6]:


# Creamos nuestra lista final, la cual se obtiene al separar los elementos por comas, en excel esto representa que estamos 
# separando los elementos por celdas. Además indicamos que el tipo de dato almacenado es foltante. Finalmente creamos
# un arreglo que contenga dichos valores y los vamos almaacenando en una lista. 

final_list = []
for i in range(len(List)):
    elementos = List[i][0].split(',')
    elementos = [float(i) for i in elementos]
    final = np.array(elementos)
    final_list.append(final)
len(final_list)


# In[7]:


#Finalmente creamos la función deseada para cada archivo
def lectura_archivo(nombre_archivo):
    List = []
    with open(nombre_archivo,'r') as f:
        reader = csv.reader(f,delimiter='\n')
        f.close
        for i,line in enumerate(reader):
            List.append(line)    
    indices = []
    for i in range(len(List)):
        if not List[i]:
            indices.append(i)
    List = [i for j, i in enumerate(List) if j not in indices]
    len(List)        
    final_list = []
    for i in range(len(List)):
        elementos = List[i][0].split(',')
        elementos = [float(i) for i in elementos]
        final = np.array(elementos)
        final_list.append(final)
    return indices,final_list


# In[ ]:




