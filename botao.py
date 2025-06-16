import pygame
import sys

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_fundo=(70, 70, 70), cor_hover=(100, 100, 100), cor_texto=(255, 255, 255)):
        self.__rect = pygame.Rect(x, y, largura, altura)
        self.__texto = str(texto)
        self.__cor_fundo = cor_fundo
        self.__cor_hover = cor_hover
        self.__cor_texto = cor_texto
        
        # Atributos de estado interno
        self.__cor_atual = cor_fundo
        self.__clicado = False

    # --- Getters e Setters ---
    @property
    def rect(self):
        return self.__rect
    @rect.setter
    def rect(self, value):
        if not isinstance(value, pygame.Rect):
            raise TypeError("O valor para rect deve ser um objeto pygame.Rect")
        self.__rect = value
    @property
    def texto(self):
        return self.__texto
    @texto.setter
    def texto(self, value):
        self.__texto = str(value)
    @property
    def cor_texto(self):
        return self.__cor_texto
    @cor_texto.setter
    def cor_texto(self, value):
        self.__cor_texto = value
    @property
    def clicado(self):
        return self.__clicado
    @clicado.setter
    def clicado(self, valor):
        self.__clicado = valor
    @property
    def cor_atual(self):
        return self.__cor_atual
    @cor_atual.setter
    def cor_atual(self, value):
        self.__cor_fundo = value    
    @property
    def cor_hover(self):
        return self.__cor_hover
    @cor_hover.setter
    def cor_hover(self, value):
        self.__cor_hover = value
    @property
    def cor_fundo(self):
        return self.__cor_fundo
    @cor_fundo.setter
    def cor_fundo(self, value):
        self.__cor_fundo = value

    def desenhar(self, screen, fonte):
        # Desenha o retângulo do botão
        pygame.draw.rect(screen, self.cor_atual, self.rect, border_radius=10)

        # Renderiza e centraliza o texto
        texto_surface = fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        screen.blit(texto_surface, texto_rect)

    def verificar_evento(self, event):
        self.clicado = False
        mouse_pos = pygame.mouse.get_pos()

        # Verifica se o mouse está sobre o botão (efeito hover)
        if self.rect.collidepoint(mouse_pos):
            self.cor_atual = self.cor_hover
            # Verifica se houve um clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicado = True
        else:
            self.cor_atual = self.cor_fundo
        
        return self.clicado