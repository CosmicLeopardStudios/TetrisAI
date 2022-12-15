
import random
import sys
import pickle
from datetime import datetime
import numpy as np

class tetris:
    DERECHA = 'd'
    IZQUIERDA = 'a'
    ROTAR_DER = 'e'
    ROTAR_IZQ = 'q'
    NADA = 's'
    
    def __init__(self, W, H, generate_data=True, debugMode = False):
        self.W = W
        self.H = H
        self.save_tuples = []
        self.generate_data = generate_data
        self.current_pieza = []
        self.tablero = []
        self.debugMode = debugMode
        
        for i in range(self.H):
            self.tablero.append([])
            for j in range(self.W):
                self.tablero[-1].append(0)
        self.gameover = False
        
        if not self.debugMode:
            nlines = self.H + 2
        
            # scroll up to make room for output
            print(f"\033[{nlines}S", end="")

            # move cursor back up
            print(f"\033[{nlines}A", end="")

            # save current cursor position
            print("\033[s", end="")
            
        self.create_pieza(None)


#region piezas

    pieza1 = [[1,1,1,1]]

    pieza2 = [[1,1],
            [1,1]]

    pieza3 = [[1,1,0],
            [0,1,1]]

    pieza4 = [[0,1,1],
            [1,1,0]]

    pieza5 = [[1,1,1],
            [1,0,0]]

    pieza6 = [[1,1,1],
            [0,0,1]]

    pieza7 = [[0,1,0],
            [1,1,1]]

    piezas = [pieza1,pieza2,pieza3,pieza4,pieza5,pieza6,pieza7]

#endregion

#region Tablero


    def print_tablero(self):
        if self.gameover or self.debugMode:
            return None

        #Preparar output string color format
        shown_tablero = []
        for i in self.tablero:
            shown_tablero.append([])
            for n in i:
                shown_tablero[-1].append(str(n))
        for x,y in self.current_pieza:
            shown_tablero[y][x] = '2'
        print("\033[u", end="")
        print('+', end='')
        for i in range(self.W):
            print('--', end='')
        print('+', end='\n')
        
        for i in range(self.H):
            print('|', end = '')
            for j in range(self.W):
                color = ''
                if shown_tablero[i][j] == '1':
                    color = '\033[94m'
                elif shown_tablero[i][j] == '0':
                    color = '\033[90m'
                else:
                    color = '\033[95m'
                print(color + '██',end='')
            print('\033[0m' +'|')
        
        print('+', end='')
        for i in range(self.W):
            print('--', end='')
        print('+', end='\n')
#endregion

#region Bucle principal
    def key_pressed(self,key:str):
        if self.gameover:
            return None
        
        can_move = True
        if key == tetris.DERECHA:
            self.register_data(key)
            self.move_current(1,0)
        elif key == tetris.IZQUIERDA:
            self.register_data(key)
            self.move_current(-1,0)
        elif key == tetris.ROTAR_DER:
            self.register_data(key)
            self.rotate_current('der')
        elif key == tetris.ROTAR_IZQ:
            self.register_data(key)
            self.rotate_current('izq')
        elif key == tetris.NADA:
            self.register_data(key)
            self.move_current(0,1)
#endregion

#region metodos
    def get_perceptron_data(self):
        decoded = tetris.decode_pieza(self.current_pieza,self.W,self.H)
        return np.array([*self.tablero,*decoded]).flatten()
    
    def encode_pieza(self, pieza, dx,dy):
        res = []
        for y,l in enumerate(pieza):
            for x,e in enumerate(l):
                if e == 1:
                    res.append((x + dx,y + dy))
        return res

    def decode_current(self):
        res = []
        for i in range(self.H):
            res.append([])
            for j in range(self.W):
                res[-1].append(0)

        for x,y in self.current_pieza:
            res[y][x] = 1
        return res
    
    def decode_pieza(p,w,h):
        res = []
        for i in range(h):
            res.append([])
            for j in range(w):
                res[-1].append(0)

        for x,y in p:
            res[y][x] = 1
        return res

    def move_current(self, d_x, d_y):
        
        if self.debugMode:
            print("move_current: ", self.current_pieza)
        
        can_move = True
        res = []
        for x,y in self.current_pieza:
            res.append((x + d_x, y + d_y))
            
        for x,y in res:
            if x < 0 or x >= self.W or (d_y == 0 and self.tablero[y][x] == 1):
                can_move = False
            if d_y > 0 and (y >= self.H or self.tablero[y][x] == 1):
                self.create_pieza()
                return
        if not can_move:
            return
        
        self.current_pieza = res
        self.print_tablero()
        

    def rotate_current(self, dir):
        new_pieza = []
        xs = [x for x,y in self.current_pieza]
        ys = [y for x,y in self.current_pieza]
        min_x = min(xs)
        min_y = min(ys)
        max_x = max(xs)
        max_y = max(ys)
        w = max_x - min_x +1
        h = max_y - min_y +1
        
        if dir == 'der':
            for x,y in self.current_pieza:
                norm_x = x - min_x
                norm_y = y - min_y
                new_pieza.append((h - norm_y + min_x-1, norm_x + min_y))
        else:
            for x,y in self.current_pieza:
                norm_x = x - min_x
                norm_y = y - min_y
                new_pieza.append((norm_y + min_x, w-norm_x + min_y-1))

        for x,y in new_pieza:
            if self.W <= x or x < 0 or self.H <= y or y < 0 or self.tablero[y][x] == 1:
                print('Nope')
                return
        self.current_pieza = new_pieza
        self.print_tablero()
        
    def endgame(self,show_message=True):
        if self.gameover:
            return None
        now = datetime.now()
        file_name = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)   
        if self.generate_data:
            with open('Samples/' + file_name + '.pickle', 'wb') as file:
                pickle.dump(self.save_tuples, file)
        if show_message:
            print("GAME OVER: pres ESC")
        self.gameover = True

    def create_pieza(self, pieza=None):
        if pieza == None:
            pieza = tetris.piezas[random.randint(0,len(tetris.piezas)-1)]
        
        if self.gameover:
            return None
        
        mirar_ys = []
        for x,y in self.current_pieza:
            if self.tablero[y][x] == 1:
                self.endgame()
            mirar_ys.append(y)
            self.tablero[y][x] = 1
        
        mirar_ys.sort()
        for y in mirar_ys:
            if self.tablero[y].count(0) == 0:
                del self.tablero[y]
                self.tablero.insert(0,[0]*self.W)
        
        
        self.current_pieza = self.encode_pieza(pieza, (self.W - len(pieza[0]))//2, 0)
        self.print_tablero()

    def register_data(self, key):
        if self.generate_data:
            self.save_tuples.append((self.tablero,self.current_pieza,key))
#endregion





