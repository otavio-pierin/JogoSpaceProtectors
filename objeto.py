import pygame
from abc import ABC, abstractmethod

class Objeto(ABC):
    def __init__(self, x, y, image_path):
        self.__image = pygame.image.load(image_path)
        self.__x = x
        self.__y = y
    
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,valor):
        self.__x = max(0, min(valor, 950)) #limita o movimento ao tamanho da tela

    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,valor):
        self.__y = valor

    @property
    def image(self):
        return self.__image
    @image.setter
    def image(self, novo):
        self.__image = novo

    @abstractmethod
    def draw(self, screen):
        pass
    @abstractmethod
    def move(self):
        pass