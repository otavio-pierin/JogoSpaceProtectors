import pygame
from abc import ABC, abstractmethod

class Personagem():
    def __init__(self, x, y, image_path):
        self.__x = x
        self.__y = y
    
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