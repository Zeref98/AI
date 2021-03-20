# coding: utf-8

# In[278]:


#lista de opciones
options = ["piedra", "tijeras", "papel"]


# In[279]:


#definicion de una funcion
def search_winner(p1, p2):
    if p1 == p2:
        result = 0
    
    elif p1 == "piedra" and p2 == "tijeras":
        result = 1
    elif p1 == "piedra" and p2 == "papel":
        result = 2
    elif p1 == "tijeras" and p2 == "piedra":
        result = 2
    elif p1 == "tijeras" and p2 == "papel":
        result = 1
    elif p1 == "papel" and p2 == "piedra":
        result = 1
    elif p1 == "papel" and p2 == "tijeras":
        result = 2
        
    return result


# In[280]:


#ejemplo
search_winner("papel", "papel")


# In[281]:


#Se crea una lista 
test = [
    ["piedra", "piedra", 0],
    ["piedra", "tijeras", 1],
    ["piedra", "papel", 2]
   
]
#iteracion de las listas de test usando un for 
for partida in test:
    print("player1: %s player2: %s Winner: %s Validation: %s" % (
        partida[0], partida[1], search_winner(partida[0], partida[1]), partida[2]
    ))


# In[282]:


#importamos la libreria Random choice --secuencia
from random import choice
#Definimos el metodo choice y le enviamos options con los 
#3 parametros el metodo retorna de forma aleatoria 1
def get_choice():
    return choice(options)


# In[283]:


#utilizamos un for con la funcion range con el fin de definir
#el numero de iteraciones
for i in range(12):
    player1 = get_choice()
    player2 = get_choice()
    print("player1: %s player2: %s Winner: %s " % (
        player1, player2, search_winner(player1, player2)
    ))


# In[284]:


#funcion para convertir los string en una lista de 0 y 1
def str_to_list(option):
    if option=="piedra":
        res = [1,0,0]
    elif option=="tijeras":
        res = [0,1,0]
    else:
        res = [0,0,1]
    return res
#se crea una lista de datos y se guarda en data_x y data_y
#data x corresponde a lo que elige el jugador 1
data_X = list(map(str_to_list, ["piedra", "tijeras", "papel"]))
#data y corresponde a la eleccion ganadora con relacion a lo seleccionado
#por el jugador 1
data_y = list(map(str_to_list, ["papel", "piedra", "tijeras"]))
#map(funcion, secuencia) llama a funcion(item) por cada uno de los ítems de la secuencia y
#devuelve una lista de los valores retornados
print(data_X)
print(data_y)


# In[285]:


from sklearn.neural_network import MLPClassifier


# In[286]:



clf = MLPClassifier(verbose=False, warm_start=True)


# In[287]:


#al modelo lo entrenamos enseñandole un valor
model = clf.fit([data_X[1]], [data_y[1]])
print(model)


# In[288]:


def play_and_learn(iters=10, debug=False):
    score = {"win": 0, "loose": 0}
    
    data_X = []
    data_y = []
    
    for i in range(iters):
        player1 = get_choice()
        
        predict = model.predict_proba([str_to_list(player1)])[0]
        
        if predict[0] >= 0.95:
            player2 = options[0]
        elif predict[1] >= 0.95:
            player2 = options[1]
        elif predict[2] >= 0.95:
            player2 = options[2]
        else:
            player2 = get_choice()
            
        if debug==True:
            print("Player1: %s Player2 (modelo): %s --> %s" % (player1, predict, player2))
        
        winner = search_winner(player1, player2)
        if debug==True:
            print("Comprobamos: p1 VS p2: %s" % winner)
        
        if winner==2:
            data_X.append(str_to_list(player1))
            data_y.append(str_to_list(player2))
            
            score["win"]+=1
        else:
            score["loose"]+=1
        
    return score, data_X, data_y


# In[293]:


score, data_X, data_y = play_and_learn(1, debug=True)
print(data_X)
print(data_y)
print("Score: %s %s %%" % (score, (score["win"]*100/(score["win"]+score["loose"]))))
if len(data_X):
    model = model.partial_fit(data_X, data_y)


# In[294]:


i = 0
historic_pct = []
while True:
    i+=1
    score, data_X, data_y = play_and_learn(1000, debug=False)
    pct = (score["win"]*100/(score["win"]+score["loose"]))
    historic_pct.append(pct)
    print("Iter: %s - score: %s %s %%" % (i, score, pct))
    
    if len(data_X):
        model = model.partial_fit(data_X, data_y)
    
    if sum(historic_pct[-9:])==900:
        break


# In[295]:


import math
import numpy as np
from matplotlib import pyplot as plt


# In[296]:


x = range(len(historic_pct))
y = historic_pct

plt.ion()
plt.plot(x,y)


# In[297]:


model.predict_proba([str_to_list("piedra")])