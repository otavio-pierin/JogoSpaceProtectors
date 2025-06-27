import pygame
from inimigo import Inimigo
from poderteleguiado import PoderTeleguiado
import random
from jogador import Jogador

class Inimigo4(Inimigo):
    def __init__(self, x, y, speed_x, speed_y, image_path, speed_poder, image_poder, chance_disparo, size):
        super().__init__(x, y, speed_x, speed_y, image_path, speed_poder, image_poder, chance_disparo)
        self.power = PoderTeleguiado(self.x, self.y, image_poder, speed_poder) 
        self.image = pygame.transform.scale(self.image, size) #transforma a imagem do inimigo tupla(size,size)        
    

    def move(self, jogador:Jogador):
       
        self.x += self.speed_x
        if self.x <= 0 or self.x >= 950:
           self.speed_x *=-1
           self.y += self.speed_y

        if self.power.state == "ready" and random.randint(0,100)<self.chance_disparo:
            self.power.fire(self.x, self.y, jogador.x, jogador.y)
