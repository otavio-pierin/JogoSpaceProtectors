import pygame
import random
from objeto import Objeto
from inimigo import Inimigo
from poder import Poder

class Inimigo3(Inimigo):
    #inimigo se move lentamente para baixo em zig-zag.

    def __init__(self, x, y, speed_x, speed_y, image_path, speed_poder, image_poder, size, chance_disparo):
        super().__init__(x, y, speed_x, speed_y, image_path, speed_poder, image_poder,chance_disparo)
        self.image = pygame.transform.scale(self.image, size) #transforma a imagem do inimigo tupla(size,size)
        
        # Atributos para o zig-zag
        self.__zig_zag_timer = pygame.time.get_ticks() #guarda o tempo desde que __init__ foi chamado
        self.__zig_zag_interval = 700  # Intervalo em milissegundos para mudar de direção

    @property
    def zig_zag_timer(self):
        return self.__zig_zag_timer
    @zig_zag_timer.setter
    def zig_zag_timer(self, valor):
        self.__zig_zag_timer = valor
    @property
    def zig_zag_interval(self):
        return self.__zig_zag_interval  

    def move(self):
        #Sobrescreve o método move para implementar a lógica de zig-zag.
        # Movimento vertical constante e lento para baixo
        self.y += self.speed_y

        # Movimento horizontal em zig-zag
        self.x += self.speed_x

        # Verifica se é hora de inverter a direção horizontal
        agora = pygame.time.get_ticks()
        if agora - self.zig_zag_timer > self.zig_zag_interval:
            self.zig_zag_timer = agora
            self.speed_x *= -1 # Inverte a direção do movimento lateral

        #limites laterais da tela
        if self.x <= 0 or self.x >= 950:
            self.speed_x *= -1

        # Lógica de tiro
        if self.power.state == "ready" and random.randint(0, 100) < self.chance_disparo:  # chance de atirar
            self.power.fire(self.x + 32, self.y + 32)

        # Se o inimigo ultrapassar a borda inferior da tela (800 de altura)
        if self.y > 800:
            self.reset_position()                

    def draw(self, screen):
        super().draw(screen)

    def reset_position(self):
        super().reset_position()