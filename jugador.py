import instanciaPartida as ip 
import random
import time 


partida = ip.Partida()
for i in range(10): 
    time.sleep(1)
    arr = [0, 0, 0, 0]
    arr[random.randint(0, 3)] = 1
    partida.jugar(arr)
    