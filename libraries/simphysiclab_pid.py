# -*- coding: utf-8 -*-
"""simphysiclab_pid.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tPv4NQiBviewu1jsTRphXe5cF6CtXsqH

# <font color="darkorange">Librería PID de SIMPHYSICLAB</font>

**Autoría**:

*   Eduardo Iáñez (eianez@umh.es)
*   Vicente Quiles (vquiles@umh.es)
*   Federico Botella (federico@umh.es)

Departamento de Ingeniería de Sistemas y Automática.

Universidad Miguel Hernández de Elche.


**Financiación**: El material que aparece a continuación se ha desarrollado dentro del marco del proyecto UNIDIGITAL- SIMPHYSICLAB.

<small><img src=https://raw.githubusercontent.com/SIMPHYSICLAB/simphysiclab/main/images/logo_unidigital_simphysiclab.png></small>

**Fecha última edición**: 15/06/2023

**Licencia**: <small><a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /></small>

*No olvides hacer una copia si deseas utilizarlo. Al usar estos contenidos, aceptas nuestros términos de uso y nuestra política de privacidad.*

### <font color="darkorange">Introducción</font>

En este fichero .py pueden encontrarse todas las funciones desarrolladas para la librería PID dentro del proyecto SIMPHYSICLAB. No es por tanto un cuaderno al uso sino que será cargado en cada cuaderno del proyecto para poder utilizar dichas funciones.

**Las funciones están relacionadas con ...**

### <font color="darkorange">Librerias de python necesarias para el funcionamiento de las funciones</font>
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
import copy
import numpy as np

#Specific control system python libraries:
import control
import sympy
from tbcontrol.symbolic import routh

#Plot python graphic libraries and interactive
import matplotlib
# %matplotlib ipympl
sympy.init_printing()
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.colors as colors

from google.colab import output
output.enable_custom_widget_manager()
import ipywidgets as widgets

"""### <font color="darkorange">Funciones para la implementación de controladores tipo P, tipo PI, tipo PD y tipo PID</font>

"""

def puntosEnAreaValidaSegunRestricciones(TF,theta=None,wd=None,sgm=None,maxK=1000,paso=0.1):
  """
  input:
        TF: función de transferencia.
        theta: límite de la restricción, Sobreoscilación.
        wd: límite de la restricción, Tiempo de pico.
        sgm: límite de la restricción, Tiempo de establecimiento.
        maxK: max value of K 1000.
        paso: paso para el calculo de K, desde 0 hasta maxK, cada valor de paso.
  output:
        xD,yD: lista de puntos xD e yD puntos validos según restricciones que cumplen los requisitos de dominancia.
  código:
        rlist,klist=LDR.LDRautomatico(None,TF,[[-1,1],[-1,1]],False,np.arange(0,maxK,paso))

        x=[]
        y=[]
        countK=0
        for k in rlist:
          for kindx in range(0,len(k)):
            x.append(k[kindx].real)
            y.append(abs(k[kindx].imag))
          countK=countK+1
        x = np.array(x)
        y = np.array(y)

        xMp,yMp=SIS.dibujarRestriccionMp(None,theta,[[-1,1],[-1,1]])
        path1  = mpath.Path(np.column_stack([xMp,yMp]))
        xTp,yTp,nxTp,nyTp=SIS.dibujarRestriccionTp(None,wd,[[-1,1],[-1,1]])
        path2 = mpath.Path(np.column_stack([xTp,yTp]))
        xTs,yTs=SIS.dibujarRestriccionTs(None,sgm,[[-1,1],[-1,1]])
        path3 = mpath.Path(np.column_stack([xTs,yTs]))

        print([xMp,yMp],[xTp,yTp],[nxTp,nyTp],[xTs,yTs])
        puntos_dentro3 = path3.contains_points(np.column_stack([x, y]))
        puntos_dentro2 = path2.contains_points(np.column_stack([x, y]))
        puntos_dentro = path1.contains_points(np.column_stack([x, y]))

        intersection= np.logical_and(puntos_dentro3, puntos_dentro2)
        intersectionf= np.logical_and(intersection, puntos_dentro)

        xI=x[intersectionf]
        yI=y[intersectionf]

        xD=[]
        yD=[]

        for intrf in range(0,len(xI)):
          if (SIS.polosDominantes(TF, complex(xI[intrf],yI[intrf]))==True):
            xD.append(xI[intrf])
            yD.append(yI[intrf])

        xD = np.array(xD)
        yD = np.array(yD)

        return xD, yD
  """
  rlist,klist=LDR.LDRautomatico(None,TF,[[-1,1],[-1,1]],False,np.arange(0,maxK,paso))

  x=[]
  y=[]
  countK=0
  for k in rlist:
    for kindx in range(0,len(k)):
      x.append(k[kindx].real)
      y.append(abs(k[kindx].imag))
    countK=countK+1
  x = np.array(x)
  y = np.array(y)

  xMp,yMp=SIS.dibujarRestriccionMp(None,theta,[[-1,1],[-1,1]])
  path1  = mpath.Path(np.column_stack([xMp,yMp]))
  xTp,yTp,nxTp,nyTp=SIS.dibujarRestriccionTp(None,wd,[[-1,1],[-1,1]])
  path2 = mpath.Path(np.column_stack([xTp,yTp]))
  xTs,yTs=SIS.dibujarRestriccionTs(None,sgm,[[-1,1],[-1,1]])
  path3 = mpath.Path(np.column_stack([xTs,yTs]))

  print([xMp,yMp],[xTp,yTp],[nxTp,nyTp],[xTs,yTs])
  puntos_dentro3 = path3.contains_points(np.column_stack([x, y]))
  puntos_dentro2 = path2.contains_points(np.column_stack([x, y]))
  puntos_dentro = path1.contains_points(np.column_stack([x, y]))

  intersection= np.logical_and(puntos_dentro3, puntos_dentro2)
  intersectionf= np.logical_and(intersection, puntos_dentro)

  xI=x[intersectionf]
  yI=y[intersectionf]

  xD=[]
  yD=[]

  for intrf in range(0,len(xI)):
    if (SIS.polosDominantes(TF, complex(xI[intrf],yI[intrf]))==True):
      xD.append(xI[intrf])
      yD.append(yI[intrf])

  xD = np.array(xD)
  yD = np.array(yD)

  return xD, yD

def comprobarLimitesConRestriccionesLDR(TF,theta=None,wd=None,sgm=None):
  """
  input:
        TF: función de transferencia.
        theta: límite de la restricción, Sobreoscilación.
        wd: límite de la restricción, Tiempo de pico.
        sgm: límite de la restricción, Tiempo de establecimiento.
  output:
        [[xfist,yfirst],[xlast,ylast]]: componente x e y del primer punto con parte imaginaria, componente x e y del último punto con parte imaginaria.
  código:
        x,y=puntosEnAreaValidaSegunRestricciones(TF,theta,wd,sgm)
        findElement=[element for element in y if element != 0][0]
        findLastElement=[element for element in reversed(y) if element != 0][0]
        firstElementComplex=np.where(y == findElement)[0][0]
        LastElementComplex=np.where(y == findLastElement)[0][0]
        if y[LastElementComplex]<100:
          return [x[firstElementComplex],y[firstElementComplex]],[x[LastElementComplex],y[LastElementComplex]]
        else:
          return [x[firstElementComplex],y[firstElementComplex]],None
  """
  x,y=puntosEnAreaValidaSegunRestricciones(TF,theta,wd,sgm)
  findElement=[element for element in y if element != 0][0]
  findLastElement=[element for element in reversed(y) if element != 0][0]
  firstElementComplex=np.where(y == findElement)[0][0]
  LastElementComplex=np.where(y == findLastElement)[0][0]
  if y[LastElementComplex]<50:
    return [x[firstElementComplex],y[firstElementComplex]],[x[LastElementComplex],y[LastElementComplex]]
  else:
    return [x[firstElementComplex],y[firstElementComplex]],None

def areaValidaSegunRestricciones(theta=None,wd=None,sgm=None,paso=0.1):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        paso: unidad minima para el incremento.
        theta: límite de la restricción, Sobreoscilación.
        wd: límite de la restricción, Tiempo de pico.
        sgm: límite de la restricción, Tiempo de establecimiento.
  output:
        x: componente de los puntos X que cumplen todas la restricciones.
        y: componente de los puntos Y que cumplen todas la restricciones.

  código:
        xmin,xmax,ymin,ymax=ajustarLimites(limites)

        xMp,yMp=SIS.dibujarRestriccionMp(None,theta,[[-1,1],[-1,1]])
        path1  = mpath.Path(np.column_stack([xMp,yMp]))
        xTp,yTp,nxTp,nyTp=SIS.dibujarRestriccionTp(None,wd,[[-1,1],[-1,1]])
        path2 = mpath.Path(np.column_stack([xTp,yTp]))
        xTs,yTs=SIS.dibujarRestriccionTs(None,sgm,[[-1,1],[-1,1]])
        path3 = mpath.Path(np.column_stack([xTs,yTs]))

        x=[]
        y=[]
        for iX in np.arange(-100, 100, paso):
          for iY in np.arange(-100, 100, paso):
            x.append(iX)
            y.append(iY)
        x = np.array(x)
        y = np.array(y)

        puntos_dentro3 = path3.contains_points(np.column_stack([x, y]))
        puntos_dentro2 = path2.contains_points(np.column_stack([x, y]))
        puntos_dentro = path1.contains_points(np.column_stack([x, y]))

        intersection= np.logical_and(puntos_dentro3, puntos_dentro2)
        intersectionf= np.logical_and(intersection, puntos_dentro)

        return x[intersectionf], y[intersectionf]
  """

  xMp,yMp=SIS.dibujarRestriccionMp(None,theta,[[-1,1],[-1,1]])
  path1  = mpath.Path(np.column_stack([xMp,yMp]))
  xTp,yTp,nxTp,nyTp=SIS.dibujarRestriccionTp(None,wd,[[-1,1],[-1,1]])
  path2 = mpath.Path(np.column_stack([xTp,yTp]))
  xTs,yTs=SIS.dibujarRestriccionTs(None,sgm,[[-1,1],[-1,1]])
  path3 = mpath.Path(np.column_stack([xTs,yTs]))

  x=[]
  y=[]
  for iX in np.arange(-100, 100, paso):
    for iY in np.arange(-100, 100, paso):
      x.append(iX)
      y.append(iY)
  x = np.array(x)
  y = np.array(y)

  puntos_dentro3 = path3.contains_points(np.column_stack([x, y]))
  puntos_dentro2 = path2.contains_points(np.column_stack([x, y]))
  puntos_dentro = path1.contains_points(np.column_stack([x, y]))

  intersection= np.logical_and(puntos_dentro3, puntos_dentro2)
  intersectionf= np.logical_and(intersection, puntos_dentro)

  return x[intersectionf], y[intersectionf]