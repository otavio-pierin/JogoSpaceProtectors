import pygame
import math
from objeto import Objeto

class Bullet(Objeto):
    def __init__(self, x, y, image_path, speed_y):
        super().__init__(x, y, image_path)
        self.__speed_y = speed_y
        self.__state = "ready"        

    # Getter e setter para a velocidade em y
    @property
    def speed_y(self):
        return self.__speed_y

    @speed_y.setter
    def speed_y(self, value):
        self.__speed_y = value

    # Getter e setter para o estado da bala
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    # Método para disparar a bala
    def fire(self, x):
        self.state = "fire"
        self.x = x

    # Método para mover a bala
    def move(self):
        if self.state == "fire":
            self.y -= self.__speed_y
        if self.y <= 0:
            self.state = "ready"
            self.y = 720

    # Método para desenhar a bala na tela
    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self._image, (self.x + 2, self.y + 2))

    # Método para verificar colisão com o inimigo
    def is_collision(self, enemy):
        distance = math.sqrt(math.pow(enemy.x - self.x, 2) + math.pow(enemy.y - self.y, 2))
        return distance < 27