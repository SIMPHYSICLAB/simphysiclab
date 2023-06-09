# -*- coding: utf-8 -*-
"""simphysiclab_ldr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KpayN8S1upxnwpr-v3RrgGGA_38xu9cg
"""

# Commented out IPython magic to ensure Python compatibility.
#Clonar github con los repositorios
#!wget {f"https://raw.githubusercontent.com/SIMPHYSICLAB/simphysiclab/main/libraries/simphysiclab_sistemas.py"}
import simphysiclab_sistemas as SIS

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

"""# **FUNCIONES PARA LA REPRESENTACION DEL LUGAR DE LAS RAICES**"""

def checkIfIsLDR(ax,ceros,polos):
  c=np.concatenate((ceros,polos))
  c=np.insert(c,0, c[0]-10)

  for index in range(0,len(c)-1):
      deletelist=c
      if sum(((c[index].real-c[index+1].real)/2+c[index+1].real)<deletelist.real)%2==1:
        ax.plot([int(c[index].real),int(c[index+1].real)], [0,0],
            linewidth=4.0,
            linestyle='-',
            color='b',
            alpha=0.5,
            marker='o')

def dibujarAsintotas(ax,ceros,polos):
  k=len(polos)-len(ceros)
  q = sympy.symbols('k')
  ia=(sum(polos)-sum(ceros))/(len(polos)-len(ceros))
  print(str(180*(2*q+1)/(len(polos)-len(ceros)))+ "%, para k>0, donde k= 0,+1,+2,+3,...")
  for i in range(0,k):
    print("k=",i,", ",(180*(2*i+1)/(len(polos)-len(ceros))),"%")
    angle=(180*(2*i+1)/(len(polos)-len(ceros)))  
    phi = np.deg2rad(angle)
    L = np.array([0, 10])
    px =  ia.real+np.cos(phi) * L[1]
    py =  np.sin(phi) * L[1]
    ax.plot([ia.real,round(px)], [0,py],'--')

def angleDefinition(diffTargetSource):
  if type(diffTargetSource)!=complex:
    diffTargetSource=complex(diffTargetSource,0)

  if diffTargetSource.real>=0 and diffTargetSource.imag>=0:
    #print("PrimerCuadrante")
    return math.degrees(math.atan2(diffTargetSource.imag, diffTargetSource.real))
  elif diffTargetSource.real<0 and diffTargetSource.imag>=0:
    #print("SegundoCuadrante")
    return math.degrees(math.atan2(diffTargetSource.imag, diffTargetSource.real))
  elif diffTargetSource.real<0 and diffTargetSource.imag<0:
    #print("TercerCuadrante")
    return math.degrees(math.atan2(diffTargetSource.imag, diffTargetSource.real))
  elif diffTargetSource.real>=0 and diffTargetSource.imag<0:
    #print("CuartoCuadrante")
    return math.degrees(math.atan2(diffTargetSource.imag, diffTargetSource.real))

def checkIfPointIsLDR(ceros,polos,point):
  angulos=0;
  angulosCum=[]
  for cp in polos:
    angle=angleDefinition(point-cp)
    angulosCum.append(angle)
    angulos-=angle
  for cp in ceros:
    angle=angleDefinition(point-cp)
    angulosCum.append(angle)
    angulos+=angle
  if abs(round(angulos))!=0 and abs(round(angulos))==180:
    return True
  else:
    return False

"""ESTA HA SUFRIDO VARIACIONES HAY QUE REVISAR"""

def symbolRouth(pol_den):
  s = sympy.Symbol('s')
  den=0
  i=0
  exponente=len(pol_den)-1
  for num in pol_den:
    if i==len(pol_den)-1:
      if type(num)!= type(s):
        den = den + float(num)
      else:
        den = den + num
    else: 
      if type(num)!= type(s):
        den = den + float(num)*s**exponente
      else:
        den = den + num*s**exponente
    i+=1
    exponente-=1
  return den,s

"""EN ESTA HAY QUE FORZAR A QUE SEA CONTROL, REVISAR"""

def rupturaOingreso(TF):
  s = control.tf('s')
  num,s=symbolRouth(TF.num[0][0])
  den,s=symbolRouth(TF.den[0][0])
  derivative = sympy.diff(-(den/num),s)
  solutionsRoot=sympy.solve(derivative)
  return solutionsRoot

def LDR_Automatico(ax,TF,xmax,ymax,maxK=0,stepK=0.01):
  num,den,gain=SIS.InfoTF("num_den",TF)
  TF=SIS.CrearTF("num_den",num,den)
  if maxK==0:
    if ax!=None:
      rlist, klist = control.root_locus(TF,grid=False,xlim=[-xmax[0],xmax[1]],ylim=[-ymax[0],ymax[1]],ax=ax,print_gain =False)
    else:
      rlist, klist = control.root_locus(TF,grid=False,xlim=[-xmax[0],xmax[1]],ylim=[-ymax[0],ymax[1]],print_gain =False)
  else:
    if ax!=None:
      rlist, klist = control.root_locus(TF,np.arange(0, maxK, stepK),grid=False,xlim=[-xmax[0],xmax[1]],ylim=[-ymax[0],ymax[1]],ax=ax,print_gain =False)
    else:
      rlist, klist = control.root_locus(TF,np.arange(0, maxK, stepK),grid=False,xlim=[-xmax[0],xmax[1]],ylim=[-ymax[0],ymax[1]],print_gain =False)
  return rlist, klist

def manualLDR(ceros,polos,maxX,maxY,step):
  x=[]
  y=[]
  for iX in np.arange(-maxX, maxX+step, step):
    for iY in np.arange(-maxY, maxY+step, step):
      x.append(iX)
      y.append(iY)
  x = np.array(x)
  y = np.array(y)
  x,y=regTrans_areaIntersectionWithPoints(None,x,y,40,40,theta,Wd,None)
  maxPoint=[]
  for i in range(len(x)):
    if checkIfPointIsLDR(ceros,polos,complex(x[i],y[i]))==True:
      if y[i]==maxY:
        return -1

def criterioModulo(polosnew,polos,ceros,gain):
  polosden=1;
  cerosnum=1;
  for cp in polos:
    diff=cp-polosnew
    polosden*=sqrt(pow(diff.real, 2)+pow(diff.imag, 2))
  for cp in ceros:
    diff=cp-polosnew
    cerosnum*=sqrt(pow(diff.real, 2)+pow(diff.imag, 2))
  return polosden/(cerosnum*gain)#ERROR, PONER PARAMETRO GAIN