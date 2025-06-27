import pygame
from objeto import Objeto

class Jogador(Objeto):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.__mov_x = 0

    #Getters e Setters

    #Getter e Setter do movimento da variável x
    @property
    def mov_x(self):
        return self.__mov_x
    @mov_x.setter
    def mov_x(self, move):
        self.__mov_x = move
    
    #Método para movimentação da nave
    def move(self):
        self.x += self.mov_x #é limitado no setter de x
    
    #desenhar o jogador na tela
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
