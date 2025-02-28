import pygame
class Lutador:
    def __init__(self, jogador, x, y, flip, dados, sprite_sheet, frames_animacao):
        self.jogador = jogador                        #definir P1/P2
        self.tamanho = dados["tamanho"]               #tamanho dos frames dos personagens conforme a spritesheet
        self.escala = dados["escala"]                 #escala do tamanho do personagem na tela
        self.flip = flip                              #virar axis x do personagem, para manter os personagens cara a cara

        #armazenando as animações possíveis para o personagem na forma de uma matriz
        self.lista_animacao = self.carregar_imagens(sprite_sheet, frames_animacao)
        #definir a acao atual do personagem
        self.acao = 0 #parado:0, correndo:1, ataque_1:2, ataque_2:3, dano:5, morto:6
        # definir index do frame atual
        self.index_img = 0
        # imagem atual de acordo com a ação e o index atual
        self.imagem = self.lista_animacao[self.acao][self.index_img]
        self.atualiza_tempo = pygame.time.get_ticks() #atualizacao do tempo da imagem
        self.rect = pygame.Rect(x, y, 90, 180)        #posiçao do personagem e tamanho
        self.vel_y = 0                                #variação de velocidade de y
        self.correndo = False                         #estado de corrida do personagem
        self.pulando = False                          #estado de pulo
        self.tipo_ataque = 0                          #tipo do ataque atual realizado
        self.counter_ataques = [0, 0]                 #contagem de ataques do personagem
        self.tempo_espera_ataque = 0                  #tempo de espera para o próximo ataque
        self.atacando = False                         #estado de ataque
        self.dano = False                             #levou dano
        self.vida = 100                               #quantidade de vida
        self.vivo = True                              #estado vivo/morto

    #-----|função responsavel por extrair as imagens da spritesheet|----------------------------------------------------
    def carregar_imagens(self, sprite_sheet, frames_animacao):
        lista_final_animacao = []
        y = 0
        for animacao in frames_animacao:
            lista_temp_animacao = []
            for x in range(animacao):
                img_temp = sprite_sheet.subsurface(x * self.tamanho,y * self.tamanho, self.tamanho, self.tamanho)
                lista_temp_animacao.append(pygame.transform.scale(img_temp, (self.tamanho*self.escala, self.tamanho*self.escala)))
            y += 1
            lista_final_animacao.append(lista_temp_animacao)
        return lista_final_animacao

    #-----|função responsavel pela movimentação do personagem em geral (mover, ataque, pulo, etc)|----------------------
    def movimento(self, alvo, cord_chao, game_pausado):
        #---|velocidade padrão do jogador ao se movimentar|-------------------------------------------------------------
        velocidade_personagem = 10
        #---|variação das posições do personagem no plano|
        delta_x = 0
        delta_y = 0
        #---|valor gravitacional|---------------------------------------------------------------------------------------
        gravidade = 2
        #---|atualiza o status de correndo pra false a cada iteração da função|-----------------------------------------
        self.correndo = False
        #---|atualiza o status do tipo de ataque pra 0 a cada iteração da função|---------------------------------------
        self.tipo_ataque = 0

        #---|verifica teclas pressionadas|------------------------------------------------------------------------------
        key = pygame.key.get_pressed()

        #---|só pode realizar ações se atacando == False e estiver vivo|------------------------------------------------
        if self.atacando == False and self.vivo == True and game_pausado == False:
            #---|definir movimentação jogador 1|------------------------------------------------------------------------
            if self.jogador == 1:
                #mover delta x/direita e esquerda
                if key[pygame.K_a]:
                    delta_x = -velocidade_personagem
                    self.correndo = True
                if key[pygame.K_d]:
                    delta_x = velocidade_personagem
                    self.correndo = True

                #se o botão de ataque for pressionado, realiza o ataque correspondente
                if key[pygame.K_r]:
                    self.atacando = True
                    self.ataque(alvo, 1)
                    self.tipo_ataque = 1
                    self.counter_ataques[0] += 1
                    #o ataque especial só pode ser realizado após 3 ataques normais
                if key[pygame.K_t] and self.counter_ataques[0] >= 3:
                    self.atacando = True
                    self.ataque(alvo, 2)
                    self.tipo_ataque = 2
                    self.counter_ataques[0] = 0

                #realiza um pulo, ativando a velocidade de y com um valor
                if key[pygame.K_w] and self.pulando == False:
                    self.vel_y = -30
                    self.pulando = True

            #definir jogador 2
            if self.jogador == 2:
                #mover delta x
                if key[pygame.K_LEFT]:
                    delta_x = -velocidade_personagem
                    self.correndo = True
                if key[pygame.K_RIGHT]:
                    delta_x = velocidade_personagem
                    self.correndo = True
                #ataque
                if key[pygame.K_KP1]:
                    self.atacando = True
                    self.ataque(alvo, 1)
                    self.tipo_ataque = 1
                    self.counter_ataques[1] += 1
                if key[pygame.K_KP2] and self.counter_ataques[1] >= 3:
                    self.atacando = True
                    self.ataque(alvo, 2)
                    self.tipo_ataque = 2
                    self.counter_ataques[1] = 0
                #pulo
                if key[pygame.K_UP] and self.pulando == False:
                    self.vel_y = -30
                    self.pulando = True

        #---|somando o valor da velocidade de y|------------------------------------------------------------------------
        delta_y += self.vel_y

        #---|atualizar a posição do player|-----------------------------------------------------------------------------
        self.rect.x += delta_x
        self.rect.y += delta_y

        #---|gravidade|-------------------------------------------------------------------------------------------------
        self.vel_y += gravidade
        delta_y += self.vel_y

        #---|delimitar bordas da tela|----------------------------------------------------------------------------------
        if self.rect.right >= 1152:
            self.rect.right = 1152
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= cord_chao :
            self.rect.bottom = cord_chao
            self.pulando = False

        #---|manter os personagens cara-a-cara|-------------------------------------------------------------------------
        if alvo.rect.centerx > self.rect.centerx and self.vivo == True:
            self.flip = False
        else:
            self.flip = True

        #---|tempo de espera para o ataque|-----------------------------------------------------------------------------
        if self.tempo_espera_ataque > 0:
            self.tempo_espera_ataque -= 1
    #---|atualiza as ações do personagem e desenha na tela|-------------------------------------------------------------
    def atualizar(self):
        #---|checa, e atualiza o personagem de acordo com os status do personagem|--------------------------------------
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.atualiza_acao(5) #morto
        elif self.dano == True:
            self.atualiza_acao(4)
        elif self.atacando == True:
            if self.tipo_ataque == 1:
                self.atualiza_acao(2) #ataque 1
            elif self.tipo_ataque == 2:
                self.atualiza_acao(3) #ataque 2
        elif self.correndo == True:
            self.atualiza_acao(1) #correndo
        else:
            self.atualiza_acao(0) #parado

        #---|velocidade em que a animação é realizada|------------------------------------------------------------------
        tempo_espera = 70
        #atualiza imagem
        self.imagem = self.lista_animacao[self.acao][self.index_img]
        if pygame.time.get_ticks() - self.atualiza_tempo > tempo_espera:
            self.atualiza_tempo = pygame.time.get_ticks()
            self.index_img += 1

        #se a acao acabou retorna pro estado parado
        if self.index_img >= len(self.lista_animacao[self.acao]):
            self.index_img = 0

            #checar se morreu
            if self.vivo == False:
                self.index_img = len(self.lista_animacao[self.acao])-1
            else:
                self.index_img = 0
            #checar se o ataque foi executado
            if self.acao == 2 or self.acao == 3:
                self.atacando = False
                self.tempo_espera_ataque = 10
            #checar se parou de levar dano
            if self.acao == 4:
                self.dano = False
                self.atacando = False
                self.tempo_espera_ataque = 10

    def ataque(self, alvo, tipo_ataque):
        if self.tempo_espera_ataque == 0:
            self.atacando = True
            ataque_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if ataque_rect.colliderect(alvo.rect):
                if tipo_ataque == 1:
                    alvo.vida -= 10
                    alvo.dano = True
                if tipo_ataque == 2:
                    alvo.vida -= 20
                    alvo.dano = True

    def atualiza_acao(self, nova_acao):
        #checar se a nova acao é diferente da anterior
        if nova_acao != self.acao:
            self.acao = nova_acao
            #atualizar index da acao
            self.index_img = 0
            self.atualiza_tempo = pygame.time.get_ticks()

    def desenha_personagem(self, tela):
        img = pygame.transform.flip(self.imagem, self.flip, False)
        rec_imagem = img.get_rect()
        rec_imagem.center = self.rect.center
        tela.blit(img,rec_imagem)
