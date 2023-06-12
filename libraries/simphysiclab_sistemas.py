# -*- coding: utf-8 -*-
"""simphysiclab_sistemas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J87TCBlMko2JhAoYIjqFv4BfJ4CI6Guo
"""

# Commented out IPython magic to ensure Python compatibility.
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

"""# **FUNCIONES PARA LA GENERACION Y REPRESENTACION DEL SISTEMA**

TIPO DE LA FUNCION
"""

def libraryType(TF):
  return type(TF).__module__.split('.')[0]

"""YA NO SE UTILIZA"""

def libraryDetection(TF):
  if type(G).__module__.split('.')[0]=="sympy":
    return 1
  else:
    return 0

"""TIPO DE LA FUNCION ATENDIENDO A OTROS PARAMETROS"""

def checkIfTFParameter(TF):
  if libraryType(TF)=="sympy":
    symbolappearance=[]
    num,den,gain=InfoTF("num_den",TF)
    return checkIfParameter(num,den)
  else:
    return "other"

def checkIfParameter(num,den):
  symbolappearance=[]
  for i in np.concatenate((num, den), axis=0):
      try:
        testrealnumber=float(i)
        symbolappearance.append(0)
      except:
        symbolappearance.append(1)
  if symbolappearance.count(1)>0:
    return "sympy"
  else:
    return "other"

#Crear funcion de transfercia generica ya sea G o H
def CrearTF(tipo,num,den,simbol=0):
  if tipo=="num_den":
    symbolappearance=[]
    #Comprobar si contiene algun simbolico la expresión
    for i in np.concatenate((num, den), axis=0):
      try:
        testrealnumber=float(i)
        symbolappearance.append(0)
      except:
        symbolappearance.append(1)

    #Contiene simbolicos#La expresión simbolica no se puede simplificar
    if (symbolappearance.count(1)!=len(np.concatenate((num, den), axis=0)) and symbolappearance.count(1)>0) or (simbol==1):
      s = sympy.Symbol('s')
      return sympy.factor(sympy.simplify(sympy.Poly(num, s)/sympy.Poly(den, s)))
    #Contiene simbolicos#Se puede simplificar la expresión simbolica
    elif symbolappearance.count(1)==len(np.concatenate((num, den), axis=0)) and symbolappearance.count(1)>0:
      numwithoutParameter=[]
      denwithoutParameter=[]
      for i in num:
        if len(i.atoms(sympy.Number))==0:
          numwithoutParameter.append(float(1))
        else:
          numwithoutParameter.append(float(i.atoms(sympy.Number).pop()))
      for i in den:
        if len(i.atoms(sympy.Number))==0:
          denwithoutParameter.append(float(1))
        else:
          denwithoutParameter.append(float(i.atoms(sympy.Number).pop()))

      return control.tf(numwithoutParameter, denwithoutParameter)
    #No contiene simbolicos
    else: 
      #Este cast es por si simpy guarda los valores en un formato distinto de float
      numcastfloat=[]
      dencastfloat=[]
      for i in num:
        numcastfloat.append(float(i))
      for i in den:
        dencastfloat.append(float(i))
      #Crear la función de transferencia con los valores guardados en formato float
      return control.tf(numcastfloat, dencastfloat)
  elif tipo =="ceros_polos":
    if checkIfParameter(num,den)=="sympy":
      print("Error")
      return "Error."
    else:
      if simbol==0:
        s = control.tf('s')
        numcp = 1
        dencp = 1
        if len(num)==0 and len(den)==0:
          TF=control.tf(1, 1)
        else:
          for i in range(len(num)):
            numcp = numcp * (s + num[i])
          for j in range(len(den)):
            dencp = dencp * (s + den[j])
          TF=numcp/dencp
      elif simbol==1:
        s=sympy.symbols('s')
        numcp = 1
        dencp = 1
        if len(num)==0 and len(den)==0:
          TF=sympy.factor(numcp/dencp)
        else:
          for i in range(len(num)):
            numcp = numcp * (s + num[i])
          for j in range(len(den)):
            dencp = dencp * (s + den[j])
          TF=sympy.factor(numcp/dencp)
    
    return TF

#Recibir información
def InfoTF(tipo,TF):
  if tipo=="num_den":
    num=[]
    den=[]
    
    if libraryType(TF)=="sympy":
      n,d = sympy.fraction(TF)
      num=sympy.Poly(n, sympy.symbols('s')).coeffs()
      den=sympy.Poly(d, sympy.symbols('s')).coeffs()

      gain=num[0]
      denCoeff=den[0]

      numSimplify=[]
      denSimplify=[]
      
      for i in num:
        numSimplify.append(i/gain)
      for i in den:
        denSimplify.append(i)
      return numSimplify,denSimplify,gain
    #No simbolico
    else:

      gain=TF.num[0][0][0]

      for i in TF.num[0][0]:
        num.append(i.real/gain)
      for i in TF.den[0][0]:
        den.append(i.real)
      return num,den,gain
  #No permite simbolico
  elif tipo =="ceros_polos":
    if libraryType(TF)=="sympy":
      gain=TF.num[0][0][0]
      n,d = sympy.fraction(TF)
      num=sympy.Poly(n, sympy.symbols('s'))
      den=sympy.Poly(d, sympy.symbols('s'))
      ceros=solve(num,sympy.symbols('s'))
      polos=solve(den,sympy.symbols('s'))
      return ceros,polos,gain
    else:
      gain=TF.num[0][0][0]
      ceros=TF.zeros()
      ceros=[np.round(i,8) for i in ceros]
      polos=TF.poles()
      polos=[np.round(i,8) for i in polos]
      return ceros,polos,gain

#Sistema de retroalimentación M, a partir de G H y k
def TFSymtem(G,H,k=1):
  #if checkIfTFParameter(G)=="sympy" and checkIfTFParameter(H)=="sympy":#Este if hace que si las dos funciones de transferencia tengan sympy salte error
  #  return "Error. Only one function with k and the k parameter"
  #else:
    if (checkIfTFParameter(G)=="sympy" or checkIfTFParameter(H)=="sympy") and libraryType(k)=="sympy":
      num,den,gain=InfoTF("num_den",G)
      numk=[]
      for i in num:
        numk.append(i*k)
      G=gain*CrearTF("num_den",numk,den)#!!!EDUARDO
      H,num,den,gain=InfoTF("num_den",H)
      H=gain*CrearTF("num_den",num,den,1)#!!!EDUARDO
      M=(G/(1+(G*H)))
      M=sympy.simplify(M)
      return M
    elif (checkIfTFParameter(G)=="sympy" or checkIfTFParameter(H)=="sympy") and libraryType(k)!="sympy":
      num,den,gain=InfoTF("num_den",G)
      numk=[]
      for i in num:
        numk.append(i*k)
      G=gain*CrearTF("num_den",numk,den,1)#!!!EDUARDO
      num,den,gain=InfoTF("num_den",H)
      H=gain*CrearTF("num_den",num,den,1)#!!!EDUARDO
      M=(G/(1+(G*H)))
      M=sympy.simplify(M)
      return M
    elif (checkIfTFParameter(G)!="sympy" and checkIfTFParameter(H)!="sympy") and libraryType(k)=="sympy":
      num,den,gain=InfoTF("num_den",G)
      numk=[]
      for i in num:
        numk.append(i*k)
      G=gain*CrearTF("num_den",numk,den,1)#!!!EDUARDO
      num,den,gain=InfoTF("num_den",H)
      H=gain*CrearTF("num_den",num,den,1)#!!!EDUARDO
      M=(G/(1+(G*H)))
      M=sympy.simplify(M)
      return M
    elif (checkIfTFParameter(G)!="sympy" and checkIfTFParameter(H)!="sympy") and libraryType(k)!="sympy":
      numG,denG,gainG=InfoTF("num_den",G)
      numH,denH,gainH=InfoTF("num_den",H)
      if libraryType(G)=="sympy" and libraryType(H)=="sympy":
        G=gainG*CrearTF("num_den",numG,denG,1)#!!!EDUARDO
        H=gainH*CrearTF("num_den",numH,denH,1)#!!!EDUARDO
        M=(G/(1+(G*H)))
        M=sympy.simplify(M)
      else:
        G=gainG*CrearTF("num_den",numG,denG)#!!!EDUARDO
        H=gainH*CrearTF("num_den",numH,denH)#!!!EDUARDO
        K_G=control.series(k,G)
        M=control.feedback(K_G,H)
        ceros,polos,gain=InfoTF("ceros_polos",M)
      return M
    #elif checkIfTFParameter(G)=="sympy" and checkIfTFParameter(H)=="sympy" and libraryType(k)=="sympy":
    #  return "Error. Only one function with k and the k parameter"

def EstabilidadDelSistema(G):
  if checkIfTFParameter(G)=="sympy"
    ceros_G=control.zero(G)
    polos_G=control.pole(G)
    ceros_G=[round(i,2) for i in ceros_G]
    polos_G=[round(i,2) for i in polos_G]
    EstableInestable=0
    for i in polos_G:
      if i.real>=0:
        if EstableInestable==0:
          print("Sistema Inestable")
          EstableInestable=1
        print("Polo inestable en:")
        print(i)
    if EstableInestable==0:
      print("Sistema Estable")
  else:
    print("La estabilidad con esta función solo se puede estudiar sin parametros variables.")

def pintar_Funcion(ax,ceros,polos):
  for i in range(len(polos)) :
    ax.scatter(polos[i].real, polos[i].imag, s=200,c='r', marker="x")
  for j in range(len(ceros)) :
    ax.scatter(ceros[j].real, ceros[j].imag, s=200,c='b', marker="o")

def tpParemeter(tp):
  if tp!=None:
    wd=math.pi/tp
  return wd

def tsParemeter(ts):
  if ts!=None:
    sgm=math.pi/ts
  return sgm

def MpParemeter(Mp):
  if Mp!=None:
    Mp=Mp/100
    theta=np.arctan(-math.pi/np.log(Mp))
  return theta

def restriccionTp(ax,Wd,maxX,maxY):
  if Wd!=None:
    x21 = [0, 0, -maxX, -maxX]
    y21 = [maxY, Wd, Wd, maxY]
    x22 = [0, 0, -maxX, -maxX]
    y22 = [-maxY, -Wd, -Wd, -maxY]
  else:
    x21 = [-maxX,0,0,-maxX]
    y21 = [maxY,maxY,-maxY,-maxY]
    x22 = [-maxX,0,0,-maxX]
    y22 = [-maxY,-maxY,-maxY,-maxY]
  if ax!=None:
    ax.fill(x21,y21,alpha=0.3,color='green',hatch='|')
    ax.fill(x22,y22,alpha=0.3,color='green',hatch='|')
  return x21,y21

def restriccionTs(ax,sgm,maxX,maxY):
  if sgm!=None:
    x3= [-maxX,-sgm,-sgm,-maxX]
    y3= [maxY,maxY,-maxY,-maxY]
  else:
    x3= [-maxX,0,0,-maxX]
    y3= [maxY,maxY,-maxY,-maxY]
  if ax!=None:
    ax.fill(x3,y3,alpha=0.3,color='orange',hatch='|')
  return x3,y3

def restriccionMp(ax,theta,maxX,maxY):
  if theta!=None:
    x1 = [-maxX * math.cos(theta), 0,0, -maxX * math.cos(theta)]
    y1 = [-maxY * math.sin(theta), 0,0,  maxY * math.sin(theta)]
  else:
    x1 = [-maxX,0,0,-maxX]
    y1 = [maxY,maxY,-maxY,-maxY]
  if ax!=None:
    ax.plot(x1, y1, c='brown', ls='--', lw=1, alpha=1)
    ax.fill(x1, y1, alpha=0.2, color='r', hatch='/')
  return x1,y1

def determina_orden(TF):
  num,den,gain=InfoTF("num_den",TF)
  orden=len(den)-1
  return orden

#!!!!!!!!!HABLAR CON EDUARDO NO ME GUSTA LO DE LA GANANCIA, PORQUE TE TOCA TODO EL RATO MULTIPLICARLO
def regPermanent(G,H):
  #Convertir a funcion transferencia tipo sympy
  num,den,gain=InfoTF("num_den",G)
  G=CrearTF("num_den",num,den,1)
  G=gain*G
  num,den,gain=InfoTF("num_den",H)
  H=CrearTF("num_den",num,den,1)
  H=gain*H
  #Se multiplica por el simbolo s y se calcula el limite en 0
  s = sympy.Symbol('s')
  Merrp=G*H
  Merrv=s*G*H
  Merra=s*s*G*H
  #Se calcula el error en regimen permanente para cada tipo de error
  return [Merrp.subs(s, 0), 1/(1+Merrp.subs(s, 0))] , [Merrv.subs(s, 0), 1/(Merrv.subs(s, 0))] ,[Merra.subs(s, 0), 1/(Merra.subs(s, 0))]

def pintar_ejes(ax,step,xmax,ymax):
  xmin=-xmax
  ymin=-ymax
  ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')
  # Establecemos en 0,0 el origen del eje de coordenadas para representar
  # las marcas de la escala de los ejes
  ax.spines['bottom'].set_position('zero')
  ax.spines['left'].set_position('zero')
  # Borramos las marcas en un lado de la grafica para mejorar el diseño
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  # Escribimos el nombre de cada ejes
  ax.set_xlabel('Real', size=14, labelpad=-24, x=1.03)
  ax.set_ylabel('Im', size=14, labelpad=-21, y=1.02, rotation=0)
  # Creamos las marcas principales personalizadas para determinar la posición 
  # de las etiquetas de cada marca
  ticks_frequency = step
  x_ticks = np.arange(xmin, xmax+1, ticks_frequency)
  y_ticks = np.arange(ymin, ymax+1, ticks_frequency)
  ax.set_xticks(x_ticks[x_ticks != 0])
  ax.set_yticks(y_ticks[y_ticks != 0])  
  # Creamos las marcas menores colocadas en cada entero para habilitar el dibujo de 
  # las líneas de cuadrícula menores: tenga en cuenta que esto no tiene efecto en 
  ax.set_xticks(np.arange(xmin, xmax+1), minor=True)
  ax.set_yticks(np.arange(ymin, ymax+1), minor=True)  
  # Dibujamos las lineas de la cuadrícula
  ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
  # Dibujamos las flechas
  arrow_fmt = dict(markersize=4, color='black', clip_on=False)
  ax.plot((1), (0), marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
  ax.plot((0), (1), marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)

#Valor final, maximo, tiempo establecimiento
def pintar_parametros_grafica(ax,y,t):
  b=y[len(t)-1]
  a=max(y)-b
  errp=1-y[len(t)-1]

  
  ax.plot([0, 0], [0, y[len(t)-1]], c='green', ls='--', lw=1, alpha=1)
  ax.annotate('b=%s'%round(b,3),(0,b/2),(0,b/2))
  ax.plot([0, 0], [y[len(t)-1], max(y)], c='blue', ls='--', lw=1, alpha=1)
  ax.annotate('a=%s'%round(a,3),(0,b+a/2),(0,b+a/2))
  ax.annotate('a+b=%s'%round(a+b,3),(0,b+a),(0,b+a))
  ax.annotate('vf=%s'%round(b,3),(t[len(t)-1],b),(t[len(t)-1],b))
  
  print("Sobreoscilacion: ",100*(a/b),"%")
  print("Errp: ",errp)
  print("b: ",b)
  print("a: ",a)
  print("valor final: ",b)
  print("max: ",a+b)
  if a>0:

    tp=t[np.argmax(y)]
    print("tp: ",tp,"s")
    ax.annotate('tp=%s s'%round(tp,3),(tp,0.1),(tp,0.1))
    ax.plot([0, tp], [y[len(t)-1], y[len(t)-1]], c='red', ls='--', lw=1, alpha=1)
    ax.plot([0, tp], [a+b, a+b], c='b', ls='--', lw=1, alpha=1)
    ax.plot([tp, tp], [0, y[np.argmax(y)]], c='red', ls='--', lw=1, alpha=1)
    ax.plot([tp, t[len(t)-1]], [y[len(t)-1], y[len(t)-1]], c='black', ls='--', lw=1, alpha=1)
  else:
    pto_y=0.632*np.max(y)
    round_pto_y=round(pto_y,5)
    round_K=round(np.max(y),5)
    for i in range(len(y)):
      if pto_y-y[i]<0:
        ts=t[i-1] 
        break
    ax.annotate('T=%s s'%round(ts,3),(ts,pto_y-0.1),(ts,pto_y-0.1))
  #return [100*(a/b),a,b,tp,ts,errp]

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