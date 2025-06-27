import pygame
from poder import Poder
import math

class PoderTeleguiado(Poder):
    def __init__(self, x, y, image_path, speed_y):
        super().__init__(x, y, image_path, speed_y)

        self.__dx = 0 #variação da cordenada x da bala em comparação com o personagem, varia de -1 e 1 (total esquerda a total direita)
        self.__dy = 0

    #Setters e Getters
    @property
    def dx(self):
        return self.__dx
    @dx.setter
    def dx(self,valor):
        self.__dx = valor
    
    @property
    def dy(self):
        return self.__dy
    @dy.setter
    def dy(self, valor):
        self.__dy = valor
    
    def fire(self, x, y, alvo_x, alvo_y):
        self.x = x
        self.y = y

        #calcular a distância entre a bala e o o player
        distancia_x = alvo_x - self.x
        distancia_y = alvo_y - self.y

        #distancia total, usando pitágoras
        distancia_total = math.sqrt((distancia_x*distancia_x) + (distancia_y*distancia_y))

        #transforma x e y em valores limitado de 1 a -1
        if distancia_total > 0:
            self.dx = distancia_x / distancia_total
            self.dy = distancia_y / distancia_total            
        else: #se estiver na mesma posição do jogador
            self.dx=0
            self.dy=1

        self.state = "fire" #muda o estado para atirar

    def move(self):
        if self.state == "fire":
            #altera a posição de x e y baseada na velocidade setada no objeto
            self.x += self.dx * self.speed_y
            self.y += self.dy * self.speed_y
        if self.y > 780:
            self.state = "ready"
            self.y = 0
        