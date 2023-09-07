# -*- coding: utf-8 -*-
"""simphysiclab_ldr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CMhkHp3V-fpum-a5f7tbMR5okrV-a_Pa

# <font color="darkorange">Librería LDR de SIMPHYSICLAB</font>

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

En este fichero .py pueden encontrarse todas las funciones desarrolladas para la librería LDR dentro del proyecto SIMPHYSICLAB. No es por tanto un cuaderno al uso sino que será cargado en cada cuaderno del proyecto para poder utilizar dichas funciones.

**Las funciones están relacionadas con ...**

### <font color="darkorange">Librerias de python necesarias para el funcionamiento de las funciones</font>
"""

# Commented out IPython magic to ensure Python compatibility.
#Clonar github con los repositorios
#!wget {f"https://raw.githubusercontent.com/SIMPHYSICLAB/simphysiclab/main/libraries/simphysiclab_sistemas.py"}
import simphysiclab_sistemas as SIS

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
from matplotlib.animation import FuncAnimation
from IPython.display import HTML


from google.colab import output
output.enable_custom_widget_manager()
import ipywidgets as widgets

"""### <font color="darkorange">Funciones para la representación del Lungar de las Raíces</font>

"""

def anguloCuadrante(ceros_polos,punto):

  """
  input:
        ceros_polos: cero o polo del sistema.
        punto: punto a evaluar.
  output:

  código:
        diffTargetSource=ceros_polos-punto

        if type(diffTargetSource)!=complex:
          diffTargetSource=complex(diffTargetSource,0)

        if diffTargetSource.real>=0 and diffTargetSource.imag>=0:
          print("PrimerCuadrante")
        elif diffTargetSource.real<0 and diffTargetSource.imag>=0:
          print("SegundoCuadrante")
        elif diffTargetSource.real<0 and diffTargetSource.imag<0:
          print("TercerCuadrante")
        elif diffTargetSource.real>=0 and diffTargetSource.imag<0:
          print("CuartoCuadrante")
  """

  diffTargetSource=ceros_polos-punto

  if type(diffTargetSource)!=complex:
    diffTargetSource=complex(diffTargetSource,0)

  if diffTargetSource.real>=0 and diffTargetSource.imag>=0:
    print("PrimerCuadrante")
  elif diffTargetSource.real<0 and diffTargetSource.imag>=0:
    print("SegundoCuadrante")
  elif diffTargetSource.real<0 and diffTargetSource.imag<0:
    print("TercerCuadrante")
  elif diffTargetSource.real>=0 and diffTargetSource.imag<0:
    print("CuartoCuadrante")

def criterioArgumento(TF,punto,tolerancia=0):

  """
  input:
        TF: función de transferencia.
        punto: cero o polo del sistema, expresado según complex(real,imag).
        tolerancia: rango de validez del angulo a evaluar, 0 por defecto
  output:
        angulos: angulo para el punto dado
        criterio del argumento:
  código:
        def criterioArgumento(TF,punto,tolerancia=0):
          ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)

          angulos=0;
          angulosCum=[]

          for p in polos:
            diff=(punto-p)
            if type(diff)!=complex:
              diff=complex(diff,0)
            angle=math.degrees(math.atan2(diff.imag, diff.real))
            angulosCum.append(angle)
            angulos-=angle

          for c in ceros:
            diff=(punto-c)
            if type(diff)!=complex:
              diff=complex(diff,0)
            angle=math.degrees(math.atan2(diff.imag, diff.real))
            angulosCum.append(angle)
            angulos+=angle

          q=sympy.Symbol('q')

          if abs(round(angulos))!=0 and abs(abs(round(angulos%360))-180)<=tolerancia:
            return angulos,True
          else:
            return angulos,False
  """

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)

  angulos=0;
  angulosCum=[]

  for p in polos:
    diff=(punto-p)
    if type(diff)!=complex:
      diff=complex(diff,0)
    angle=math.degrees(math.atan2(diff.imag, diff.real))
    angulosCum.append(angle)
    angulos-=angle

  for c in ceros:
    diff=(punto-c)
    if type(diff)!=complex:
      diff=complex(diff,0)
    angle=math.degrees(math.atan2(diff.imag, diff.real))
    angulosCum.append(angle)
    angulos+=angle

  q=sympy.Symbol('q')

  if abs(round(angulos))!=0 and abs(abs(round(angulos%360))-180)<=tolerancia:
    return angulos,True
  else:
    return angulos,False

def criterioModulo(TF,punto):

  """
  input:
        TF: función de transferencia.
        punto: punto a evaluar, expresado según complex(real,imag).
  output:

  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)

        polosden=1;
        cerosnum=1;
        for p in polos:
          diff=p-punto
          if type(diff)!=complex:
            diff=complex(diff,0)
          polosden*=math.sqrt(pow(diff.real, 2)+pow(diff.imag, 2))
        for c in ceros:
          diff=c-punto
          if type(diff)!=complex:
            diff=complex(diff,0)
          cerosnum*=math.sqrt(pow(diff.real, 2)+pow(diff.imag, 2))

        return polosden/(cerosnum*gain)
  """

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)

  polosden=1;
  cerosnum=1;
  for p in polos:
    diff=p-punto
    if type(diff)!=complex:
      diff=complex(diff,0)
    polosden*=math.sqrt(pow(diff.real, 2)+pow(diff.imag, 2))
  for c in ceros:
    diff=c-punto
    if type(diff)!=complex:
      diff=complex(diff,0)
    cerosnum*=math.sqrt(pow(diff.real, 2)+pow(diff.imag, 2))

  return polosden/(cerosnum*gain)

def LDRmanual(fig,ax,G,H,limites,rangoK):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        G: función de transferencia G.
        H: función de transferencia H.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        rangoK: np.arange(0,100,0.1)
  output:

  código:
        #Forzar libreria sympy
        num,den,gain=SIS.InfoTF("num_den",G)
        numcK=[]
        for i in num:
          numcK.append(float(i)*gain)
        num=SIS.generarTF("num_den",numcK,[1],1)
        den=SIS.generarTF("num_den",den,[1],1)
        G=num/den
        #Forzar libreria sympy

        #Forzar libreria sympy
        num,den,gain=SIS.InfoTF("num_den",H)
        numcK=[]
        for i in num:
          numcK.append(float(i)*gain)
        num=SIS.generarTF("num_den",numcK,[1],1)
        den=SIS.generarTF("num_den",den,[1],1)
        H=num/den
        #Forzar libreria sympy

        xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        for i in rango:
          M=SIS.realimentacion(G,H,i)
          ceros,polos,gain=SIS.InfoTF("ceros_polos",M)
          for ptA in polos:
            if ptA.as_real_imag()[0]>xmin:
              ax.scatter(ptA.as_real_imag()[0],ptA.as_real_imag()[1],s=25,c='r', marker="o")
  """
  global axs
  global figs
  global Gs
  global Hs

  #Forzar libreria sympy
  num,den,gain=SIS.InfoTF("num_den",G)
  numcK=[]
  for i in num:
    numcK.append(float(i)*gain)
  num=SIS.generarTF("num_den",numcK,[1],1)
  den=SIS.generarTF("num_den",den,[1],1)
  G=num/den
  #Forzar libreria sympy

  #Forzar libreria sympy
  num,den,gain=SIS.InfoTF("num_den",H)
  numcK=[]
  for i in num:
    numcK.append(float(i)*gain)
  num=SIS.generarTF("num_den",numcK,[1],1)
  den=SIS.generarTF("num_den",den,[1],1)
  H=num/den
  #Forzar libreria sympy

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)

  axs=ax
  figs=fig
  Gs=G
  Hs=H
  ani = FuncAnimation(fig, updateScatterLDRmanual, frames=rangoK, interval=1000, repeat=False)
  #for i in rangoK:
  #  M=SIS.realimentacion(G,H,i)
  #  ceros,polos,gain=SIS.InfoTF("ceros_polos",M)
  #  for ptA in polos:
  #    if ptA.as_real_imag()[0]>xmin:
  #      ax.scatter(ptA.as_real_imag()[0],ptA.as_real_imag()[1],s=25,c='r', marker="o")
  return HTML(ani.to_jshtml())

def updateScatterLDRmanual(frame):
  global axs
  global figs
  global Gs
  global Hs
  M=SIS.realimentacion(G,H,frame)
  ceros,polos,gain=SIS.InfoTF("ceros_polos",M)
  for ptA in polos:
    if ptA.as_real_imag()[0]>xmin:
      ax.scatter(ptA.as_real_imag()[0],ptA.as_real_imag()[1],s=25,c='r', marker="o")

def barridoCriterios(ax,TF,limites,paso,tolerancia):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        G: función de transferencia G.
        H: función de transferencia H.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        paso: unidad minima para el incremento.
        tolerancia: vector para dibujar puntos que cumplan los requisitos de tolerancia especificados, ordenar el vector de mayor a menor
  output:

  código:
        colors_list = list(colors.BASE_COLORS.values())

        xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

        maxX=xmax
        maxY=ymax

        x=[]
        y=[]
        for iX in np.arange(-maxX, maxX, paso):
          for iY in np.arange(-maxY, maxY, paso):
            x.append(iX)
            y.append(iY)
        x = np.array(x)
        y = np.array(y)
        tolerancia=list(reversed(np.sort(tolerancia)))
        dcrmnt=10
        for i in range(len(x)):
          maxDcrmnt=(len(tolerancia)+1)*dcrmnt+20
          index=0
          for j in tolerancia:
            angulos,boolV=criterioArgumento(TF,complex(x[i],y[i]),j)
            if boolV:
              ax.scatter(x[i],y[i],s=maxDcrmnt-dcrmnt,c=colors_list[index], marker="o")
            maxDcrmnt-=dcrmnt
            index+=1
  """
  colors_list = list(colors.BASE_COLORS.values())

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

  x=[]
  y=[]
  print(xmin,xmax,ymin,ymax)
  for iX in np.arange(xmin, xmax, paso):
    for iY in np.arange(ymin, ymax, paso):
      x.append(iX)
      y.append(iY)
  x = np.array(x)
  y = np.array(y)
  tolerancia=list(reversed(np.sort(tolerancia)))
  dcrmnt=15

  maxDcrmnt=(len(tolerancia)+1)*dcrmnt+dcrmnt
  index=0

  for j in tolerancia:
    for i in range(len(x)):
      angulos,boolV=criterioArgumento(TF,complex(x[i],y[i]),j)
      if boolV:
        ax.scatter(x[i],y[i],s=maxDcrmnt-dcrmnt,c=colors_list[index], marker="o")
    maxDcrmnt-=dcrmnt
    index+=1

def comprobarLimitesLDR(G,H):

  """
  input:
        G: función de transferencia G.
        H: función de transferencia H.
  output:
        #Finito=-1,1;Infinito=-2,2
        X: tipo de límite en X.
        Y: tipo de límite en Y.

  código:
        #Forzar libreria control
        num,den,gain=SIS.InfoTF("num_den",G)
        numcK=[]
        for i in num:
          numcK.append(float(i)*gain)
        denc=[]
        for i in den:
          denc.append(float(i))
        G=SIS.generarTF("num_den",numcK,denc)
        #Forzar libreria control

        #Forzar libreria control
        num,den,gain=SIS.InfoTF("num_den",H)
        numcK=[]
        for i in num:
          numcK.append(float(i)*gain)
        denc=[]
        for i in den:
          denc.append(float(i))
        H=SIS.generarTF("num_den",numcK,denc)
        #Forzar libreria control

        M=SIS.realimentacion(G,H,10000000000)
        ceros2,polos2,gain2=SIS.InfoTF("ceros_polos",M)
        M=SIS.realimentacion(G,H,100)
        ceros1,polos1,gain1=SIS.InfoTF("ceros_polos",M)
        #Finito=-1,1;Infinito=-2,2
        Y=[]
        X=[]
        for i in range(len(polos2)):
          print("punto inicial: ",polos1[i],"punto extremo: ",polos2[i])
          if (polos2[i].imag>0):
            if(math.sqrt(pow(polos2[i].imag-polos1[i].imag,2))>50):
              print("infinito Y")
              Y.append(2)
            else:
              print("finito Y")
              Y.append(1)
          elif(polos2[i].imag==0):
              print("finito Y")
              Y.append(0)
          else:
            if(math.sqrt(pow(polos2[i].imag-polos1[i].imag,2))>50):
              print("infinito -Y")
              Y.append(-2)
            else:
              print("finito -Y")
              Y.append(-1)
          if (polos2[i].real>0):
            if(math.sqrt(pow(polos2[i].real-polos1[i].real,2))>50):
              print("infinito X")
              X.append(2)
            else:
              print("finito X")
              X.append(1)
          elif(polos2[i].real-polos1[i].real==0):
              print("finito X")
              X.append(0)
          else:
            if(math.sqrt(pow(polos2[i].real-polos1[i].real,2))>50):
              print("infinito -X")
              X.append(-2)
            else:
              print("finito -X")
              X.append(-1)
        return X,Y
  """
  #Forzar libreria control
  num,den,gain=SIS.InfoTF("num_den",G)
  numcK=[]
  for i in num:
    numcK.append(float(i)*gain)
  denc=[]
  for i in den:
    denc.append(float(i))
  G=SIS.generarTF("num_den",numcK,denc)
  #Forzar libreria control

  #Forzar libreria control
  num,den,gain=SIS.InfoTF("num_den",H)
  numcK=[]
  for i in num:
    numcK.append(float(i)*gain)
  denc=[]
  for i in den:
    denc.append(float(i))
  H=SIS.generarTF("num_den",numcK,denc)
  #Forzar libreria control

  M=SIS.realimentacion(G,H,10000000000)
  ceros2,polos2,gain2=SIS.InfoTF("ceros_polos",M)
  M=SIS.realimentacion(G,H,100)
  ceros1,polos1,gain1=SIS.InfoTF("ceros_polos",M)
  #Finito=-1,1;Infinito=-2,2
  Y=[]
  X=[]
  for i in range(len(polos2)):
    print("punto inicial: ",polos1[i],"punto extremo: ",polos2[i])
    if (polos2[i].imag>0):
      if(math.sqrt(pow(polos2[i].imag-polos1[i].imag,2))>50):
        print("infinito Y")
        Y.append(2)
      else:
        print("finito Y")
        Y.append(1)
    elif(polos2[i].imag==0):
        print("finito Y")
        Y.append(0)
    else:
      if(math.sqrt(pow(polos2[i].imag-polos1[i].imag,2))>50):
        print("infinito -Y")
        Y.append(-2)
      else:
        print("finito -Y")
        Y.append(-1)
    if (polos2[i].real>0):
      if(math.sqrt(pow(polos2[i].real-polos1[i].real,2))>50):
        print("infinito X")
        X.append(2)
      else:
        print("finito X")
        X.append(1)
    elif(polos2[i].real-polos1[i].real==0):
        print("finito X")
        X.append(0)
    else:
      if(math.sqrt(pow(polos2[i].real-polos1[i].real,2))>50):
        print("infinito -X")
        X.append(-2)
      else:
        print("finito -X")
        X.append(-1)
  return X,Y

def LDRautomatico(ax,TF,limites,gainPlot=False,rangeK=None):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        TF: función de transferencia.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        K: rango de valores de K np.arange(0,1000,0.1) o valor unico de K
  output:
        plist: lista de puntos.
        klist: lista de valores de k para cada punto.

  código:
        xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)
        try:
          if rangeK.any()==None:
            if ax!=None:
              plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot)
            else:
              plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot)
          else:
            if ax!=None:
              plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot)
            else:
              plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot)
        except:
          if rangeK==None:
            if ax!=None:
              plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot)
            else:
              plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot)
          else:
            if ax!=None:
              plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot)
            else:
              plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot)

        return plist, klist
  """

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)
  try:
    if rangeK.any()==None:
      if ax!=None:
        plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot,plot=True)
      else:
        plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot,plot=False)
    else:
      if ax!=None:
        plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot,plot=True)
      else:
        plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot,plot=False)
  except:
    if rangeK==None:
      if ax!=None:
        plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot,plot=True)
      else:
        plist, klist = control.root_locus(TF,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot,plot=False)
    else:
      if ax!=None:
        plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],ax=ax,print_gain = gainPlot,plot=True)
      else:
        plist, klist = control.root_locus(TF,rangeK,grid=False,xlim=[xmin,xmax],ylim=[ymin,ymax],print_gain = gainPlot,plot=False)

  return plist, klist

def norma1ramas(TF):
  """
  input:
        TF: función de transferencia.
  output:

  código:
        orden=SIS.ordenTF(TF)
        print("Norma 1: Número de ramas r:"+str(orden))
  """
  orden=SIS.ordenTF(TF)
  print("Norma 1: Número de ramas r:"+str(orden))

def norma2ramasInfinito(TF):
  """
  input:
        TF: función de transferencia.
  output:

  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
        print("Norma 2: Punto de comienzo Polos y punto final Ceros o Infinito (Nº polos-Nº ceros):")
        print(" Número de ramas que tienden al infinito:"+str(len(polos)-len(ceros)))
  """
  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
  print("Norma 2: Punto de comienzo Polos y punto final Ceros o Infinito (Nº polos-Nº ceros):")
  print(" Número de ramas que tienden al infinito:"+str(len(polos)-len(ceros)))

def norma3ejeReal(ax,limites,TF):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        TF: función de transferencia.
  output:

  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)

        c=np.concatenate((ceros,polos))
        c=np.insert(c,0, c[0]-10)

        for index in range(0,len(c)-1):
            deletelist=c
            if sum(((c[index].real-c[index+1].real)/2+c[index+1].real)<deletelist.real)%2==1:
              plt.plot([int(c[index].real),int(c[index+1].real)], [0,0],
                  linewidth=4.0,
                  linestyle='-',
                  color='b',
                  alpha=0.5,
                  marker='o')
  """
  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)
  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)

  c=np.concatenate((ceros,polos))
  c=np.insert(c,0, c[0]-10)

  for index in range(0,len(c)-1):
      deletelist=c
      if sum(((c[index].real-c[index+1].real)/2+c[index+1].real)<deletelist.real)%2==1:
        plt.plot([int(c[index].real),int(c[index+1].real)], [0,0],
            linewidth=4.0,
            linestyle='-',
            color='b',
            alpha=0.5,
            marker='o')

def norma4nAsintotas(TF):

  """
  input:
        TF: función de transferencia.
  output:
        nAsintotas: numero de asintotas
  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
        nAsintotas=len(polos)-len(ceros)
        return nAsintotas
  """

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
  nAsintotas=len(polos)-len(ceros)

  return nAsintotas

def norma4interseccionAsintotas(TF):

  """
  input:
        TF: función de transferencia.
  output:
        interAsin: punto de intersección del limite asintoticos.
  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
        interAsin=int((sum(polos)-sum(ceros))/(len(polos)-len(ceros)))
        return interAsin
  """

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
  interAsin=int((sum(polos)-sum(ceros))/(len(polos)-len(ceros)))
  return interAsin

def norma4dibujarAsintotas(ax,limites,TF):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        TF: función de transferencia.
  output:

  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
        k=len(polos)-len(ceros)
        print("Numero de ramas al infinito :",k)
        q = sympy.symbols('k')
        print(str(180*(2*q+1)/(len(polos)-len(ceros)))+ ", para k>0, donde k= 0,+1,+2,+3,...")
        for i in range(0,k):
          print((180*(2*i+1)/(len(polos)-len(ceros))))
          angle=(180*(2*i+1)/(len(polos)-len(ceros)))
          phi = np.deg2rad(angle)
          L = np.array([0, 10])
          x = norma4interseccionAsintotas(TF) + np.cos(phi) * L
          y = 0 + np.sin(phi) * L
          ax.plot(x, y,'--')
  """
  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)
  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
  k=len(polos)-len(ceros)
  print("Numero de ramas al infinito :",k)
  q = sympy.symbols('k')
  print(str(180*(2*q+1)/(len(polos)-len(ceros)))+ ", para k>0, donde k= 0,+1,+2,+3,...")
  for i in range(0,k):
    print((180*(2*i+1)/(len(polos)-len(ceros))))
    angle=(180*(2*i+1)/(len(polos)-len(ceros)))
    phi = np.deg2rad(angle)
    L = np.array([0, 10])
    x = norma4interseccionAsintotas(TF) + np.cos(phi) * L
    y = 0 + np.sin(phi) * L
    ax.plot(x, y,'--')

def norma5simetria(ax,limites,TF):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        TF: función de transferencia.
  output:

  código:
        xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)
        rlist,klist=LDRautomatico(ax,TF,[[xmin,xmax],[ymin,ymax]])
        ax.plot(rlist.real,rlist.imag)
  """

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)
  rlist,klist=LDRautomatico(ax,TF,[[xmin,xmax],[ymin,ymax]])
  ax.plot(rlist.real,rlist.imag)

def norma6anguloIndividual(TF,ceroPolo):

  """
  input:
        TF: función de transferencia.
        ceroPolo: cero o polo en el que evaluar los angulos.
  output:
        anguloCeroPolo: angulo del cero o polo.
  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
        anguloCeroPolo=[]
        if ceroPolo.imag!=0:
          angulos=0;
          for cp2 in ceros:
            if cp2!=ceroPolo:
              angulos+=math.atan2(abs(cp2.imag-ceroPolo.real), abs(cp2.real-ceroPolo.real))
          for cp2 in polos:
            if cp2!=ceroPolo:
              angulos-=math.atan2(abs(cp2.imag-ceroPolo.real), abs(cp2.real-ceroPolo.real))
          angrdv=(-(angulos-math.pi))
          if angrdv<0:
            angrdv=2*math.pi+angrdv
          anguloCeroPolo=angrdv*(180/math.pi)
        return anguloCeroPolo
  """

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
  anguloCeroPolo=[]
  if ceroPolo.imag!=0:
    angulos=0;
    for cp2 in ceros:
      if cp2!=ceroPolo:
        angulos+=math.atan2(abs(cp2.imag-ceroPolo.real), abs(cp2.real-ceroPolo.real))
    for cp2 in polos:
      if cp2!=ceroPolo:
        angulos-=math.atan2(abs(cp2.imag-ceroPolo.real), abs(cp2.real-ceroPolo.real))
    angrdv=(-(angulos-math.pi))
    if angrdv<0:
      angrdv=2*math.pi+angrdv
    anguloCeroPolo=angrdv*(180/math.pi)
  return anguloCeroPolo

def norma6angulos(ax,limites,TF):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        TF: función de transferencia.
  output:
        [[angulosPolos,listaPolos],[angulosCeros,listaCeros]]: lista de angulos de polo y ceros y su correspondencia.

  código:
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
        angulosCeros=[]
        listaCeros=[]
        for c in ceros:
          angulosCeros.append(norma6anguloIndividual(TF,c))
          listaCeros.append(c)
        angulosPolos=[]
        listaPolos=[]
        for p in polos:
          angulosPolos.append(norma6anguloIndividual(TF,c))
          listaPolos.append(p)
        return [[angulosPolos,listaPolos],[angulosCeros,listaCeros]]
  """

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)

  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
  angulosCeros=[]
  listaCeros=[]
  for c in ceros:
    angulosCeros.append(norma6anguloIndividual(TF,c))
    listaCeros.append(c)
  angulosPolos=[]
  listaPolos=[]
  for p in polos:
    angulosPolos.append(norma6anguloIndividual(TF,p))
    listaPolos.append(p)
  return [[angulosPolos,listaPolos],[angulosCeros,listaCeros]]

def norma7confluenciaDispersion(ax,limites,TF):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        TF: función de transferencia.
  output:
        solveCP,validSolveCP: ceros y polos como solución posible de la intersección entre ramas y eje X y puntos validos.

  código:
        sgm=sympy.symbols('sgm')
        ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
        cerosSum=0
        polosSum=0
        for i in ceros:
          cerosSum+=(1/(sgm-i))
        for i in polos:
          polosSum+=(1/(sgm-i))

        solveCP=cerosSum-polosSum
        solveCP=sympy.solve(solveCP)

        validSolveCP=[]
        for j in solveCP:
          if criterioArgumento(G,complex(j.as_real_imag()[0],j.as_real_imag()[1]))[1]:
            ax.plot(j.as_real_imag()[0],j.as_real_imag()[1],'o')
            validSolveCP.append(complex(j.as_real_imag()[0],j.as_real_imag()[1]))
        return solveCP,validSolveCP
  """

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)

  sgm=sympy.symbols('sgm')
  ceros,polos,gain=SIS.InfoTF("ceros_polos",TF)
  cerosSum=0
  polosSum=0
  for i in ceros:
    cerosSum+=(1/(sgm-i))
  for i in polos:
    polosSum+=(1/(sgm-i))

  solveCP=cerosSum-polosSum
  solveCP=sympy.solve(solveCP)

  validSolveCP=[]
  for j in solveCP:
    if criterioArgumento(TF,complex(j.as_real_imag()[0],j.as_real_imag()[1]))[1]:
      ax.plot(j.as_real_imag()[0],j.as_real_imag()[1],'o')
      validSolveCP.append(complex(j.as_real_imag()[0],j.as_real_imag()[1]))
  return solveCP,validSolveCP

def norma7confluenciaDispersionMetodoAlt(ax,limites,TF):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        TF: función de transferencia.
  output:
        solveCP,validSolveCP: ceros y polos como solución posible de la intersección entre ramas y eje X y puntos validos

  código:
        #Forzar libreria sympy
        s=sympy.symbols('s')
        num,den,gain=SIS.InfoTF("num_den",TF)
        numcK=[]
        for i in num:
          numcK.append(float(i)*gain)
        num=SIS.generarTF("num_den",numcK,[1],1)
        den=SIS.generarTF("num_den",den,[1],1)
        #Forzar libreria sympy

        print(num)
        print(den)
        print((den/num))
        derivative = sympy.diff(-(den/num),s)
        print(derivative)

        solveCP=sympy.solve(derivative)
        print(solveCP)

        validSolveCP=[]
        for j in solveCP:
          if criterioArgumento(G,complex(j.as_real_imag()[0],j.as_real_imag()[1]))[1]:
            ax.plot(j.as_real_imag()[0],j.as_real_imag()[1],'o')
            validSolveCP.append(complex(j.as_real_imag()[0],j.as_real_imag()[1]))
        return solveCP,validSolveCP
  """

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)

  #Forzar libreria sympy
  s=sympy.symbols('s')
  num,den,gain=SIS.InfoTF("num_den",TF)
  numcK=[]
  for i in num:
    numcK.append(float(i)*gain)
  num=SIS.generarTF("num_den",numcK,[1],1)
  den=SIS.generarTF("num_den",den,[1],1)
  #Forzar libreria sympy

  print(num)
  print(den)
  print((den/num))
  derivative = sympy.diff(-(den/num),s)
  print(derivative)

  solveCP=sympy.solve(derivative)
  print(solveCP)

  validSolveCP=[]
  for j in solveCP:
    if criterioArgumento(TF,complex(j.as_real_imag()[0],j.as_real_imag()[1]))[1]:
      ax.plot(j.as_real_imag()[0],j.as_real_imag()[1],'o')
      validSolveCP.append(complex(j.as_real_imag()[0],j.as_real_imag()[1]))
  return solveCP,validSolveCP

def norma8corteEjeImaginario(ax,limites,G,H):

  """
  input:
        ax: ventana donde se dibujará la imagen.
        limites: formato de entrada en el que pueden faltar algun componente de los cuatro valores [[-x,x],[-y,y]].
        G: función de transferencia G del sistema.
        H: función de transferencia H del sistema.
  output:

  código:
        #Forzar libreria sympy
        numG,denG,gainG=SIS.InfoTF("num_den",G)
        numcK=[]
        for i in numG:
          numcK.append(float(i)*gainG)
        numG=numcK
        numH,denH,gainH=SIS.InfoTF("num_den",H)
        numcK=[]
        for i in numH:
          numcK.append(float(i)*gainH)
        numH=numcK
        #Forzar libreria sympy

        k = sympy.Symbol('k')
        s = sympy.symbols('s')
        num1=sympy.Poly(numG, s)
        den1=sympy.Poly(denG, s)
        num2=sympy.Poly(numH, s)
        den2=sympy.Poly(denH, s)
        G=(k*num1)/den1
        H=num2/den2
        dNClsLp=den2*(k*num1)
        TF=((G)/(1+(G)*H))/dNClsLp
        TF=sympy.simplify(TF)
        TF=1/TF
        sP=sympy.Poly(TF,s)
        A= routh(sympy.Poly(TF, s))
        print(sP)
        print(A)

        equation_subs=A[:, 0]
        solve_equation_subs=sympy.solve([e > 0 for e in equation_subs], k)
        solution_set=solve_equation_subs.as_set()

        fig = plt.figure(figsize = (5,5))
        ax = fig.add_subplot(1,1,1)

        print("solution_set: ",solution_set)
        for i in range(sP.degree(),-1,-1):
          es=A[i, :]
          print("es: ",es,i,sP.degree(),i)
          C=SIS.ecuacionCaracteristicaRouth(es,sP.degree(),i)
          print("sa",solution_set.args[1])
          TFsubs=sympy.Poly(C,s).subs(k,solution_set.args[0])
          ss=sympy.solve(TFsubs)
          if len(ss)!=0:
            for i in ss:
              ax.plot(i.as_real_imag()[0],i.as_real_imag()[1],'o')
  """

  xmin,xmax,ymin,ymax=SIS.ajustarLimites(limites)

  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)

  #Forzar libreria sympy
  numG,denG,gainG=SIS.InfoTF("num_den",G)
  numcK=[]
  for i in numG:
    numcK.append(float(i)*gainG)
  numG=numcK
  numH,denH,gainH=SIS.InfoTF("num_den",H)
  numcK=[]
  for i in numH:
    numcK.append(float(i)*gainH)
  numH=numcK
  #Forzar libreria sympy

  k = sympy.Symbol('k')
  s = sympy.symbols('s')
  num1=sympy.Poly(numG, s)
  den1=sympy.Poly(denG, s)
  num2=sympy.Poly(numH, s)
  den2=sympy.Poly(denH, s)
  G=(k*num1)/den1
  H=num2/den2
  dNClsLp=den2*(k*num1)
  TF=((G)/(1+(G)*H))/dNClsLp
  TF=sympy.simplify(TF)
  TF=1/TF
  sP=sympy.Poly(TF,s)
  A= routh(sympy.Poly(TF, s))
  print(sP)
  print(A)

  equation_subs=A[:, 0]
  solve_equation_subs=sympy.solve([e > 0 for e in equation_subs], k)
  solution_set=solve_equation_subs.as_set()

  print("solution_set: ",solution_set)
  for i in range(sP.degree(),-1,-1):
    es=A[i, :]
    print("es: ",es,i,sP.degree(),i)
    C=SIS.ecuacionCaracteristicaRouth(es,sP.degree(),i)
    print("sa",solution_set.args[1])
    TFsubs=sympy.Poly(C,s).subs(k,solution_set.args[0])
    ss=sympy.solve(TFsubs)
    if len(ss)!=0:
      for i in ss:
        ax.plot(i.as_real_imag()[0],i.as_real_imag()[1],'o')