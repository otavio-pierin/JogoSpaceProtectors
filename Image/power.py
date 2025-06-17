import pygame
import math

class Power():
    def __init__(self, x, y, speed_y):
        self._image = pygame.image.load('imagem/poderenemy.png')
        self._x = x
        self._y = y
        self._speed_y = speed_y
        self._state = "ready"

    # Getters e setters para a posição x
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    # Getters e setters para a posição y
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    # Getters e setters para a velocidade em y
    @property
    def speed_y(self):
        return self._speed_y

    @speed_y.setter
    def speed_y(self, value):
        self._speed_y = value

    # Getter e setter para o estado
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    # Getter para a imagem (somente leitura)
    @property
    def image(self):
        return self._image

    # Método para disparar o poder
    def fire(self, x, y):
        self.state = "fire"
        self.x = x
        self.y = y

    # Método para mover o poder
    def move(self):
        if self.state == "fire":
            self.y += self._speed_y
        if self.y >= 780:
            self.state = "ready"
            self.y = 0

    # Método para desenhar o poder na tela
    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self._image, (self._x, self._y))

    # Método para verificar colisão com o jogador
    def is_collision(self, player):
        distance = math.sqrt(math.pow(player.x - self._x, 2) + (math.pow(player.y - self._y, 2)))
        return distance < 43