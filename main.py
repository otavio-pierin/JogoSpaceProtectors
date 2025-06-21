import pygame
import random
from pygame import mixer
from jogador import Jogador
from inimigo import Inimigo
from inimigo3 import Inimigo3
from bullet import Bullet
from menu import Menu
from botao import Botao

import os
# Define o diretório de trabalho como o diretório do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class SpaceProtectors():
    def __init__(self):
        pygame.init() #inicializa o pygame

        #Configuração da tela e fundo
        self.__screen = pygame.display.set_mode((1000,800))
        pygame.display.set_caption("Space Protectors")
        self.__background = pygame.image.load('Image/fundojogo.png')
        self.__game_over_background = pygame.image.load('Image/fundoGameOver.jpg')

        #Fonte e som
        self.__font = pygame.font.Font('font/Laira.otf', 32)
        self.__over_font = pygame.font.Font('font/Orbitron-VariableFont_wght.ttf',50)
        mixer.music.load("Audio/musicafundo.wav")

        #Estado do jogo
        self.__personagem_selecionado = None
        self.__score_value = 0

        #Instância do menu
        self._menu = Menu()

        #Balas disparo duplo da nave2
        self.__bullets = [] # Lista para armazenar balas quando nave2 for selecionado

    #Getters e Setters
    @property
    def screen(self):
        return self.__screen
    @screen.setter
    def screen(self, valor:tuple):
        self.__screen = pygame.display.set_mode(valor)
    
    @property
    def background(self):
        return self.__background
    @background.setter
    def background(self, image_path):
        self.__background = pygame.image.load(image_path)
    
    @property
    def game_over_background(self):
        return self.__game_over_background
    @game_over_background.setter
    def game_over_background(self, image_path):
        self.__game_over_background = pygame.image.load(image_path)    

    @property
    def font(self):
        return self.__font
    @font.setter
    def font(self, image_path):
        self.__font = pygame.font.Font(image_path)

    @property
    def over_font(self):
        return self.__over_font
    @over_font.setter
    def over_font(self, image_path):
        self.__over_font = pygame.font.Font(image_path) 

    @property
    def score_value(self):
        return self.__score_value
    @score_value.setter
    def score_value(self, valor):
        self.__score_value = valor

    @property
    def personagem_selecionado(self):
        return self.__personagem_selecionado
    @personagem_selecionado.setter
    def personagem_selecionado(self, valor):
        self.__personagem_selecionado = valor
    
    @property
    def bullets(self):
        return self.__bullets
    @bullets.setter
    def bullets(self, valor):
        self.__bullets = valor
    
    #salvar pontuação
    def salvar_score(self):
        try:
            with open("log.txt", "a") as file: #a -> append escreve no final
                if self.score_value > 0:
                    file.write(f"Score: {self.score_value}, {self.personagem_selecionado}\n")
        except IOError as e:
            print(f"Erro ao salvar o score: {e}")
    
    #Exibir pontuação
    def mostrar_score(self, x, y):
        score = self.font.render("Score: "+ str(self.score_value), True, (255,255,255))
        self.screen.blit(score, (x,y))
    
    #Tela de game over
    def game_over_screen(self):
        self.salvar_score() #salva a pontuação
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

            #instância para o botão de voltar ao menu
            botao_menu = Botao(pos_x, pos_y, largura_botao, altura_botao, "Reiniciar")

            # Centraliza o texto GAME OVER
            over_text_rect = over_text.get_rect(center=(self.__screen.get_width() // 2, self.__screen.get_height() // 2 - 50))
            self.__screen.blit(over_text, over_text_rect)
            
            #escrever a pontuação na tela
            if self.score_value == 0:
                no_score_text = self.font.render("Sem pontuação!", True, (255, 255, 255))
                no_score_text_rect = no_score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 200))
                self.screen.blit(no_score_text, no_score_text_rect)  
            else:
                no_score_text = self.font.render("Pontuação: " + str(self.score_value), True, (255, 255, 255))
                no_score_text_rect = no_score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 200))
                self.screen.blit(no_score_text, no_score_text_rect)                      


            # Desenha o botão na tela
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                # Verifica se o botão "Voltar" foi clicado
                if botao_menu.verificar_evento(event):
                        mixer.music.stop()  # Para a música ao voltar ao menu
                        return  # Retorna ao menu principal         

            botao_menu.desenhar(self.screen, self.font)
            pygame.display.update()#atualiza a tela
 
    def game(self):
        self.score_value = 0
        
        #CONFIGURAÇÃO INICIAL
        try:
            mixer.music.play(-1)

            if self.personagem_selecionado == "nave1":
                player_image = 'Image/nave1.png'
                bullet = Bullet(0, 720, 'Image/laser_amarelo.png', 10)
            else: # Se for nave2
                player_image = 'Image/nave2.png'
                caminho_bala_nave2 = 'Image/laser_amarelo.png'
                self.bullets = [Bullet(0, 720, caminho_bala_nave2, 5), Bullet(0, 720, caminho_bala_nave2, 4)] #lista de balas (dupla)

            player = Jogador(370, 720, player_image)

            #lista com todos os inimigos
            inimigos = [Inimigo(random.randint(0,950), random.randint(50,150), 6, 20, 'Image/inimigo5.png', 1, 'Image/poderenemy.png',5) for _ in range(5)]
            inimigos.extend([Inimigo(random.randint(0,950), random.randint(50,150), 3.0, 20, 'Image/inimigo4.png', 1.0, 'Image/poderenemy2.png',3) for _ in range(6)])
            inimigos.extend([Inimigo3(random.randint(0,950), random.randint(50,150), 4.5, 2, 'Image/inimigo3.png', 2.0, 'Image/laser_vermelho.png', (60,60),3) for _ in range(3)])

        except pygame.error as e:
            print(f"Erro ao carregar recursos do jogo: {e}")
            return

        #LOOP PRINCIPAL
        running = True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.background, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN: #ao apertar uma tecla (move +-4px cada vez e atira ao apertar espaço)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
                        player.mov_x = -4
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.mov_x = 4
                    if event.key == pygame.K_SPACE:
                        if self.personagem_selecionado == 'nave1' and bullet.state == "ready":
                            mixer.Sound('Audio/laser_shot.wav').play()
                            bullet.fire(player.x)
                        elif self.personagem_selecionado == 'nave2' and self.bullets[0].state == 'ready':
                            mixer.Sound('Audio/laser_shot.wav').play()
                            self.bullets[0].fire(player.x - 15)
                            self.bullets[1].fire(player.x + 15)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                        player.mov_x = 0

            player.move()
            player.draw(self.screen)

            if self.personagem_selecionado == 'nave1':
                bullet.move()
                bullet.draw(self.screen)
                for enemy in inimigos: #for que testa se acertou o inimigo
                    if bullet.is_collision(enemy):
                        mixer.Sound('Audio/explosion1.mp3').play() #aúdio de tiro
                        bullet.y = 720
                        bullet.state = 'ready'
                        self.score_value += 2 if not isinstance(enemy, Inimigo) or isinstance(enemy, Inimigo3) else 1 #2 pontos para o inimigo 2 e 3, e 1 para o boca
                        enemy.reset_position()
            else: # Se for nave2
                for bullet in self.bullets:
                    bullet.move()
                    bullet.draw(self.screen)
                    for enemy in inimigos:
                        if bullet.is_collision(enemy):
                            mixer.Sound('Audio/explosion1.mp3').play()
                            bullet.y = 720
                            bullet.state = 'ready'
                            self.score_value += 2 if not isinstance(enemy, Inimigo) or isinstance(enemy, Inimigo3) else 1
                            enemy.reset_position()

            for enemy in inimigos: #for para mover e desenhar o inimigo
                enemy.move()
                enemy.draw(self.screen)
                if enemy.power.is_collision(player):
                    mixer.Sound('Audio/morte.wav').play()
                    running = False
                    break 

            self.mostrar_score(10, 10) #mostra score no canto superior esquerdo
            pygame.display.update() #atualiza a tela
        
        self.game_over_screen()#quando running==false abre a tela de game over

    def run(self):
        while True:
            try:
                self.personagem_selecionado = self._menu.mostrarMenu()
                if self.personagem_selecionado == 'view_scores': #se apertar o botão de score irá alterar o valor do personagem e abrir a tela score
                    self._menu.mostrarScore()
                else:
                    self.game() #senão roda o jogo
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                exit()

if __name__ == "__main__":
    try:
        game_instance = SpaceProtectors()
        game_instance.run()
    except Exception as e:
         print(f"Erro ao iniciar o jogo: {e}")
         exit()

                    





