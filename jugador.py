import instanciaPartida as ip
import random
import time
class PartidaFactory:
    @staticmethod
    def create_partida():
        partida = ip.Partida()
        return partida

def hotEncode(pos):
    if pos == 0:
        return [1, 0, 0, 0]
    elif pos == 1:
        return [0, 1, 0, 0]
    elif pos == 2:
        return [0, 0, 1, 0]
    elif pos == 3:
        return [0, 0, 0, 1]
    return [0, 0, 0, 0]
def randomPlayer():
    partida = PartidaFactory.create_partida()
    while not partida.isOver():
        partida.play(hotEncode(random.randint(0, 3)))
    partida.showUI()

print("Hola")
randomPlayer()
print("Adios")

    
