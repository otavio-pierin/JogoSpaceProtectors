import pygame
import random
from objeto import Objeto
from inimigo import Inimigo
from poder import Poder

class Enemy3(Inimigo):
    #inimigo se move lentamente para baixo em zig-zag.

    def __init__(self, x, y, speed_x, speed_y, image_path, speed_poder, image_poder, size):
        super().__init__(self, x, y, speed_x, speed_y, image_path, speed_poder, image_poder)
        self.image = pygame.transform.scale(self.image, size) #transforma a imagem do inimigo tupla(size,size)

        #self.speed_y = 0.25  # Velocidade de queda LENTA
        #self.speed_x = 0.5  # Velocidade do movimento lateral
        
        # Atributos para o zig-zag
        self.__zig_zag_timer = pygame.time.get_ticks() #guarda o tempo desde que __init__ foi chamado
        self.__zig_zag_interval = 700  # Intervalo em milissegundos para mudar de direção

    @property
    def zig_zag_timer(self):
        return self.__zig_zag_timer
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
        if self.x <= 0 or self.x >= 950: # 800 - largura da imagem (~64)
            self.speed_x *= -1

        # Lógica de tiro (opcional, pode ser ajustada)
        if self.power.state == "ready" and random.randint(0, 100) < 3:  # 3% de chance de atirar
            self.power.fire(self._x + 32, self._y + 32)

    def draw(self, screen):
        super().draw(screen)
        self.power.move()
        self.power.draw(screen)

    def reset_position(self):
        super().reset_position()
        self.power.state = "ready"  # Reseta o estado do poder    