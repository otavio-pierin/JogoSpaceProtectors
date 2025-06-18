import pygame
import math
from objeto import Objeto
from poder import Poder

class Bullet(Poder): #classe do poder dos jogadores
    def __init__(self, x, y, image_path, speed_y):
        super().__init__(x, y, image_path, speed_y)        

    # Método para disparar a bala
    def fire(self, x):
        self.state = "fire"
        self.x = x

    # Método para mover a bala
    def move(self):
        if self.state == "fire":
            self.y -= self.speed_y
        if self.y <= 0:
            self.state = "ready"
            self.y = 720

    # Método para desenhar a bala na tela
    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x + 2, self.y + 2))

    # Método para verificar colisão com o inimigo
    def is_collision(self, enemy):
        distance = math.sqrt(math.pow(enemy.x - self.x, 2) + math.pow(enemy.y - self.y, 2))
        return distance < 40