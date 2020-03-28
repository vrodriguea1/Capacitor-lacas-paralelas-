from numpy import asarray
from numpy import savetxt
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np
from PIL import Image
from copy import copy, deepcopy
from numpy import loadtxt
from scipy import interpolate
import pylab as py

StringLoad='capacitor100.csv'


fs=5 # factor de escala 
tu=400 # dimensiones del universo (mm) 
diamplac=260 # diametro placa (mm)
dis=3 # distancia entre las placas (mm)
it=1000# número de iteraciones
Ep=0.001  # error permitido  
Eo=8.8541878128*10**(-12) # permitividad en el vacio 

# se le asigan variables para armar un cudrado en donde va a estar el capacitor
ymin=0    
ymax=0
xmi1=0
xma1=0
xmi2=0
xma2=0

## los siguientes comandos son comandos anteriormente establecidos 
vv=tu/fs
t=int(vv) 
if t/2-int(t/2)==0: 
   t=t+1
fs=tu/t


uni=np.zeros((t,t)) # la matriz cuadrada del sistema
dis=round((dis/2)/fs, 0) # distancia entre el punto medio y un extremo de la placa 
mdd=((dis+2*dis/0.5),(diamplac+2*diamplac/2))
psup=(t/2)-dis+0.5-1 # placa superior
pinf=(t/2)+dis+0.5-1 # placa inferior 
lado=round((diamplac/2)/fs,0) 
borx=len(uni[0]) # parte sup x
bory=len(uni)   # parte supy
px=round(borx/2) # inicio en x
yy=round(bory/2) # inicio en y 
Grad=1  # condicion para iniciar el calculo del gradiente 

# definimos los limites del sistema 
lol=0
for y in range(bory):
    for x in range(borx):
     
       if (uni[y][x]==0 and lol==0):
            lol=1                                                               
            ymin=y                                                               
            xmi1=x                                                             
        elif (y==ymin and x>=xmin1 and uni[y][x]==1 and lol==1):
            xma1=x-1
            lol=2
        elif (uni[y][x]==0 and y!=ymin and lol==2):
            ymax=y
            xmi2=x
            lol=3
        elif (y==ymax and x>=xmin2 and uni[y][x]==1 and lol==3):
            xma2=x-1
            lol=4
            
if(xmi1==xmi2 and xma1==xma2):
    Yb= ymin
    Ya= ymax
    Xmi= xmi1
    Xma= xma1
    

uni= loadtxt(StringLoad, delimiter=',')
comy= loadtxt(StringLoad, delimiter=',')
comx= loadtxt(StringLoad, delimiter=',') 

if  (Grad==1):
    Vgrad= np.gradient(uni)    # en este parte vamos a calcular la capacitancia 
    comx= -Vgrad[1]*(10**3)   
    comy= -Vgrad[0]*(10**3)
   
    z=0
    Q=0
    while (z!=Xma):     # sacamos la carga mulplicando el gradiente negativo del potencial por las componentes en los que esta ubcado 
     Capacitancia= Q +(((comx[Ya-1][Xmin+z])**2 +(comy[Yb-1][Xmin+z])**2)**0.5)*(1/fs)*Eo
       z=z+1
    #Capacitancia en nF
    Capacitancia= (Capacitancia/(100-0))*10**(9) 
    print('Capacitancia [nF]=') 
    print(Capacitancia)
    
# en esta parte se realizara las..
# ..gráficas y visualización de los datos 
Emagnitude=np.power(matx,3)+np.power(maty,3)
Emagnitude=np.power(Emagnitude,0.7)
      
mdd=(int(mdd[0]),int(mdd[1]))

# cuadricula para los ejes 
px= fs*mdd[1],
py=  fs*mdd[0]
x= np.linspace(0, mdd[1], px)
y= np.linspace(0, mdd[0], py)
X, Y= np.meshgrid(x, y)


fx = interpolate.interp2d(x, y, matx, kind='cubic')
fy = interpolate.interp2d(x, y, maty, kind='cubic')

# gráfica líneas equipotenciales 
breaks=np.linspace(100, 0 ,21)
plt.figure(figsize=(7,9))
bb = plt.contourf(X, Y, uni, breaks, cmap='seismic' )
plt.colorbar(ticks=breaks, orientation= 'vertical')
plt.xlabel(' [mm]')    
plt.ylabel(' [mm]')
plt.title('LÍNEAS EQUIPOTENCIALES [V].')         


# gráfica de las líneas de campo eléctrico
fig1=plt.figure(figsize=(7,9))      
ax = fig1.add_subplot(1, 1, 1) 
r1 = plt.Rectangle((Xmin, Y_a), diamplac, 1/fs, color='g', alpha=0.5)   
r2 = plt.Rectangle((Xmin, Y_b), diamplac, 1/fs, color='g', alpha=0.5)     
plt.streamplot(X, Y, fx(x,y), fy(x,y), color=Emagnitude, density=[1,100], cmap=plt.cm.jet) 
plt.xlabel('[mm]')    
plt.ylabel('[mm]')
plt.title('LÍNEAS DE CAMPO ELÉCTRICO [V/m]')     
plt.colorbar(orientation= 'vertical')
ax.add_patch(r1)
ax.add_patch(r2)

