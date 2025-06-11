import sys
from cx_Freeze import setup, Executable

# --- CONFIGURAÇÕES BÁSICAS ---

# Base para ocultar o console preto no Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Lista de arquivos e pastas para incluir obrigatoriamente
# Incluímos a pasta de recursos e seu outro arquivo .py
arquivos_para_incluir = ["recursos/", "comandos.py"]

# Lista de pacotes essenciais que o cx_Freeze pode não encontrar sozinho
# Adicionamos "aifc" que causou o erro anterior
pacotes_extras = ["pygame", "tkinter", "pyttsx3", "speech_recognition", "aifc"]

# --- DEFINIÇÃO DO EXECUTÁVEL ---

executavel = [
    Executable(
        script="main.py",             # Seu arquivo principal
        base=base,                    # Usa a base que definimos acima
        icon="recursos/gameIcon.ico"  # IMPORTANTE: Use um ícone .ico
    )
]

# --- CHAMADA DO SETUP ---

setup(
    name="Ataque a Horta",
    version="1.0",
    description="Jogo de desviar de projéteis",
    options={
        "build_exe": {
            "packages": pacotes_extras,
            "include_files": arquivos_para_incluir
        }
    },
    executables=executavel
)