import pygame
import sys
from botao import Botao

#definir diretório
import os
# Define o diretório de trabalho como o diretório do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Menu():
    def __init__(self):
        pygame.init() #inicializar pygame
        # Atributos tela
        self.__screen = pygame.display.set_mode((1000, 800))
        self.__background = pygame.image.load('Image/fundoMenu.jpg')

        # Atributos fontes
        self.__title_font = pygame.font.Font('font/Laira.otf', 45)  # Fonte maior para o título
        self.__option_font = pygame.font.Font('font/Orbitron-VariableFont_wght.ttf', 36)  # Fonte maior para as opções
        self.__button_font = pygame.font.Font('font/Laira.otf', 24) #Fonte para a escrita dos botões

        #atributo das naves
        self.__nave1 = pygame.image.load('Image/nave1.png')
        self.__nave2 = pygame.image.load('Image/nave2.png')

        #atributos botao
        self.__botao_score = Botao((self.screen.get_width() - 200) // 2, self.screen.get_height() // 2 + 200, 200, 50, "Ver Scores")
    
    #GETTERS E SETTERS
    #Getters e setter para tela
    @property
    def screen(self):
        return self.__screen
    @screen.setter
    def screen(self, x, y):
        self.__screen = pygame.display.set_mode(x,y)

    # Getters e setters para o fundo
    @property
    def background(self):
        return self.__background
    @background.setter
    def background(self, path):
        self.__background = pygame.image.load(path)

    # Getters e setters para o título
    @property
    def title_font(self):
        return self.__title_font
    @title_font.setter
    def title_font(self, font_path, size):
        self.__title_font = pygame.font.Font(font_path, size)

    # Getters e setters para as opções
    @property
    def option_font(self):
        return self.__option_font
    @option_font.setter
    def option_font(self, font_path, size):
        self.__option_font = pygame.font.Font(font_path, size)

    # Getters e setters para as imagens dos personagens
    @property
    def nave1(self):
        return self.__nave1
    @nave1.setter
    def nave1(self, valor):
        self.__nave1 = pygame.image.load(valor)

    @property
    def nave2(self):
        return self.__nave2
    @nave2.setter
    def nave2(self, valor):
        self.__nave2 = pygame.image.load(valor)

    @property
    def button_font(self):
        return self.__button_font
    @button_font.setter
    def button_font(self, font_path, size):
        self.__button_font = pygame.font.Font(font_path, size)

    @property
    def botao_score(self):
        return self.__botao_score
    @botao_score.setter
    def botao_score(self, pos_x, pos_y, largura_botao, altura_botao):
        self.__botao_score = Botao(pos_x, pos_y, largura_botao, altura_botao, "Ver Scores")

    #função mostrar menu
    def mostrarMenu(self):
        personagem_selecionado = None

        while personagem_selecionado is None:
            #desenha a imagem no fundo -> blit: desenhar uma imagem ou superfície sobre outra. superficiedestino.blit(superficieorigem, coordenadas)
            self.screen.blit(self.background, (0,0))

            #título do menu
            titulo = self.title_font.render("S P A C E  P R O T E C T O R S", True, (0, 0, 0))
            titulo_rect = titulo.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 200))
            self.screen.blit(titulo, titulo_rect)

            #Texto "Escolha seu personagem"
            texto_escolha = self.option_font.render("Escolha seu personagem", True, (255,0,0))
            texto_rect = texto_escolha.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
            self.screen.blit(texto_escolha, texto_rect) 

            #desenhar imagem dos personagens
            nave1_rect = self.nave1.get_rect(center=(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 50))
            nave2_rect = self.nave2.get_rect(center=(self.screen.get_width() // 2 + 100, self.screen.get_height() // 2 + 50))
            self.screen.blit(self.nave1,nave1_rect)
            self.screen.blit(self.nave2, nave2_rect)

            #desenha botao
            self.botao_score.desenhar(self.screen, self.button_font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #verifica evento botão
                if self.botao_score.verificar_evento(event):
                    personagem_selecionado = 'view_scores'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if nave1_rect.collidepoint(event.pos):
                        personagem_selecionado = 'nave1'
                    elif nave2_rect.collidepoint(event.pos):
                        personagem_selecionado = 'nave2'
            
            pygame.display.update()

        return personagem_selecionado 

    #função para mostrar a tela de score
    def mostrarScore(self):
        scores_para_exibir = []
        
        #Tratamento de Exceções para Leitura do Arquivo
        try:
            # 'with open' é a forma mais segura de garantir que o arquivo será fechado.
            with open("log.txt", "r", encoding="utf-8") as file:
                scores_para_exibir = file.readlines()
            
            scores_para_exibir = scores_para_exibir[-15:] #list slicing p/ mostrar só os 15 últimos
            
            if not scores_para_exibir:
                scores_para_exibir.append("Nenhuma pontuação registrada.\n")

        except FileNotFoundError:
            mensagem = "Arquivo de scores ainda não foi criado."
            scores_para_exibir.append(mensagem + "\n")
            print(f"AVISO: {mensagem} Jogue uma partida para criá-lo.")
        except Exception as e:
            mensagem = "Ocorreu um erro ao ler os scores."
            scores_para_exibir.append(mensagem + "\n")
            print(f"ERRO: Não foi possível ler 'log.txt': {e}")
        
        #Config do Botão "Voltar"
        largura_botao = 150
        altura_botao = 50
        #centro inferior da tela
        pos_x = (self.screen.get_width() - largura_botao) // 2
        pos_y = self.screen.get_height() - altura_botao - 30

        botao_voltar = Botao(pos_x, pos_y, largura_botao, altura_botao, "Voltar")

        viewing_scores = True
        while viewing_scores:
            # Preenche o fundo
            self.screen.fill((0, 0, 0))

            # Desenha o título da tela
            title_text = self.title_font.render("SCORES", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 60))
            self.screen.blit(title_text, title_rect)

            # Desenha cada linha de score
            y_offset = 120
            for line in scores_para_exibir:
                score_text = self.option_font.render(line.strip(), True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, y_offset))
                self.screen.blit(score_text, score_rect)
                y_offset += 40

            # Loop de eventos da tela de score
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                # Verifica se o botão "Voltar" foi clicado
                if botao_voltar.verificar_evento(event):
                    viewing_scores = False # Encerra o loop e volta ao menu

            # Desenha o botão na tela
            botao_voltar.desenhar(self.screen, self.button_font)
            
            # Atualiza a tela para mostrar tudo
            pygame.display.update()
    

# if __name__ == "__main__":
#     menu = Menu()
#     personagem_selecionado = menu.mostrarMenu()
#     pygame.quit()
