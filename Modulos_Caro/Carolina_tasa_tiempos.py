#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Librería cálculo tasa de disparo elaborada por Carolina Bernal Rodríguez.


# In[2]:


#En específico esta librería fue creada para su uso en la práctica 2, en los archivos de Tiempos, 
#ya que estos cuentan con 4 clases de 15 ensayos cada una. 


# In[3]:


#Importamos las librerías. 
import pandas as pd
import numpy as np


# In[4]:


#Función que toma los datos y separa por clases además de modificarlas para ser utilizables
def separar_por_clase(data):    
    clase1 = data[0:15] 
    clase2 = data[15:30]
    clase3 = data[30:45]
    clase4 = data[45:60]
    
    #Separamos cada valor por comas de cada renglón para obtener nuestra tabla a analizar cada clase 
    clase1_mod = clase1[0].str.split(',', expand=True)
    clase2_mod = clase2[0].str.split(',', expand=True)
    clase3_mod = clase3[0].str.split(',', expand=True)
    clase4_mod = clase4[0].str.split(',', expand=True)

    #Es necesario modificar los valores None por valores NaN
    clase1_mod.fillna(value=np.nan,inplace=True)
    clase2_mod.fillna(value=np.nan,inplace=True)
    clase3_mod.fillna(value=np.nan,inplace=True)
    clase4_mod.fillna(value=np.nan,inplace=True)
    
    #Cambiamos el formato de str a float ya que no son cadenas de texto si no que son flotantes 
    #Número de columnas de cada dataframe
    columnas1 = clase1_mod.shape[1]
    columnas2 = clase2_mod.shape[1]
    columnas3 = clase3_mod.shape[1]
    columnas4 = clase4_mod.shape[1]

    for col in range(columnas1):
        clase1_mod[col] = clase1_mod[col].astype(float)

    for col in range(columnas2):
        clase2_mod[col] = clase2_mod[col].astype(float)

    for col in range(columnas3):
        clase3_mod[col] = clase3_mod[col].astype(float)

    for col in range(columnas4):
        clase4_mod[col] = clase4_mod[col].astype(float)
    
    return  clase1_mod, clase2_mod, clase3_mod, clase4_mod


# In[5]:


#Se crea la función ventana_causal ya que se requiere de una ventana causal, cuadrada y de cualquier longitud
def ventana_causal(tiempo,long_ventana):
    return tiempo + long_ventana


# In[6]:


#Función particiones temporales:
#lista_tiempos: Recibe una lista cuyo primer elemento es una lista con el par de valor extremo(inferior), valor extremo + tamaño de ventana, en segundos.
#paso_tiempo que es la longitud de los pasos temporales (en segundos).
#lim_inferior y lim_superior son los extremos temporales de la partición.

def particiones_temporales(lista_tiempos, paso_tiempo,lim_inferior,lim_superior,long_ventana):
    rango = (abs(lim_inferior)+abs(lim_superior))/paso_tiempo
    for seg in range(int(rango)-1):
        tiempo_actual = lista_tiempos[seg][0] + paso_tiempo
        parejas_tiempo = [round(tiempo_actual,4) ,round(ventana_causal(tiempo_actual,long_ventana),4)]
        lista_tiempos.append(parejas_tiempo)
    return lista_tiempos


# In[8]:


def lista_tiempos(ext_inf,ext_sup,ancho_vent,paso_temp):
    return particiones_temporales([ext_inf,(ext_inf+paso_temp)],paso_temp,ext_inf,ext_sup,ancho_vent)


# In[9]:


#Función que compara la si la lista_comparable de tiempos cae en algún intervalo de la lista_tiempos
def comparar_tiempo(lista_tiempos,lista_comparable):
    lista_coincidencias =  [0]*len(lista_tiempos)     
    for i in range(len(lista_coincidencias)):
        for p in range(len(lista_comparable)):
            if (lista_tiempos[i][0]<= lista_comparable[p] <= lista_tiempos[i][1]) == True:
                    lista_coincidencias[i] = lista_coincidencias[i] + 1
    return lista_coincidencias


# In[10]:


# Para cada uno de los ensayos se tiene que encontrar el número de espigas correspondientes a cada intervalo utilizando la función comparar_tiempo
# Cada una de estas cuentas es almacenada en una lista para formar una lista de listas. 
#Creamos ahora una función que incluya la clase a analizar 
def numero_espigas_lista_de_listas(clase,lista_tiempos):
    num_ensayos = clase.shape[0]
    lista_de_listas=[]
    for i in range(num_ensayos):          #En este caso la longitud está dada por el número de ensayos de la clase 
        lista_de_listas.append(comparar_tiempo(lista_tiempos,list(clase.iloc[i])))
    return lista_de_listas


# In[11]:


#Exactamente lo que se había realizado para clase1, pero ahora se generaliza con una función de acumulado de espigas
def acumulado_espigas(lista_de_listas):
    lista_suma = []
    for i in range(len(lista_de_listas[0])):
        suma=0
        for j in range(len(lista_de_listas)): 
            suma = lista_de_listas[j][i]+suma
        lista_suma.append(suma)
    return lista_suma


# In[12]:


#Función de la que se obtiene los extremos de la lista de intervalos 
def lista_extremos(lim_inferior,lim_superior,paso_tiempo,ancho_ven):
    lista_tiempos = particiones_temporales([lim_inferior,(lim_inferior+paso_tiempo)],paso_tiempo,lim_inferior,lim_superior,ancho_ven)
    lista_extremos_final = []
    rango = (abs(lim_inferior)+abs(lim_superior))/paso_tiempo
    for i in range(int(rango)): 
        lista_extremos_final.append(lista_tiempos[i][1])
    return lista_extremos_final


# In[13]:


#Función que calcula 
def tasa_disparo_clases_agrupadas(data,ext_inf,ext_sup,ancho_vent,paso_temp):
    ensayos = 15
    listas_de_clase = []
    array_lista_suma = [] 
    array_tasa_disparo = []
    array_tren_espigas = []
    array_df_tasa_disparo = []
    
    clases_mod = separar_por_clase(data)
    lista_tiempos = particiones_temporales([ext_inf,(ext_inf+paso_temp)],paso_temp,ext_inf,ext_sup,ancho_vent)
    
   # lista_extremos_final = lista_extremos(ext_inf,ext_sup,paso_temp)
    
    for i in range(len(clases_mod)):
        lista_de_listas = numero_espigas_lista_de_listas(clases_mod[i],lista_tiempos)
        listas_de_clase.append(lista_de_listas)
        
        lista_de_listas = listas_de_clase[i]
        lista_suma = acumulado_espigas(lista_de_listas)
        array_lista_suma.append(lista_suma)
        
        tasa_disparo = list(map(lambda x: x/((ancho_vent)*(ensayos)), array_lista_suma[i]))
        array_tasa_disparo.append(tasa_disparo)
        
        tren_de_espigas ={
                        'tiempo': lista_extremos(ext_inf,ext_sup,paso_temp,ancho_vent),
                        'tasa_disparo': array_tasa_disparo[i]
                         }
        array_tren_espigas.append(tren_de_espigas)
        df_tasa_disparo = pd.DataFrame(array_tren_espigas[i])
        array_df_tasa_disparo.append(df_tasa_disparo)
        
    return  array_df_tasa_disparo


# In[ ]:





# In[ ]:





# In[ ]:




