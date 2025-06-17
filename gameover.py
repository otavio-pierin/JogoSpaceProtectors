import pygame
from pygame import mixer
from botao import Botao

class GameOver():
    def __init__(self, screen, font, over_font, background):
        self.__screen = screen
        self.__font = font
        self.__over_font = over_font
        self.__background = background

    # Getters e setters para o atributo screen
    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, value):
        self.__screen = value

    # Getters e setters para o atributo font
    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, value):
        self.__font = value

    # Getters e setters para o atributo over_font
    @property
    def over_font(self):
        return self.__over_font

    @over_font.setter
    def over_font(self, value):
        self.__over_font = value

    # Getters e setters para o atributo background
    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, value):
        self.__background = value

    #exibir a tela de Game Over
    def mostrar(self):
        mixer.music.pause()  # Pausa a música ao entrar na tela de Game Over
        while True:
            self.__screen.blit(self.__background, (0, 0))  # Define o fundo para a tela de Game Over

            over_text = self.__over_font.render("GAME OVER", True, (255, 255, 255))
            
            #Config do Botão "Menu"
            largura_botao = 150
            altura_botao = 50
            #centro da tela
            pos_x = (self.screen.get_width() - largura_botao) // 2
            pos_y = self.screen.get_height() //2  + (altura_botao + 30)

            botao_menu = Botao(pos_x, pos_y, largura_botao, altura_botao, "Reiniciar")

            # Centraliza o texto GAME OVER
            over_text_rect = over_text.get_rect(center=(self.__screen.get_width() // 2, self.__screen.get_height() // 2 - 50))
            self.__screen.blit(over_text, over_text_rect)



            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Desenha o botão na tela
                botao_menu.desenhar(self.screen, self.button_font)
                
                # Verifica se o botão "Voltar" foi clicado
                if botao_menu.verificar_evento(event):
                        mixer.music.stop()  # Para a música ao voltar ao menu
                        return  # Retorna ao menu principal 
       