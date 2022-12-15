from TetrisLib import tetris
import numpy as np
import time

t = tetris(10,24,generate_data=False)

Cs = ['a','s','d','q','e']

W = np.load('W_matrix.npy')
queue = [None,None,None,None]
def all_equals():
    return queue[0] != None and queue[0] == queue[1] == queue[2] == queue[3]

while True:
    key = Cs[np.argmax(t.get_perceptron_data().dot(W))]
    queue.append(key)
    queue = queue[1:]
    if all_equals():
        key = 's'
    t.key_pressed(key)
    time.sleep(0.5)
