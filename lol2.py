import numpy as np
from copy import deepcopy
from PIL import Image
from numpy import savetxt
import matplotlib.pyplot as plt
import os.path


fs=5 # factor de escala 
tu=400 # dimensiones del universo (mm) 
diamplac=260 # diametro placa (mm)
dis=3 # distancia entre las placas (mm)
it=100 # número de iteraciones
Ep=0.001

vv=tu/fs
t=int(vv) 
if t/2-int(t/2)==0:      # para asegurarnos que sea un matriz impar, así seleccionamos más facil  el centrp 
   t=t+1
fs=tu/t

uni=np.zeros((t,t)) # la matriz cuadrada del sistema
dis=round((dis/2)/fs, 0) # distancia entre el punto medio y un extremo de la placa 
UDSetupP=((dis+2*dis/0.5),(diamplac+2*diamplac/2))
psup=(t/2)-dis+0.5-1 # placa superior
pinf=(t/2)+dis+0.5-1 # placa inferior 
lado=round((diamplac/2)/fs,0) # numero de nodos en los cuales sus valores estan libres en los lados por la fila de las placas 

k=1 
for x in range(t):                        # En este parte del codigo definimos
   for y in range(t):                     # el voltaje asociada a esa placa 
        if x==psup :
            if y>=(t/2+0.5-lado-1) and y<=(t/2+0.5+lado-1):
                if k==0:
                    print(y)
                uni[x,y]=100
p=1
s=1
l=1
w=0
uni2=deepcopy(uni)
for c in range(it):
    w=w+1                                           # en esta parte definimos la suma de los 4 compnentes... 
    if w>=2:                                        # ...para definir el potencial electrico en ese punto a partir del número de iteraciones 
     uni=deepcopy(uni2)                
    for a in range(t):
        for b in range(t):            
         if b>=(t/2+0.5-lado-1) and b<=(t/2+0.5+lado-1) and (a==psup or a==pinf):
             p=0
         if a==0 or b==0 or b==t-1 or a==t-1:
             p=0
         if (p!=0 and s!=0 and l!=0):
             uni2[a,b]=(uni[a+1,b]+uni[a-1,b]+uni[a,b+1]+uni[a,b-1])/4
         p=1
         s=1
         l=1
         
         
comx=np.zeros((t,t)) # inicializamos la matriz,con el mismo tamaño pero con ceros 
comy=np.zeros((t,t)) # inicializamos la matriz,con el mismo tamaño pero con ceros         
for a in range(t):
    for b in range(t):
        if b>=(t/2+0.5-lado-1) and b<=(t/2+0.5+lado-1) and (a==psup or a==pinf):
             p=0
        if a==0 or b==0 or b==t-1 or a==t-1:             # en esta parte nos entega los compnenetes de x y Y...
             p=0                                         # ...en las matrices correspondinetes 
        if (p!=0 and l!=0):
             comx[a,b]=(uni2[a+1,b]-uni2[a-1,b])/(2*fs*1000) 
             comy[a,b]=(uni2[a,b+1]-uni2[a,b-1])/(2*fs*1000)             
        p=1
        l=1
#visualizamos el resultado de las matrices       
print(uni2)
print(comx)
print(comy)


## almacenamos los datos 
StringSave='capacitor100.csv'

StringSave=StringSave.replace('2',str(dis))
StringSave=StringSave.replace('0.05',str(Ep*100))
StringSave=StringSave.replace('100',str(abs(100-0)))
                                                           
savetxt(StringSave, uni, delimiter=',')
savetxt(StringSave, comx, delimiter=',')
savetxt(StringSave, comy, delimiter=',')
