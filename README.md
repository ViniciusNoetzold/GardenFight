##Testador do jogo: Luís Eduardo Köche RA:1138427


# 🎮 Ataque à Horta

**Ataque à Horta** é um jogo interativo de desvio de projéteis desenvolvido em Python com a biblioteca Pygame. Controle um personagem que deve sobreviver a um ataque inimigo, acumulando a maior pontuação possível. O jogo se destaca por funcionalidades como reconhecimento de voz para entrada de nome e síntese de fala, tornando a experiência mais imersiva e acessível.

---

## ✨ Principais Funcionalidades

- **Jogabilidade Dinâmica:** Mova-se para a esquerda e direita para desviar dos projéteis.
- **Sistema de Pontuação:** Desafie-se a bater seu próprio recorde.
- **Interface Gráfica Viva:** Animações como o sol girando e nuvens se movendo criam um cenário agradável.
- **Efeitos Sonoros e Música:** Áudio imersivo para uma melhor experiência de jogo.
- **Reconhecimento de Voz:** Diga seu nome para começar a jogar, sem precisar digitar.
- **Síntese de Fala (TTS):** O jogo interage com você através de voz.
- **Histórico de Pontuações:** Suas últimas pontuações são salvas com data e hora e exibidas na tela de "Game Over".

---

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)**: Linguagem de programação principal.
- **[Pygame](https://www.pygame.org/)**: Biblioteca para desenvolvimento de jogos.
- **[pyttsx3](https://pypi.org/project/pyttsx3/)**: Conversão de texto em voz (Text-to-Speech).
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)**: Reconhecimento de fala.
- **[PyAudio](https://pypi.org/project/PyAudio/)**: Backend para captura de áudio do microfone.
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)**: Para a janela de entrada de texto como alternativa à voz.

---

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar e rodar o projeto em sua máquina.

**1. Clone o repositório:**
```bash
git clone https://github.com/ViniciusNoetzold/GardenFight.git
cd ataque-a-horta
```

**2. Crie e ative um ambiente virtual (recomendado):**
```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no Linux/macOS
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```
> **ℹ️ Nota para usuários Linux:**
> Caso encontre problemas com as bibliotecas `tkinter` ou `pyaudio`, pode ser necessário instalar pacotes adicionais no seu sistema. Para distribuições baseadas em Debian (como Ubuntu), use o comando:
> ```bash
> sudo apt-get update
> sudo apt-get install python3-tk portaudio19-dev python3-pyaudio
> ```

**4. Execute o jogo:**
```bash
python main.py
```
---

## 📁 Estrutura do Projeto
```
.
├── main.py              # Arquivo principal que inicia o jogo
├── comandos.py          # Módulo com funções auxiliares (voz, pontuação, etc.)
├── requirements.txt     # Lista de dependências do projeto
├── log.dat              # Arquivo de log para salvar as pontuações
├── README.md            # Este arquivo
└── recursos/            # Pasta com todos os assets (imagens, ícones e sons)
    ├── gameIcon.png
    ├── gameMusic.mp3
    ├── startScreen.png
    ├── background.png
    ├── dieScreen.png
    ├── mainChracter.png
    ├── enemy.png
    └── enemyProjetil.png
```

---

## 📜 Licença

Sinta-se à vontade para usar, modificar e distribuir para fins educacionais e pessoais.

---

## 💡 Créditos

Desenvolvido por **Vinícius de Almeida Noetzold** (RA: 1138554).

*Projeto criado como trabalho avaliativo para a disciplina de Algoritmos e Programação do curso de Ciência da Computação na Atitus Educação - Campus Santa Teresinha.*
