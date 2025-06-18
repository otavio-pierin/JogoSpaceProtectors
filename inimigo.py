import pygame
import random
from objeto import Objeto
from poder import Poder

class Inimigo(Objeto):
    def __init__(self, x, y, speed_x, speed_y, image_path, speed_poder, image_poder):
        super().__init__(x, y, image_path)
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__power = Poder(self.x, self.y, image_poder, speed_poder)

    # Getters e setters para a velocidade em x
    @property
    def speed_x(self):
        return self.__speed_x

    @speed_x.setter
    def speed_x(self, value):
        self.__speed_x = value

    # Getters e setters para a velocidade em y
    @property
    def speed_y(self):
        return self.__speed_y

    @speed_y.setter
    def speed_y(self, value):
        self.__speed_y = value

    # Getters e setters para o poder
    @property
    def power(self):
        return self.__power

    @power.setter
    def power(self, value):
        self.__power = value        
    
    #método para mover o inimigo
    def move(self):
        self.x += self.speed_x
        if self.x <= 0 or self.x >= 950:
           self.speed_x *=-1
           self.y += self.speed_y

        if self.power.state == "ready" and random.randint(0,100)<5: #chance de 5% de disparar um poder
            self.power.fire(self.x + 16, self.y +32)

    #desenhar o inimigo e o pode na tela
    def draw(self, screen):
        screen.blit(self.image,(self.x,self.y))
        self.power.move()
        self.power.draw(screen)

    #resetar a posição do inimigo e estao do poder
    def reset_position(self):
        self.x = random.randint(0, 950)
        self.y = random.randint(50, 150)
        self.power.state = "ready" #reseta o estado do poder

    #verificar se acertou o jogador
    def check_collision_with_player(self,jogador):
        return self.power.is_collision(jogador) #Verifica se o poder colidiu com o jogador
