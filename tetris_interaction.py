import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from TetrisLib import tetris
import keyboard as k

t = tetris(W=10,H=24,debugMode=False)


 #Evento de tecla pulsada. Mover pieza.
 
k.on_press(lambda event: t.key_pressed(event.name))

k.wait('esc')
t.endgame(show_message=False)