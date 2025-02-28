import pygame
from lutador import Lutador

#----------|inicia o jogo|----------------------------------------------------------------------------------------------
pygame.init()

#----------|faz a musica tocar no jogo|---------------------------------------------------------------------------------
musica_tema_tocando = True
if musica_tema_tocando:
    pygame.mixer.music.load("musica_tema.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

#----------|nome do game|-----------------------------------------------------------------------------------------------
pygame.display.set_caption("Medieval Fight")

#----------|carrega o ícone do jogo pro game/define o ícone do game|----------------------------------------------------
icone = pygame.image.load("icone.png")
pygame.display.set_icon(icone)

#----------|dimenções da tela|------------------------------------------------------------------------------------------
largura = 1152
altura = 648

#----------|define a altura do chão|------------------------------------------------------------------------------------
cord_chao = 580

#----------|cria a tela onde o jogo será exibido|-----------------------------------------------------------------------
tela = pygame.display.set_mode((largura, altura))

#----------|carregar a imagem do fundo para game/modifica a escala para se adequar a tela|------------------------------
fundo = pygame.image.load("background.png").convert_alpha()
fundo = pygame.transform.smoothscale(fundo, ((largura, altura)))

#----------|carrega as sprites da memoria pro game|---------------------------------------------------------------------
cavaleiro_sheet = pygame.image.load("Cavaleiro/cavaleiro.png").convert_alpha()
orc_sheet = pygame.image.load("Orc/Orc.png").convert_alpha()

#----------|numero de frames em cada animação|--------------------------------------------------------------------------
num_animacoes_cav = [6,8,6,6,4,4]
num_animacoes_orc = [6,8,6,6,4,4]

#----------|definir dados dos jogadores|--------------------------------------------------------------------------------
tamanho_frame_spritesheet = 100
escala_jogadores = 9
dadosCav = {"tamanho":tamanho_frame_spritesheet, "escala":escala_jogadores}
dadosOrc = {"tamanho":tamanho_frame_spritesheet, "escala":escala_jogadores}

#----------|FPS em que o jogo vai rodar|--------------------------------------------------------------------------------
clock = pygame.time.Clock()
FPS = 60

#----------|fontes estilizadas do game|---------------------------------------------------------------------------------
nome_estilo = pygame.font.Font("fonte_padrao.TTF", 40)
score_estilo = pygame.font.Font("fonte_padrao.TTF", 30)
vitoria_estilo = pygame.font.Font("fonte_padrao.TTF", 60)
aviso = pygame.font.Font("fonte_padrao.TTF", 25)
tela_pause_fonte = pygame.font.Font("fonte_padrao.TTF", 60)
mini_aviso_fonte = pygame.font.Font("fonte_padrao.TTF", 30)

#----------|cores utilizadas no game|-----------------------------------------------------------------------------------
GREEN = (0,245,0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
YELLOW = (255,215,0)

#----------|score dos jogadores|----------------------------------------------------------------------------------------
score = {"P1_score":0,"P2_score":0}

#----------|var responsavel por saber se o jogo foi pausado|------------------------------------------------------------
game_pause = False

#----------|var responsável por saber quando acaba o round|-------------------------------------------------------------
round_over = False

#----------|var responsável por saber se houve vitoria|-----------------------------------------------------------------
vitoria_status = False

#----------|texto dos nomes|--------------------------------------------------------------------------------------------
nome_cav = nome_estilo.render("CAVALEIRO", True, WHITE)
nome_orc = nome_estilo.render("ORC", True, WHITE)

#----------|função que desenha as barras de vida|-----------------------------------------------------------------------
def draw_vida(vida, x, y, superficie):
    percentual_vida = vida / 100
    #desenha retângulos que representam a vida
    pygame.draw.rect(superficie, BLACK, (x - 1, y - 1, 402, 28))
    pygame.draw.rect(superficie, RED, (x, y, 400, 25))
    pygame.draw.rect(superficie, GREEN, (x, y, 400 * percentual_vida, 25))

#----------|função que desenha a tela de vitoria na tela|---------------------------------------------------------------
def vitoria(jogador,superficie):
    if jogador == 1:
        vitoria_player = vitoria_estilo.render("O CAVALEIRO VENCEU",True, YELLOW)
        superficie.blit(vitoria_player,(128,284))
    if jogador == 2:
        vitoria_player = vitoria_estilo.render("O ORC VENCEU",True, YELLOW)
        superficie.blit(vitoria_player,(232,284))

#----------|elementos da tela de pause|---------------------------------------------------------------------------------
tela_pause_fundo = pygame.Surface((largura, altura), pygame.SRCALPHA)
tela_pause_fundo.fill((0, 0, 0, 200))
aviso_tela_pause = tela_pause_fonte.render("GAME PAUSADO", True, WHITE)
mini_aviso_pause = mini_aviso_fonte.render("Pressione P para continuar", True, WHITE)

#----------|função que desenha a tela de pause na tela|-----------------------------------------------------------------
def desenha_tela_pause(superficie):
    superficie.blit(tela_pause_fundo, (0, 0))
    superficie.blit(aviso_tela_pause, (250, 250))
    superficie.blit(mini_aviso_pause, (255, 350))

#----------|instancia dos jogadores|------------------------------------------------------------------------------------
jogador1 = Lutador(1, 220,390, False, dadosCav, cavaleiro_sheet, num_animacoes_cav)
jogador2 = Lutador(2, 845,400, True, dadosOrc, orc_sheet, num_animacoes_orc)

#----------|loop principal do game|-------------------------------------------------------------------------------------
rodando = True
while rodando:
    clock.tick(FPS)
    #-----|busca se algum evento aconteceu|-----------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #-----|verifica se a tecla de pause foi pressionada|------------------------------------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and game_pause == False:
                game_pause = True
            elif event.key == pygame.K_p and game_pause == True:
                game_pause = False
    #-----|desenha a imagem de fundo na tela|---------------------------------------------------------------------------
    tela.blit(fundo, (0, 0))

    #-----|desenha os status do personagem na tela|---------------------------------------------------------------------
    draw_vida(jogador1.vida, 20, 40, tela)
    draw_vida(jogador2.vida, 732, 40, tela)

    #-----|movimentação e ataque|---------------------------------------------------------------------------------------
    jogador1.movimento(jogador2,cord_chao, game_pause)
    jogador2.movimento(jogador1,cord_chao, game_pause)

    #-----|atualiza as ações dos jogadores, como frame atual da imagem, estados e ações|--------------------------------
    jogador1.atualizar()
    jogador2.atualizar()

    #-----|desenha os jogadores na tela|--------------------------------------------------------------------------------
    jogador1.desenha_personagem(tela)
    jogador2.desenha_personagem(tela)

    #-----|cria o texto dos scores|-------------------------------------------------------------------------------------
    score_1 = score_estilo.render("P1: " + str(score["P1_score"]), True, WHITE)
    score_2 = score_estilo.render("P2: " + str(score["P2_score"]), True, WHITE)

    #-----|desenha os scores na tela|-----------------------------------------------------------------------------------
    tela.blit(score_1,(20,70))
    tela.blit(score_2,(732,70))

    #-----|desenhar os nomes dos jogadores na tela|---------------------------------------------------------------------
    tela.blit(nome_cav,(20,14))
    tela.blit(nome_orc, (732, 14))

    #-----|checar se algum jogador morreu|------------------------------------------------------------------------------
    if round_over == False:
        if jogador1.vivo == False:
            score["P2_score"] += 1
            round_over = True
        elif jogador2.vivo == False:
            score["P1_score"] += 1
            round_over = True
    #-----|se um jogador morreu, o round acaba e executa os seguintes comandos|------------------------------------------
    elif round_over == True:
        #-----|desenha o aviso de pressionar espaço para a próxima partida|---------------------------------------------
        aviso_pressionar = aviso.render("Pressione SPACE para a proxima partida", True, BLACK)
        tela.blit(aviso_pressionar, (206,600))

        #-----|se houver vitoria, desenha a tela de vitoria|------------------------------------------------------------
        if vitoria_status == True:
            if score["P1_score"] == 2:
                vitoria(1, tela)
            if score["P2_score"] == 2:
                vitoria(2, tela)

        #-----|verifica se a de tecla espaço foi pressionada|-----------------------------------------------------------
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and game_pause == False:

            #-----|se a tecla espaço foi pressionada, reinicia o round|------------------------------------------------
            if vitoria_status == False:
                round_over = False
                jogador1 = Lutador(1, 220, 390, False, dadosCav, cavaleiro_sheet, num_animacoes_cav)
                jogador2 = Lutador(2, 845, 400, True, dadosOrc, orc_sheet, num_animacoes_orc)

            #-----|se a tecla de espaço foi pressionada e houve vitoria, reinicia o round e os pontos|-------------------------------
            if vitoria_status == True:
                vitoria_status = False
                score["P1_score"], score["P2_score"] = 0, 0
                round_over = False
                jogador1 = Lutador(1, 220, 390, False, dadosCav, cavaleiro_sheet, num_animacoes_cav)
                jogador2 = Lutador(2, 845, 400, True, dadosOrc, orc_sheet, num_animacoes_orc)

    #-----|verifica se algum dos players ganhou|------------------------------------------------------------------------
    if score["P1_score"] == 2 or score["P2_score"] == 2:
        vitoria_status = True

    #-----|se o jogo tá pausado, desenha a tela de pause usando a func|-------------------------------------------------
    if game_pause == True:
        desenha_tela_pause(tela)

    #-----|atualiza a tela|---------------------------------------------------------------------------------------------
    pygame.display.update()

