import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da Janela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cidade das Cinzas - Menu Principal")
relogio = pygame.time.Clock()

# Paleta de Cores Dark Blue (Sóbrio, Elegante e Sem Neon)
COR_BG = (12, 14, 18)            # Fundo chumbo quase preto
COR_PAINEL = (20, 24, 30)        # Cinza azulado bem escuro para os painéis
COR_BORDA_DARK = (40, 48, 58)    # Borda discreta
BRANCO_FOSCO = (215, 220, 225)   # Texto principal suave
CINZA_TEXTO = (110, 118, 128)    # Texto secundário fosco
AZUL_ESCURO = (30, 80, 150)      # Azul escuro sóbrio (substituindo o vermelho)
AZUL_HOVER = (40, 105, 190)      # Azul ligeiramente mais claro para feedback visual
CINZA_BARRA = (30, 34, 40)       # Fundo para os trilhos de controle (sliders)

# Fontes nativas do sistema
try:
    fonte_titulo = pygame.font.SysFont("impact", 74)
    fonte_subtitulo = pygame.font.SysFont("arial", 20, bold=True)
    fonte_menu = pygame.font.SysFont("arial", 22, bold=True)
    fonte_comum = pygame.font.SysFont("arial", 18)
except:
    fonte_titulo = pygame.font.Font(None, 80)
    fonte_subtitulo = pygame.font.Font(None, 26)
    fonte_menu = pygame.font.Font(None, 30)
    fonte_comum = pygame.font.Font(None, 22)

# Estados do Jogo
TELA_INICIAL = "inicial"
TELA_MENU = "menu"
TELA_CONFIG = "configuracoes"
TELA_CREDITOS = "creditos"
TELA_JOGAR = "jogar"
estado_atual = TELA_INICIAL

# Variáveis para a tela inicial (texto piscante)
tempo_texto = 0
mostrar_prompt = True

# Variáveis de Configuração
volume_musica = 80
volume_sfx = 90
resolucao_selecionada = 0
opcoes_resolucao = ["1920x1080 (FHD)", "1280x720 (HD)", "Janela"]

# Classe de Botões customizados (Dark Blue)
class Botao:
    def __init__(self, x, y, largura, altura, texto, acao):
        self.rect = pygame.Rect(x - largura // 2, y, largura, altura)
        self.texto = texto
        self.acao = acao
        self.hovered = False

    def desenhar(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            cor_borda = AZUL_HOVER
            cor_fundo = (25, 35, 50)  # Fundo levemente azulado ao passar o mouse
            deslocamento = 2
        else:
            self.hovered = False
            cor_borda = COR_BORDA_DARK
            cor_fundo = COR_PAINEL
            deslocamento = 0

        # Desenha a caixa do botão
        pygame.draw.rect(superficie, cor_fundo, self.rect.move(0, deslocamento), border_radius=4)
        pygame.draw.rect(superficie, cor_borda, self.rect.move(0, deslocamento), 1, border_radius=4)

        # Texto interno do botão
        cor_txt = BRANCO_FOSCO if not self.hovered else AZUL_HOVER
        texto_surf = fonte_menu.render(self.texto, True, cor_txt)
        texto_rect = texto_surf.get_rect(center=self.rect.move(0, deslocamento).center)
        superficie.blit(texto_surf, texto_rect)

    def checar_clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.acao()

# Ações das Telas
def acao_jogar():
    global estado_atual
    estado_atual = TELA_JOGAR

def acao_config():
    global estado_atual
    estado_atual = TELA_CONFIG

def acao_creditos():
    global estado_atual
    estado_atual = TELA_CREDITOS

def acao_voltar():
    global estado_atual
    estado_atual = TELA_MENU

# Instanciando botões do menu
botoes_menu = [
    Botao(LARGURA // 2, 280, 280, 50, "JOGAR", acao_jogar),
    Botao(LARGURA // 2, 350, 280, 50, "CONFIGURAÇÕES", acao_config),
    Botao(LARGURA // 2, 420, 280, 50, "CRÉDITOS", acao_creditos)
]

botao_voltar_config = Botao(LARGURA // 2, 480, 280, 50, "VOLTAR", acao_voltar)
botao_voltar_creditos = Botao(LARGURA // 2, 480, 280, 50, "VOLTAR", acao_voltar)
botao_voltar_jogo = Botao(LARGURA // 2, 450, 280, 50, "SAIR PARA O MENU", acao_voltar)

# Loop Principal
executando = True
while executando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            executando = False

        if estado_atual == TELA_INICIAL:
            # Qualquer clique ou tecla pressionada entra direto no Menu Principal
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                estado_atual = TELA_MENU

        elif estado_atual == TELA_MENU:
            for btn in botoes_menu:
                btn.checar_clique(evento)

        elif estado_atual == TELA_CONFIG:
            botao_voltar_config.checar_clique(evento)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                if 220 <= mouse_y <= 240 and 420 <= mouse_x <= 570:
                    volume_musica = int((mouse_x - 420) / 150 * 100)
                if 280 <= mouse_y <= 300 and 420 <= mouse_x <= 570:
                    volume_sfx = int((mouse_x - 420) / 150 * 100)
                if 340 <= mouse_y <= 370 and 420 <= mouse_x <= 570:
                    resolucao_selecionada = (resolucao_selecionada + 1) % len(opcoes_resolucao)

        elif estado_atual == TELA_CREDITOS:
            botao_voltar_creditos.checar_clique(evento)

        elif estado_atual == TELA_JOGAR:
            botao_voltar_jogo.checar_clique(evento)

    # Limpa a tela com o fundo escuro padrão
    tela.fill(COR_BG)

    # --- TELA INICIAL (SEM CARREGAMENTO, SÓ CLIQUE PARA INICIAR) ---
    if estado_atual == TELA_INICIAL:
        # Título do Jogo
        txt_titulo = fonte_titulo.render("CIDADE DAS CINZAS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, ALTURA // 3 + 20)))

        # Efeito de Piscar ("Blink") lento para o texto "CLIQUE PARA INICIAR"
        tempo_texto += 1
        if tempo_texto % 35 == 0:
            mostrar_prompt = not mostrar_prompt

        if mostrar_prompt:
            txt_prompt = fonte_subtitulo.render("CLIQUE PARA INICIAR", True, AZUL_ESCURO)
            tela.blit(txt_prompt, txt_prompt.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50)))

    # --- TELA DO MENU PRINCIPAL ---
    elif estado_atual == TELA_MENU:
        txt_titulo = fonte_titulo.render("CIDADE DAS CINZAS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, 150)))

        for btn in botoes_menu:
            btn.desenhar(tela)

    # --- TELA DE CONFIGURAÇÕES ---
    elif estado_atual == TELA_CONFIG:
        painel_rect = pygame.Rect(150, 80, 500, 440)
        pygame.draw.rect(tela, COR_PAINEL, painel_rect, border_radius=8)
        pygame.draw.rect(tela, COR_BORDA_DARK, painel_rect, 1, border_radius=8)

        txt_titulo = fonte_titulo.render("CONFIGS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, 140)))

        # Volume Música
        txt_vol_musica = fonte_menu.render("Volume Música:", True, BRANCO_FOSCO)
        tela.blit(txt_vol_musica, (180, 220))
        pygame.draw.rect(tela, CINZA_BARRA, (420, 230, 150, 6), border_radius=3)
        pygame.draw.rect(tela, AZUL_ESCURO, (420, 230, int(volume_musica * 1.5), 6), border_radius=3)
        pygame.draw.circle(tela, BRANCO_FOSCO, (420 + int(volume_musica * 1.5), 233), 6)

        # Volume SFX
        txt_vol_sfx = fonte_menu.render("Volume Geral:", True, BRANCO_FOSCO)
        tela.blit(txt_vol_sfx, (180, 280))
        pygame.draw.rect(tela, CINZA_BARRA, (420, 290, 150, 6), border_radius=3)
        pygame.draw.rect(tela, AZUL_ESCURO, (420, 290, int(volume_sfx * 1.5), 6), border_radius=3)
        pygame.draw.circle(tela, BRANCO_FOSCO, (420 + int(volume_sfx * 1.5), 293), 6)

        # Resolução
        txt_res = fonte_menu.render("Resolução:", True, BRANCO_FOSCO)
        tela.blit(txt_res, (180, 340))
        txt_res_val = fonte_comum.render(opcoes_resolucao[resolucao_selecionada], True, CINZA_TEXTO)
        tela.blit(txt_res_val, (420, 342))

        botao_voltar_config.desenhar(tela)

    # --- TELA DE CRÉDITOS (CORRIGIDA) ---
    elif estado_atual == TELA_CREDITOS:
        painel_rect = pygame.Rect(150, 80, 500, 440)
        pygame.draw.rect(tela, COR_PAINEL, painel_rect, border_radius=8)
        pygame.draw.rect(tela, COR_BORDA_DARK, painel_rect, 1, border_radius=8)

        txt_titulo = fonte_titulo.render("CRÉDITOS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, 140)))

        # Desenvolvedores (Centralizado de forma elegante)
        txt_desenv_title = fonte_menu.render("DESENVOLVIDO POR:", True, CINZA_TEXTO)
        tela.blit(txt_desenv_title, txt_desenv_title.get_rect(center=(LARGURA // 2, 220)))

        txt_nomes = fonte_menu.render("Christophe, João Paulo e Alessandro", True, BRANCO_FOSCO)
        tela.blit(txt_nomes, txt_nomes.get_rect(center=(LARGURA // 2, 260)))

        # Trilha Sonora (Centralizado abaixo dos desenvolvedores)
        txt_trilha_title = fonte_menu.render("TRILHA SONORA:", True, CINZA_TEXTO)
        tela.blit(txt_trilha_title, txt_trilha_title.get_rect(center=(LARGURA // 2, 330)))

        txt_trilha = fonte_menu.render("Ambient Metal", True, BRANCO_FOSCO)
        tela.blit(txt_trilha, txt_trilha.get_rect(center=(LARGURA // 2, 370)))

        botao_voltar_creditos.desenhar(tela)

    # --- TELA DE JOGO INICIADO (DEMO) ---
    elif estado_atual == TELA_JOGAR:
        painel_rect = pygame.Rect(150, 100, 500, 400)
        pygame.draw.rect(tela, COR_PAINEL, painel_rect, border_radius=8)
        pygame.draw.rect(tela, AZUL_ESCURO, painel_rect, 1, border_radius=8)

        txt_game = fonte_titulo.render("INICIADO", True, AZUL_ESCURO)
        tela.blit(txt_game, txt_game.get_rect(center=(LARGURA // 2, 180)))

        txt_p1 = fonte_subtitulo.render("Preparando simulação do jogo...", True, BRANCO_FOSCO)
        txt_p2 = fonte_comum.render("(Transição bem-sucedida para a gameplay)", True, CINZA_TEXTO)
        
        tela.blit(txt_p1, txt_p1.get_rect(center=(LARGURA // 2, 280)))
        tela.blit(txt_p2, txt_p2.get_rect(center=(LARGURA // 2, 330)))

        botao_voltar_jogo.desenhar(tela)

    # Atualiza a tela física
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()
