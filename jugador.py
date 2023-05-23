import instanciaPartida as ip
import random
import time

class PartidaFactory:
    @staticmethod
    def create_partida():
        partida = ip.Partida()
        return partida

partida = PartidaFactory.create_partida()
partida2 = PartidaFactory.create_partida()
partida3 = PartidaFactory.create_partida()

for i in range(300): 
    seed_value = random.randint(0, 1000000)  # Generate a unique seed value
    random.seed(seed_value)  # Set the seed for random number generation
    
    arr = [0, 0, 0, 0]
    arr[random.randint(0, 3)] = 1
    partida.play(arr)
    random.seed(seed_value + 1)  # Set the seed for the second instance
    arr2 = [0, 0, 0, 0]
    arr2[random.randint(0, 3)] = 1
    partida2.play(arr2)
    random.seed(seed_value + 2)  # Set the seed for the third instance
    arr3 = [0, 0, 0, 0]
    arr3[random.randint(0, 3)] = 1
    partida3.play(arr3)
    if i%20 == 0: 
        partida.showUI()
        time.sleep(1)
        partida.closeUI()
print(partida.best_score)

    
