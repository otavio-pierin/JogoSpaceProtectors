import pygame
import random
from inimigo import Inimigo
from poder import Poder

class Inimigo2(Inimigo):
    def __init__(self, x, y, speed_x, speed_y, image_path, speed_poder, image_poder, size):
        super().__init__(self, x, y, speed_x, speed_y, image_path, speed_poder, image_poder)
        self.image = pygame.transform.scale(self.image, size) #transforma a imagem do inimigo tupla(size,size)

    #Mover inimigo
    def move(self):
        super().move()
        if self.power.state == "ready" and random.randint(0,100)<1: #Chance de 1% de disparar
            self.power.fire(self.x+16, self.y+32)

    # Método para desenhar o inimigo e o poder na tela
    def draw(self, screen):
        super().draw(screen)
        self.power.move()
        self.power.draw(screen)

    # Método para resetar a posição do inimigo e o estado do poder
    def reset_position(self):
        super().reset_position()
        self.power.state = "ready"  # Reseta o estado do poder    
