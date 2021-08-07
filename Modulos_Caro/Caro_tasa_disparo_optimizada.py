#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-- Tasa de disparo optimizada -- 
import csv
import numpy as np

import Caro_lectura_archivo as lectArchivo


# In[2]:


# Función que obtiene los nuevos índices modificados a partir de la lectura del archivo y la eliminación de las filas vacías.
# Con estos ubicamos en qué índice comienza y termina una clase. 
def indices_reales(vacios):
    indices_final = []
    for i in range(len(vacios)):
        indices_corregidos = np.array(vacios)[i] - vacios.index(vacios[i])
        indices_final.append(indices_corregidos)
    return np.array(indices_final)


# In[3]:


def tasa_disparo_optimizada(datos, inicio, fin, ventana, paso):
    
    array_ensayos = np.array(datos)  #Array de arrays que contiene los ensayos realizados de una clase 
    num_ensayos   = len(array_ensayos)
    num_vetanas   = len(np.arange( inicio , fin , paso ))
    array_conteos = np.zeros((num_ensayos, num_vetanas)) #Matriz que almacena los conteos (ensayos x #ventanas)

    razon = (array_ensayos + np.abs(inicio)) // paso #Ensayos (iniciando en cero) entre el tamaño del paso  

    for i in range (num_ensayos): 
        concatena = razon[i] #Calcular todas las ventanas en donde cae la espiga

        for j in range (1,5):
            conteo = razon[i]- j  #Recorrer las ventanas en donde cae la espiga 


            concatena = np.append(concatena[concatena>=0],conteo[conteo>=0]) #Posibilidades positivas de ocurrencia  
            #np.concatenate((concatena,conteo[conteo>=0]))  # Se agrupan los conteos positivos 

        unicos = np.unique(concatena,return_counts=True) #total de espigas x ventana , valores únicos 
        indices = unicos[0].astype(int) #unicos[0] :los valores posibles en concatena, los utilizamos como índices 
        array_conteos[i][indices] = unicos[1][np.arange(0,len(unicos[0]))]   #unicos[1]: cuántas veces ocurre cada valor 

    tiempo = np.arange(inicio + ventana, fin + paso, paso) 
    tasa_disparo = array_conteos / ventana # Tasa de disparo de cada ensayo por separado 
    tasa_disparo_promedio = np.mean(tasa_disparo,0)  #Tasa de disparo promedio de los ensayos
    
    return tasa_disparo, tasa_disparo_promedio


# In[4]:


def tasa_optimizada(inicio,fin,paso,ventana,bloque,ensayos,num_bloques):
    
    num_vetanas =  len(np.arange(inicio + ventana , fin + paso, paso))
    eventos_f = np.zeros((ensayos,num_vetanas+4)) 


    P =(bloque + np.abs(inicio))//paso 

    for i in range (0,ensayos):

        conteo = [P[i]-j for j in range(0,num_bloques+1)]
        agrupada = np.concatenate((conteo[::-1]))
        agrupada = agrupada[agrupada>=0] 
       
        Unica_cad = np.unique(agrupada,return_counts=True)
        long = len(Unica_cad[0])
        longitud = long - 1

        vec = np.arange(0,long)
        val = Unica_cad[0].astype(int)
        eventos_f[i][val] = Unica_cad[1][vec]
        
        #for j in range (0,longitud):
        #
        #    index = int(Unica_cad[0][j])
        #    value = Unica_cad[1][j]
        #    eventos_f[i][index] = value

        
    tasa_eventos = eventos_f/ventana
    tasa_disparo = np.mean(tasa_eventos,0)
    
    return tasa_eventos, tasa_disparo


# In[8]:


def bloques_tasa_det(vacios,neu_det,paso,vent):
    
    indices = indices_reales(vacios)
    
    bloq_1 = neu_det[:indices[0]]
    bloq_2 = neu_det[indices[0]:indices[1]]
    bloq_3 = neu_det[indices[1]:indices[2]]
    bloq_4 = neu_det[indices[2]:indices[3]]
    bloq_5 = neu_det[indices[3]:indices[4]]
    bloq_6 = neu_det[indices[4]:]
    
    bloque1_det = np.array(bloq_1,dtype='object')
    bloque2_det = np.array(bloq_2,dtype='object')
    bloque3_det = np.array(bloq_3,dtype='object')
    bloque4_det = np.array(bloq_4,dtype='object')
    bloque5_det = np.array(bloq_5,dtype='object')
    bloque6_det = np.array(bloq_6,dtype='object')
    
    bloque1_det = [ bloque1_det[i][(bloque1_det[i]>=-2) & (bloque1_det[i]<=3.5)] for i in range(len(bloque1_det))]
    bloque2_det = [ bloque2_det[i][(bloque2_det[i]>=-2) & (bloque2_det[i]<=3.5)] for i in range(len(bloque2_det))]
    bloque3_det = [ bloque3_det[i][(bloque3_det[i]>=-2) & (bloque3_det[i]<=3.5)] for i in range(len(bloque3_det))]
    bloque4_det = [ bloque4_det[i][(bloque4_det[i]>=-2) & (bloque4_det[i]<=3.5)] for i in range(len(bloque4_det))]
    bloque5_det = [ bloque5_det[i][(bloque5_det[i]>=-2) & (bloque5_det[i]<=3.5)] for i in range(len(bloque5_det))]
    bloque6_det = [ bloque6_det[i][(bloque6_det[i]>=-2) & (bloque6_det[i]<=3.5)] for i in range(len(bloque6_det))]
    
    tasa_eventos_1, tasa_disparo_1 = tasa_optimizada(-2,3.5,paso,vent,bloque1_det,len(bloq_1),4)
    tasa_eventos_2, tasa_disparo_2 = tasa_optimizada(-2,3.5,paso,vent,bloque2_det,len(bloq_2),4)
    tasa_eventos_3, tasa_disparo_3 = tasa_optimizada(-2,3.5,paso,vent,bloque3_det,len(bloq_3),4)
    tasa_eventos_4, tasa_disparo_4 = tasa_optimizada(-2,3.5,paso,vent,bloque4_det,len(bloq_4),4)
    tasa_eventos_5, tasa_disparo_5 = tasa_optimizada(-2,3.5,paso,vent,bloque5_det,len(bloq_5),4)
    tasa_eventos_6, tasa_disparo_6 = tasa_optimizada(-2,3.5,paso,vent,bloque6_det,len(bloq_6),4)
    
    TotalEventos = np.vstack([tasa_eventos_1,tasa_eventos_2,tasa_eventos_3,tasa_eventos_4,tasa_eventos_5,tasa_eventos_6])
    
    return TotalEventos


# In[9]:


def bloques_tasa_tiempos(vacios,neu_det,paso,vent):
    
    indices = indices_reales(vacios)
    
    bloq_1 = neu_det[:indices[0]]
    bloq_2 = neu_det[indices[0]:indices[1]]
    bloq_3 = neu_det[indices[1]:indices[2]]
    bloq_4 = neu_det[indices[2]:] 
    
    bloque1_det = np.array(bloq_1,dtype='object')
    bloque2_det = np.array(bloq_2,dtype='object')
    bloque3_det = np.array(bloq_3,dtype='object')
    bloque4_det = np.array(bloq_4,dtype='object')

    tasa_eventos_1, tasa_disparo_1 = tasa_optimizada(-2,8,paso,vent,bloque1_det,len(bloq_1),4)
    tasa_eventos_2, tasa_disparo_2 = tasa_optimizada(-2,8,paso,vent,bloque2_det,len(bloq_2),4)
    tasa_eventos_3, tasa_disparo_3 = tasa_optimizada(-2,8,paso,vent,bloque3_det,len(bloq_3),4)
    tasa_eventos_4, tasa_disparo_4 = tasa_optimizada(-2,8,paso,vent,bloque4_det,len(bloq_4),4)
    
    TotalEventos = np.vstack([tasa_eventos_1,tasa_eventos_2,tasa_eventos_3,tasa_eventos_4])
    
    return TotalEventos


# In[ ]:




