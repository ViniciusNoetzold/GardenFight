import os , time
import json
import tkinter
import speech_recognition as sr
import tkinter.messagebox as messagebox
from datetime import datetime

def cleanScreen():
    os.system('cls')
    
def timeWait(segundos):
    time.sleep(segundos)

def startDatabase():
    try:
        banco = open('log.dat', 'r')
    except:
        print('Banco de dados não encontrado, gerando...')
        banco = open('log.dat', 'w')


def nameInput():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Fale agora", "Por favor diga seu nome...")
        try:
            audio = recognizer.listen(source, timeout=5)
            nome_falado = recognizer.recognize_google(audio, language='pt-BR')
            return nome_falado
        except sr.UnknownValueError:
            messagebox.showerror("Erro", "Não entendi o que você falou. Tente novamente ou digite seu nome.")
        except sr.RequestError:
            messagebox.showerror("Erro", "Não foi possível conectar ao serviço de reconhecimento.")
        except sr.WaitTimeoutError:
            messagebox.showerror("Erro", "Tempo de espera excedido. Tente novamente.")
    return None

import pygame, sys

def tela_boas_vindas(tela, largura, branco, preto, fps, nome_jogador, iniciar_jogo):
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    rodando = False
                    iniciar_jogo()

        tela.fill(preto)

        titulo_fonte = pygame.font.SysFont('sans serif', 50)
        texto_fonte = pygame.font.SysFont('sans serif', 28)

        texto_bem_vindo = titulo_fonte.render(f"BEM-VINDO, {nome_jogador.upper()}!", True, branco)
        texto_jogo = texto_fonte.render("Você agora está no ataque a horta", True, branco)

        instrucoes = [
            "Instruções do Jogo:",
            "- Use as setas do teclado para mover o personagem",
            "- Desvie dos projéteis que caem do céu",
            "- Se você for atingido, o jogo acaba",
            "- A cada projétil desviado, você ganha 10 pontos",
            "- O jogo aumenta a dificuldade com o tempo",
            "- O jogo termina quando você é atingido por um projétil",
            "- Pressione 'Espaço' a qualquer momento para PAUSAR",
            "- Pressione 'Enter' para iniciar o jogo",
        ]

        tela.blit(texto_bem_vindo, (largura // 2 - texto_bem_vindo.get_width() // 2, 100))
        tela.blit(texto_jogo, (largura // 2 - texto_jogo.get_width() // 2, 170))

        for i, linha in enumerate(instrucoes):
            linha_render = texto_fonte.render(linha, True, branco)
            tela.blit(linha_render, (100, 250 + i * 40))

        pygame.display.update()
        fps.tick(60)

    