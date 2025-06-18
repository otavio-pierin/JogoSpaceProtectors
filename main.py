import pygame
import random
from pygame import mixer
from jogador import Jogador
from inimigo import Inimigo
from inimigo2 import Inimigo2
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
    def bullets(self, valor:list):
        self.__bullets = valor
    
    #salvar pontuação
    def salvar_score(self):
        try:
            with open("log.txt", "a") as file: #a -> append
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
        self.salvar_score()
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
            pygame.display.update()
    # def game(self):
        self.score_value = 0
        try:
            #Carrega a música
            mixer.music.play(-1)

            #Personagem selecionado
            #Bala da nave1 (única) ou lista de balas para nave2 (dupla)
            if self.personagem_selecionado == "nave1":
                player_image = 'Image/nave1.png'
                bullet = Bullet(0, 720, 'Image/laser_amarelo.png', 10) #bala única                
            else:
                player_image = 'Image/nave2.png'
                self.bullets = [Bullet(0,720, 'Image/laser_amarelo.png', 5), Bullet(5,720,'Image/laser_amarelo.png',5)] #Lista das balas da nave2                
            
            player = Jogador(370, 720, player_image)

            #Inimigos tipo 1, 2 e 3
            enemies = [Inimigo(random.randint(0,950), random.randint(50,150),6, 20, 'Image/inimigo5.png', 1, 'Image/poderenemy.png') for _ in range(5)] #gera 5 inimigos
            enemy_size = enemies[0].image.get_size()
            enemies2 = [Inimigo2(random.randint(0,950), random.randint(50,150),3.0, 20, 'Image/inimigo4.png', 1.0, 'Image/poderenemy2.png', (60,60)) for _ in range(6)] #gera 6 inimigos do tipo 2
            enemies3 = [Inimigo3(random.randint(0,950), random.randint(50,150),4.5, 20, 'Image/inimigo3.png', 1.0, 'Image/laser_vermelho.png', (60,60)) for _ in range(3)] #gera 3 inimigos do tipo 3
           
            #Movimentação do jogador
            running = True
            while running:
                self.screen.fill((0,0,0))
                self.screen.blit(self.background, (0,0))

                for event in pygame.event.get(): #captura evento dos periféricos
                    if event.type == pygame.QUIT:
                        running = False
                    
                    if event.type == pygame.KEYDOWN: #se apertar alguma tecla
                        if event.key == pygame.K_LEFT:
                            player.mov_x(-4)
                        if event.key == pygame.K_RIGHT:
                            player.mov_x(4)
                        if event.key == pygame.K_SPACE:
                            if self.personagem_selecionado == 'nave1' and bullet.state == "ready":
                                bulletSound = mixer.Sound('Audio/laser_shot.wav')
                                bulletSound.play()
                                bullet.fire(player.x)
                            elif self.personagem_selecionado == 'nave2' and self.bullets[0].state == 'ready':
                                bulletSound = mixer.Sound('Audio/laser_shot.wav')
                                bulletSound.play()
                                self.bullets[0].fire(player.x-10) #bala esquerda
                                self.bullets[1].fire(player.x + 10) #bala direita

                    if event.type == pygame.KEYUP: #se soltar a mudança de x se torna 0 e o jogador fica parado
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #último evento for <- ou ->
                            player.mov_x(0)

                player.move() #atualiza local da nave
                player.draw(self.screen) #desenha a nave
            
                #Movimentar e desenhar os inimigos, se for nave1 já compara se acertou
                for enemy in enemies:
                    enemy.move()
                    if self.personagem_selecionado == 'nave1' and bullet.is_collision(enemy):
                        somExplosao = mixer.Sound('Audio/explosion1.mp3')
                        somExplosao.play()
                        bullet.y = 720
                        bullet.state = 'ready'
                        self.score_value +=1
                        enemy.reset_position()
                    enemy.draw(self.screen)
                
                for enemy2 in enemies2:
                    enemy2.move()
                    if self.personagem_selecionado == 'nave1' and bullet.is_collision(enemy2):
                        somExplosao = mixer.Sound('Audio/explosion1.mp3')
                        somExplosao.play()
                        bullet.y = 720
                        bullet.state = 'ready'
                        self.score_value +=2 #vale 2 pontos se acertar
                        enemy2.reset_position()
                    enemy2.draw(self.screen)

                for enemy3 in enemies3:
                    enemy3.move()
                    if self.personagem_selecionado == 'nave1' and bullet.is_collision(enemy3):
                        somExplosao = mixer.Sound('Audio/explosion1.mp3')
                        somExplosao.play()
                        bullet.y = 720
                        bullet.state = 'ready'
                        self.score_value +=2 #2 pontos se acertar
                        enemy3.reset_position()                        
                    enemy3.draw(self.screen)

                #Monimentar as desenhar as balas da nave2
                if  self.personagem_selecionado == 'nave2':
                    for bullet in self.bullets:
                        bullet.move()
                        bullet.draw(self.screen)

                        for enemy in enemies + enemies2 + enemies3:
                            if bullet.is_collision(enemy):
                                somExplosao = mixer.Sound('Audio/explosion1.mp3')
                                somExplosao.play()
                                bullet.y = 720
                                bullet.state = 'ready'
                                #comparar se o acertado foi do tipo 1, dois ou 3
                                if isinstance(enemy, Inimigo):
                                    self.score_value +=1
                                elif isinstance(enemy, Inimigo2) or isinstance(enemy,Inimigo3):
                                    self.score_value +=2
                                enemy.reset_position()
                    
                #verifica se acertou o jogador
                for enemy in enemies + enemies2 + enemies3:
                    if enemy.power.is_collision(player): #se colidiu com o jogador
                        somFim = mixer.Sound('Audio/morte.wav')
                        somFim.play()
                        running = False #termina o jogo
                        break
                    
                if not running: #se terminou o jogo
                    self.game_over_screen()
                    return
                else: #movimentar bala para nave1
                    bullet.move()
                    bullet.draw(self.screen)
        
        except pygame.error as e:
            print(f"Erro durante a execução do jogo: {e}")
            exit()       
    
    # Em main.py, substitua sua função game por esta:
    def game(self):
        self.score_value = 0
        
        # --- CONFIGURAÇÃO INICIAL DO JOGO ---
        try:
            mixer.music.play(-1)

            if self.personagem_selecionado == "nave1":
                player_image = 'Image/nave1.png'
                bullet = Bullet(0, 720, 'Image/laser_amarelo.png', 10)
            else: # Se for nave2
                player_image = 'Image/nave2.png'
                caminho_bala_nave2 = 'Image/laser_amarelo.png' # Use o nome real do seu arquivo
                self.bullets = [Bullet(0, 720, caminho_bala_nave2, 5), Bullet(0, 720, caminho_bala_nave2, 4)]

            player = Jogador(370, 720, player_image)

            inimigos = []
            inimigos.extend([Inimigo(random.randint(0,950), random.randint(50,150), 6, 20, 'Image/inimigo5.png', 1, 'Image/poderenemy.png') for _ in range(5)])
            inimigos.extend([Inimigo2(random.randint(0,950), random.randint(50,150), 3.0, 20, 'Image/inimigo4.png', 1.0, 'Image/poderenemy2.png', (60,60)) for _ in range(6)])
            inimigos.extend([Inimigo3(random.randint(0,950), random.randint(50,150), 4.5, 2, 'Image/inimigo3.png', 2.0, 'Image/laser_vermelho.png', (60,60)) for _ in range(3)])

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
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.mov_x = -4
                    if event.key == pygame.K_RIGHT:
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
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.mov_x = 0

            player.move()
            player.draw(self.screen)

            if self.personagem_selecionado == 'nave1':
                bullet.move()
                bullet.draw(self.screen)
                for enemy in inimigos:
                    if bullet.is_collision(enemy):
                        mixer.Sound('Audio/explosion1.mp3').play()
                        bullet.y = 720
                        bullet.state = 'ready'
                        self.score_value += 2 if not isinstance(enemy, Inimigo) or isinstance(enemy, (Inimigo2, Inimigo3)) else 1
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
                            self.score_value += 2 if not isinstance(enemy, Inimigo) or isinstance(enemy, (Inimigo2, Inimigo3)) else 1
                            enemy.reset_position()

            for enemy in inimigos:
                enemy.move()
                enemy.draw(self.screen)
                if enemy.power.is_collision(player):
                    mixer.Sound('Audio/morte.wav').play()
                    running = False
                    break 

            self.mostrar_score(10, 10)
            pygame.display.update()
        
        self.game_over_screen()

    def run(self):
        while True:
            try:
                self.personagem_selecionado = self._menu.mostrarMenu()
                if self.personagem_selecionado == 'view_scores':
                    self._menu.mostrarScore()
                else:
                    self.game()
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                exit()

if __name__ == "__main__":
    # try:
    game_instance = SpaceProtectors()
    game_instance.run()
    # except Exception as e:
    #     print(f"Erro ao iniciar o jogo: {e}")
    #     exit()

                    





