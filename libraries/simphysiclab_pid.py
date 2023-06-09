# -*- coding: utf-8 -*-
"""simphysiclab_pid.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TLidbduvm27RaB1S0PqKy7CYGlpX5PPd
"""

# Commented out IPython magic to ensure Python compatibility.
#Clonar github con los repositorios
#!wget {f"https://raw.githubusercontent.com/SIMPHYSICLAB/simphysiclab/main/libraries/simphysiclab_sistemas.py"}
#!wget {f"https://raw.githubusercontent.com/SIMPHYSICLAB/simphysiclab/main/libraries/simphysiclab_ldr.py"}
import simphysiclab_sistemas as SIS
import simphysiclab_ldr as LDR

#Standard Python libraries:
import math
import random
import time
import numpy as np

#Specific control system python libraries:
import control
import sympy
#from sympy import *
from tbcontrol.symbolic import routh 


#Plot python libraries
#interactive
# %matplotlib ipympl
import matplotlib.pyplot as plt
import matplotlib.path as mpath

#interactive
from google.colab import output
#interactive
output.enable_custom_widget_manager()
#interactive
import ipywidgets as widgets

"""# **FUNCIONES PARA LA IMPLEMENTACION DE CONTROLADORES TIPO P, TIPO PI, TIPO PD Y TIPO PID**"""

def regTrans_areaIntersectionWithPoints(ax,x,y,maxX,maxY,theta=None,Wd=None,sgm=None):
  xMp,yMp=SIS.restriccionMp(ax,theta,40,40)
  path1  = mpath.Path(np.column_stack([xMp,yMp]))
  xTp,yTp=SIS.restriccionTp(ax,Wd,40,40)
  path2 = mpath.Path(np.column_stack([xTp,yTp]))
  xTs,yTs=SIS.restriccionTs(ax,sgm,40,40)
  path3 = mpath.Path(np.column_stack([xTs,yTs]))

   #n_puntos = 200
   #x = np.random.uniform(-15, 15, n_puntos)
   #y = np.random.uniform(-15, 15, n_puntos)

  puntos_dentro3 = path3.contains_points(np.column_stack([x, y]))
  puntos_dentro2 = path2.contains_points(np.column_stack([x, y]))
  puntos_dentro = path1.contains_points(np.column_stack([x, y]))

  intersection= np.logical_and(puntos_dentro3, puntos_dentro2)
  intersectionf= np.logical_and(intersection, puntos_dentro)
  # Graficamos los puntos que se encuentran dentro del área delimitada
  if ax!=None:
    ax.scatter(x[intersectionf], y[intersectionf], color='g')

  return x[intersectionf], y[intersectionf]