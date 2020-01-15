# Archivo auxiliar de funciones

import glob                  #EXPANCION QUE RECONOCE RUTAS PARA VER ARCHIVOS EN CARPETAS
import patoolib              #DESCOMPRIME UN RAR
import os.path               #MODULO PARA RUTAS 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import datetime
import urllib.request
import pprint
from pandas.io.json import json_normalize

import missingno as msno

#Funcion para ver los valores de cada columna

def contar_valores(df):
   for col in df:
       print(df[col].value_counts)

#Función para ver los datos nulos 
def nulos_out(df):
    """Formula para calcular datos nulos y outliers, 
   y mostrarlo en una tabla de cualquier dataframe con una desviación 
   estandar de 3+- """
    
    a = df.isnull().sum().to_frame(name='Nulos')                             #sumamos los nulos
    a['% Nulos'] = ((a['Nulos'] / len(df)) * 100).round()                    #porcentaje
    #Buscar outliers
    media = np.mean(df.iloc[:, :])
    des_std = np.std(df.iloc[:, :])
    g = des_std * 3

    ss = np.where(
        (df.iloc[:, :] < media - (g)) | (df.iloc[:, :] > media + (g)), True,
        False)

    df3 = pd.DataFrame(ss)
    df5 = df3.sum(axis=0, skipna=True)
    list_out = list(df5)
    a["Outliers"] = list_out
    a['% Outliers'] = ((a['Outliers'] / len(df)) * 100).round()
    b = msno.matrix(df, figsize=(14, 8), fontsize=10)
    return a, b
    
    
    
#HISTOGRAMA

def graficos (df,et):
  data=df[et]
  maxi=data.max()
  mini=data.min()
  r=maxi-mini
  mean = data.mean()
  median = data.median()  
  n=data.shape[0]
  k=1+3.322*np.log(n)
  if int(k)%2==0:
    k=int(k)+1
  else:
    k=int(k)    

  plt.figure(figsize=(10,6))
  datau=data.plot(kind="hist", color='Orange').set_title(" HISTOGRAMA {0}".format(et.upper()),fontsize=28, color='orange')
  plt.axvline(mean, color='r', linestyle='--')

  plt.axvline(median, color='Blue', linestyle='--')
  
  data=pd.cut(data,k, precision=0).value_counts().sort_index()
  data=data.to_frame()
  
  print('linea color ROJO es la Media:', mean)
  print('linea color AZUL es la Mediana: ',median)
  return data

#COMPARACIÓN DE COLUMNAS DE UN DATAFRAME PARA VER COLUMNAS CON LOS MISMOS DATOS

def comparacion(df,x,y):
    
  #return df_15r_completo[(x)] == df_15r_completo[(y)]
   df['iguales'] = (df[(x)] == df[(y)]).astype(bool)
   #df_15r_completo.at[15]= False
   comparacion = (df['iguales'] == True).all()
   if comparacion == True:
       print('Las Columnas Son Iguales')
   else:
       print('Las Columnas Son Distintas')
   return df.drop(['iguales'],axis=1) 



#Función que extrae desde un rar varios archivos csv


def extract_compress(nombre_archivo): # Funcion para sacar archivos csv desde un rar
    folder=patoolib.extract_archive(nombre_archivo) #descomprime un rar
    current_dir = os.path.dirname(os.path.realpath(folder)) # crea una nueva carpeta
    todos = glob.glob(current_dir+'\\'+folder+'\*') # puede ver y trabajar los csv q estan en carpeta
    data = pd.DataFrame() #Dataframe vacio
    for i in todos: # for que entra en la carpeta todos y revisa todos los archivos csv y los junta en un dataframe
        dat = pd.read_csv(i,sep=';')
        data=data.append(dat)
    return data

# Función para unir csv desde una carpeta

def extract(nombre_archivo): # Funcion para sacar archivos csv desde un rar
     
    current_dir = os.path.dirname(os.path.realpath(nombre_archivo)) # crea una nueva carpeta
    todos = glob.glob(current_dir+'\\'+nombre_archivo+'\*') # puede ver y trabajar los csv q estan en carpeta
    data = pd.DataFrame() #Dataframe vacio
    for i in todos: # for que entra en la carpeta todos y revisa todos los archivos csv y los junta en un dataframe
        dat = pd.read_csv(i,sep=';')
        data=data.append(dat)
    return data