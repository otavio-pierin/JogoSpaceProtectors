import pygame
from abc import ABC, abstractmethod

class Personagem():
    def __init__(self, x, y, image_path):
        self.__x = x
        self.__y = y
        try:
            self._image = pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Erro ao carregar a imagem: {image_path}")
            #imagem padrão em caso de erro
            self._image = pygame.Surface((40, 40))
            self._image.fill((255, 0, 255)) # Cor rosa
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,valor):
        self.__x = valor

    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,valor):
        self.__y = valor