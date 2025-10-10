# %%
import matplotlib.pyplot as plt
import numpy as np
def f(x):
  return (2*(x**7))-(x**4)+(3*(x**2))+4

res=100

x=np.linspace(-10.0,10.0,num=res)
y=f(x)

fig, ax = plt.subplots()
ax.plot(x,y)
ax.grid()
ax.axhline(y=0, color="red")
ax.axvline(x=0, color="red")
plt.xlim([-5, 5])
plt.ylim([0, 10])





# %%
def f(x):
  return np.cos(x)

res=100

x=np.linspace(-10.0,10.0,num=res)
y=f(x)

fig, ax = plt.subplots()
ax.plot(x,y)
ax.grid()
ax.axhline(y=0, color="red")
ax.axvline(x=0, color="red")


# %%
def f(x):
  return np.e**x

res=100

x=np.linspace(-10.0,10.0,num=res)
y=f(x)

fig, ax = plt.subplots()
ax.plot(x,y)
ax.grid()
ax.axhline(y=0, color="red")
ax.axvline(x=0, color="red")


# %%
def f(x):
  return np.log2(x)

res=100

x=np.linspace(0.01,64.0,num=res)
y=f(x)

fig, ax = plt.subplots()
ax.plot(x,y)
ax.grid()
ax.axhline(y=0, color="red")
ax.axvline(x=0, color="red")


# %%
def f(x):
  y=np.zeros(len(x))
  for idx,x in enumerate(x):
    if x>=0:
      y[idx]=1.0
  return y
res=1000

x=np.linspace(-20.0,10.0,num=res)
y=f(x)

fig, ax = plt.subplots()
ax.plot(x,y)
ax.grid()



# %% [markdown]
# ## Desplazamientos verticales y horizontales
# 
# Siendo $c$ una constante mayor que cero, entonces la gráfica:
# 
# - $y=f(x)+c$ se desplaza $c$ unidades hacia arriba.
# - $y=f(x)-c$ se desplaza $c$ unidades hacia abajo.
# - $y=f(x-c)$ se desplaza $c$ unidades hacia la derecha.
# - $y=f(x+c)$ se desplaza $c$ unidades hacia la izquierda.

# %%
N=1000
def f(x):
  return x**2;

c=2
x=np.linspace(-5,5,num=N)
y=f(x+c)-c
fig,ax=plt.subplots()
ax.plot(x,y)
ax.grid()
ax.axhline(y=0, color="red")
ax.axvline(x=0, color="red")

# %% [markdown]
# ## Alargamientos y compresiones
# 
# Siendo $c$ una constante mayor que cero, entonces la gráfica:
# 
# - $y=c \cdot f(x)$ alarga la gráfica verticalmente en un factor de $c$.
# - $y= \frac{1}{c} \cdot f(x)$ comprime la gráfica verticalmente en un factor de $c$.
# - $y=f(c \cdot x)$ comprime la gráfica horizontelmente en un factor de $c$.
# - $y= f(\frac{1}{c} \cdot x )$ alarga la gráfica horizontelmente en un factor de $c$.

# %%
N=1000
def f(x):
  return np.sin(x);

c=3
x=np.linspace(-15,15,num=N)
y=f(2*x)
fig,ax=plt.subplots()
ax.plot(x,y)
ax.grid()
ax.axhline(y=0, color="red")
ax.axvline(x=0, color="red")

# %% [markdown]
# ## Reflexiones
# 
# - $y=-f(x)$ refleja la gráfica respecto al eje x.
# - $y=f(-x)$ refleja la gráfica respecto al eje y.

# %%
N=1000
def f(x):
  return x**3;


x=np.linspace(-10,10,num=N)
y=f(x)
fig,ax=plt.subplots()
ax.plot(x,y)
ax.grid()
ax.axhline(y=0, color="red")
ax.axvline(x=0, color="red")

# %%
from matplotlib import cm # Para manejar colores
import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
  return np.sin(x) + 2*np.cos(y)


res = 100

x = np.linspace(-4, 4, res)
y = np.linspace(-4, 4, res)

x, y = np.meshgrid(x, y)

z = f(x,y)
# Gráficar la superficie
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(x, y, z, cmap=cm.cool)
fig.colorbar(surf)

# %% [markdown]
# Curvas de nivel

# %%
fig2, ax2 = plt.subplots()
level_map=np.linspace(np.min(z),np.max(z),num=res)

cp= ax2.contourf(x,y,z,levels=level_map,cmap=cm.cool)
fig2.colorbar(cp)

# %%
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# Descenso del gradiente

# %% [markdown]
# Grafica en 3d de nuestra funcion de coste

# %%
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(subplot_kw={"projection":"3d"})
def f(x,y):
  return np.sin(x)+2*np.cos(x)
res=100
x = np.linspace(-4,4, res)
y = np.linspace(-4,4, res)
X,Y = np.meshgrid (x,y)
Z=f(X,Y)
surf = ax.plot_surface(X,Y,Z, cmap=cm.cool)
fig.colorbar(surf)


# %% [markdown]
# Descenso del gradiente

# %%
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt

level_map=np.linspace(np.min(Z),np.max(Z), res)
plt.contourf(X,Y,Z, levels=level_map,cmap=cm.cool)
plt.colorbar()
plt.title("Descenso del gradiente")

p=np.random.rand(2) * 8 - 4
plt.plot(p[0], p[1],"o", c="k")

h=0.01
lr=0.01

def derivate(_p,p):
  return  (f(_p[0],_p[1]) - f(p[0],p[1])) / h

def gradient(p):
  grad=np.zeros(2)
  for idx, val in enumerate(p):
    cp=np.copy(p)
    cp[idx]=cp[idx]+h

    dp=derivate(cp, p)
    grad[idx]=dp
  return grad

for i in range(100):
  p= p - lr*gradient(p)
  if(i%10==0):
    plt.plot(p[0], p[1],"o", c="r")

plt.plot(p[0],p[1],"o",c="w")
print(p)


