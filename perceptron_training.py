import numpy as np
import pickle
from TetrisLib import tetris

#We got 5 different classes:
# Right, Left, Nothing(Down)
# Turn_Right, Turn_Left

#With 10*24*2 binary (0,1) data we have to predict the output.


max_iterations = 50000
Cs = ['a','s','d','q','e']

W = np.zeros((480,5))
data = []
labels = []
with open('Samples/2022-11-29_14-38-51.pickle','rb') as f:
    loaded_data = pickle.load(f)
    for t,p,c in loaded_data:
        decoded = tetris.decode_pieza(p,10,24)
        data.append(np.array([*t,*decoded]).flatten())
        labels.append(Cs.index(c))

data = np.array(data)
labels = np.array(labels)
N = data.shape[0]
paso = 0.2

error = True
iteration = 0
while error and iteration < max_iterations:
    error = False
    product = data.dot(W)
    prod_labels = np.argmax(product,axis=1)
    for i,l in enumerate(prod_labels):
        if l != labels[i]:
            escalar_prod = data[i]*paso
            W[:,l] -= escalar_prod
            W[:,labels[i]] += data[i]
            error = True
    iteration += 1

sum = 0
for i,l in enumerate(prod_labels):
    sum += not (l == labels[i])

np.save('W_matrix',W)
print('Done. Training error = ', sum / N)

        

