import pygame
import math
from objeto import Objeto

class Poder(Objeto):
    def __init__(self, x, y, image_path, velocidade_y):
        super().__init__(x, y, image_path)
        self.__speed_y = velocidade_y
        self.__state = "ready"
    
    #Getters e setters
    @property
    def speed_y(self):
        return self.__speed_y
    @speed_y.setter
    def speed_y(self,valor):
        self.__speed_y = valor

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self,valor):
        self.__state = valor
    
    #Método para disparar
    def fire(self,x,y):
        self.state = "fire"
        self.x = x
        self.y = y
    
    def move(self):
        if self.state == "fire":
            self.y += self.speed_y
        if self.y >= 780:
            self.state = "ready"
            self.y = 0

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))

    #verifica colisão com o jogador
    def is_collision(self, jogador):
        distancia = math.sqrt(math.pow(jogador.x - self.x, 2) + (math.pow(jogador.y - self.y, 2)))
        return distancia < 40 #se a distância do poder e do jogador for menor que 40px retorna que foi atingido