import pygame, random, math, os, sys, datetime, pyttsx3
import speech_recognition as sr
import tkinter as tk
from comandos import startDatabase, cleanScreen, timeWait, nameInput, tela_boas_vindas
from tkinter import messagebox
import json

# Set working directory to script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
startDatabase()

# --- Configurações Iniciais ---
largura = 1000
altura = 700
fps = pygame.time.Clock()
tela = pygame.display.set_mode((largura, altura), 0)

icone_path = "recursos/gameIcon.png"
if os.path.exists(icone_path):
    icone = pygame.image.load(icone_path)
    pygame.display.set_icon(icone)

pygame.display.set_caption('Ataque a Horta')
pygame.mixer.music.load('recursos/gameMusic.mp3')

# --- Cores e Fontes ---
branco = (255, 255, 255)
preto = (0, 0, 0)
fonteMenu = pygame.font.SysFont('sans serif', 24)

# --- Configurações de Voz ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# --- Carregamento de Imagens ---
fundo_incial = pygame.image.load("recursos/startScreen.png")
fundo_jogo = pygame.image.load("recursos/background.png") # Carrega a imagem de fundo do jogo
fundo_jogo = pygame.transform.scale(fundo_jogo, (largura, altura)) # Garante que ela preencha a tela

personagem_img_direita = pygame.image.load("recursos/mainChracter.png")
personagem_img_direita = pygame.transform.scale(personagem_img_direita, (300, 150))
personagem_img_esquerda = pygame.transform.flip(personagem_img_direita, True, False)
projetil_img = pygame.image.load("recursos/enemyProjetil.png")
projetil_img = pygame.transform.scale(projetil_img, (80, 80))
inimigo_img = pygame.image.load("recursos/enemy.png")
inimigo_img = pygame.transform.scale(inimigo_img, (300, 300))
tela_de_morte = pygame.image.load("recursos/dieScreen.png")

# --- Variáveis Globais ---
nome = ""
pontuacao = 0

# --- Funções de Desenho da Animação ---
def draw_sun(surface, center, radius, angle):
    """Desenha um sol girando."""
    rays = 8
    for i in range(rays):
        rad = math.radians(i * 360 / rays + angle)
        x = center[0] + math.cos(rad) * (radius + 20)
        y = center[1] + math.sin(rad) * (radius + 20)
        pygame.draw.line(surface, (255, 255, 0), center, (x, y), 3)
    pygame.draw.circle(surface, (255, 255, 0), center, radius)

def draw_cloud(surface, x, y):
    """Desenha uma nuvem simples."""
    pygame.draw.circle(surface, (255, 255, 255), (int(x), y), 20)
    pygame.draw.circle(surface, (255, 255, 255), (int(x + 20), y + 10), 20)
    pygame.draw.circle(surface, (255, 255, 255), (int(x - 20), y + 10), 20)

# --- Funções do Jogo ---
def iniciar_jogo():
    global nome, pontuacao
    # Variáveis do personagem e jogo
    personagem_x = largura // 2 - 50
    personagem_y = altura - 150
    velocidade = 15
    projetil_x = random.randint(0, largura - 80)
    projetil_y = -80
    velocidade_projetil = 2
    aumento_velocidade = 0.01
    inimigo_x = largura // 2 - 150
    inimigo_y = 50
    inimigo_velocidade = 1
    olhando_direita = True
    pontuacao = 0
    pygame.mixer.music.play(-1)
    rodando = True
    pausado = False

    # Variáveis da animação de fundo
    sun_center = (largura - 100, 100)
    sun_radius = 50
    sun_angle = 0
    cloud_x = 60
    cloud_y = 70
    cloud_direction = 1

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if pausado:
            texto_pausa = fonteMenu.render("JOGO PAUSADO - Pressione ESPAÇO para voltar", True, branco)
            texto_rect = texto_pausa.get_rect(center=(largura // 2, altura // 2))
            tela.blit(texto_pausa, texto_rect)
            pygame.display.update()
            fps.tick(10)
            continue
        
        # --- LÓGICA DO JOGO ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            personagem_x -= velocidade
            olhando_direita = False
        if teclas[pygame.K_RIGHT]:
            personagem_x += velocidade
            olhando_direita = True

        personagem_x = max(0, min(personagem_x, largura - 300))
        personagem_img = personagem_img_direita if olhando_direita else personagem_img_esquerda

        projetil_y += velocidade_projetil
        velocidade_projetil += aumento_velocidade

        if projetil_y > altura:
            projetil_x = random.randint(0, largura - 80)
            projetil_y = -80
            pontuacao += 10

        personagem_rect = pygame.Rect(personagem_x + 100, personagem_y + 30, 100, 100)
        projetil_rect = pygame.Rect(projetil_x + 15, projetil_y + 15, 50, 50)

        if personagem_rect.colliderect(projetil_rect):
            game_over()
            return

        inimigo_x += inimigo_velocidade
        if inimigo_x <= 0 or inimigo_x >= largura - 300:
            inimigo_velocidade *= -1

        # --- LÓGICA DE DESENHO ---
        # 1. Atualiza e desenha a animação sobre o fundo
        sun_angle += 0.5
        cloud_x += cloud_direction * 0.2
        if cloud_x < 40 or cloud_x > largura - 40:
            cloud_direction *= -1

        tela.blit(fundo_jogo, (0, 0)) # DESENHA A IMAGEM DE FUNDO
        draw_sun(tela, sun_center, sun_radius, sun_angle)
        draw_cloud(tela, cloud_x, cloud_y)

        # 2. Desenha os elementos do jogo por cima de tudo
        tela.blit(inimigo_img, (inimigo_x, inimigo_y))
        tela.blit(personagem_img, (personagem_x, personagem_y))
        tela.blit(projetil_img, (projetil_x, projetil_y))

        # 3. Desenha a pontuação (UI)
        texto_pontuacao = fonteMenu.render(f"Pontuação: {pontuacao}", True, branco)
        tela.blit(texto_pontuacao, (10, altura - texto_pontuacao.get_height() - 10))

        pygame.display.update()
        fps.tick(60)

def game_over():
    global nome, pontuacao
    pygame.mixer.music.stop()
    agora = datetime.datetime.now()
    data_hora = agora.strftime("%d/%m/%Y - (%H:%M:%S)")
    novo_registro = f"Jogador: {nome} - Pontuação: {pontuacao} - Data/Hora: {data_hora}\n"
    with open("log.dat", "a") as arquivo:
        arquivo.write(novo_registro)

    try:
        with open("log.dat", "r") as arquivo:
            linhas = arquivo.readlines()
            ultimos_registros = linhas[-5:]
    except FileNotFoundError:
        ultimos_registros = []

    fonte_botao = pygame.font.SysFont('comicsans', 30)
    texto_restart = fonte_botao.render("Jogar Novamente", True, preto)
    texto_sair = fonte_botao.render("Sair", True, preto)
    botao_restart = texto_restart.get_rect(center=(largura // 2, altura // 2 + 150))
    botao_sair = texto_sair.get_rect(center=(largura // 2, altura // 2 + 200))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if botao_restart.collidepoint(mouse_pos):
                    iniciar_jogo()
                    return
                elif botao_sair.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        tela.blit(tela_de_morte, (0, 0))
        # fonte_gameover = pygame.font.SysFont('comicsans', 72)
        # texto_gameover = fonte_gameover.render("GAME OVER", True, (255, 0, 0))
        # tela.blit(texto_gameover, (largura // 2 - texto_gameover.get_width() // 2, altura // 4))

        fonte_pontuacao = pygame.font.SysFont('comicsans', 32)
        texto_pontos = fonte_pontuacao.render(f"Pontuação final: {pontuacao}", True, branco)
        tela.blit(texto_pontos, (largura // 2 - texto_pontos.get_width() // 2, altura // 2 - 50))

        fonte_registro = pygame.font.SysFont('comicsans', 20)
        y_offset = altura // 2
        for registro in reversed(ultimos_registros):
            registro_limpo = registro.strip()
            texto_log = fonte_registro.render(registro_limpo, True, branco)
            tela.blit(texto_log, (largura // 2 - texto_log.get_width() // 2, y_offset))
            y_offset += 25

        pygame.draw.rect(tela, branco, botao_restart.inflate(10, 10), border_radius=5)
        pygame.draw.rect(tela, branco, botao_sair.inflate(10, 10), border_radius=5)
        tela.blit(texto_restart, botao_restart)
        tela.blit(texto_sair, botao_sair)

        pygame.display.update()
        fps.tick(60)

def jogar():
    largura_janela = 400
    altura_janela = 100

    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome.strip():
            messagebox.showwarning("Aviso", "Por favor, fale ou digite seu nome!")
        else:
            root.destroy()
            tela_boas_vindas(tela, largura, branco, preto, fps, nome, iniciar_jogo)

    def falar_nome_callback():
        nome_falado = nameInput()
        if nome_falado:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, nome_falado)

    def ao_fechar_janela():
        messagebox.showwarning("Aviso", "Você precisa falar ou digitar um nome para continuar!")

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    root.title("Nickname")
    root.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    label_instrucao = tk.Label(root, text="Fale ou digite seu nickname:")
    label_instrucao.pack(pady=5)
    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=5)
    frame_botoes = tk.Frame(root)
    frame_botoes.pack(pady=5)
    botao_falar = tk.Button(frame_botoes, text="Falar", command=falar_nome_callback)
    botao_falar.pack(side=tk.LEFT, padx=5)
    botao_ok = tk.Button(frame_botoes, text="OK", command=obter_nome)
    botao_ok.pack(side=tk.LEFT, padx=5)
    root.mainloop()

def start():
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    startButton = pygame.Rect(25, 12, 150, 40)
    quitButton = pygame.Rect(25, 62, 150, 40)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(mouse_pos):
                    jogar()
                if quitButton.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        tela.blit(fundo_incial, (0, 0))

        sombra_start = fonteMenu.render("Iniciar Game", True, (50, 50, 50))
        startTexto = fonteMenu.render("Iniciar Game", True, branco)
        tela.blit(sombra_start, (startButton.x + 2, startButton.y + 2))
        tela.blit(startTexto, (startButton.x, startButton.y))

        sombra_quit = fonteMenu.render("Sair do Game", True, (50, 50, 50))
        quitTexto = fonteMenu.render("Sair do Game", True, branco)
        tela.blit(sombra_quit, (quitButton.x + 2, quitButton.y + 2))
        tela.blit(quitTexto, (quitButton.x, quitButton.y))
        
        if startButton.collidepoint(mouse_pos) or quitButton.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()
        fps.tick(60)

# --- Inicia o Jogo ---
start()