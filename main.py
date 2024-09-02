import random
import os
import json
import shutil

from datetime import date
from time import sleep
from transformers import pipeline
from gtts import gTTS
from moviepy.editor import *
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

from utils.utils import request
from utils.voice import Voice
from utils.animated_text import generate_animated_text

import moviepy.config as config
config.IMAGEMAGICK_BINARY = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'

load_dotenv(override=True)
voice = Voice()

# Data atual
data_atual = date.today()
dia = data_atual.day
mes = data_atual.month
ano = data_atual.year

path = f'created_videos/{ano}/{mes}/{dia}'
os.makedirs(path, exist_ok=True)
files = os.listdir(path)

path += f"/{len(files)}"
os.makedirs(path, exist_ok=True)

# Obtendo 1 artigo aleatório

artigo = None
abstract = ""
n = 0
while artigo is None or len(abstract) < 300:
    url = f"https://api.crossref.org/works?sample=50"
    artigos:list = request(url)['message']['items']

    while len(artigos):
        n+=1
        print(f"Obtendo artigo - {n}")

        artigo_escolhido = random.choice(artigos)
        artigos.remove(artigo_escolhido)

        doi = artigo_escolhido['DOI']

        # Obtendo os dados do artigo pelo DOI
        url = f"https://api.crossref.org/works/{doi}"
        artigo_data:dict = request(url)['message']

        if 'abstract' not in artigo_data.keys():
            continue
        
        artigo = artigo_data
        
        abstract = artigo.get('abstract').replace("<jats:p>", "").replace("</jats:p>", "").replace("<jats:title>", "").replace("</jats:title>", "")
        if len(abstract) >= 300:
            break

publisher = artigo.get('publisher')
DOI = artigo.get('DOI')
article_type = artigo.get('type')
titulos = artigo.get('title')
titulos_das_revistas = artigo.get('container-title')
language = artigo.get('language', 'en')
disponivel_em = artigo.get('URL')

authors = ""
for n, author in enumerate(artigo.get('author', [])):
    if 'family' not in author or 'given' not in author:
        continue
    
    if authors != "":
        authors += ", "
    authors += author["family"] + " " + author['given'][0] + "."

    if len(artigo.get('author', [])) >= 3:
        authors += " et. al."
        break
if authors == "":
    authors = "Unknown author"

# Obtendo o resumo do resumo
print(f"Criando um resumo do resumo do artigo {titulos}")
if len(abstract) >= 350:
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    resumo = summarizer(abstract, max_length=350, min_length=30, do_sample=False)[0]['summary_text']
else:
    resumo = abstract

# Obtendo o texto do script do vídeo
print("Gerando o texto final do script")
# generator = pipeline("text-generation", model="gpt2")
# script = generator(texto, max_length=500, num_return_sequences=1)
texto = f"""Is an article that talks about {resumo}"""


# Traduzindo todos os textos
print("Traduzindo todo o texto")
tradutor = GoogleTranslator(source= language, target= "pt")
traducao = tradutor.translate(texto)

#Descrição do vídeo
description = f"""
O artigo "{titulos[0]}" foi publicado em {publisher}, escrito por {authors}.
Este artigo pode ser encontrado em {disponivel_em}, seu DOI é {DOI}.
Siga para mais resumos de artigos!!

#universidade #resumo #artigos #paper #university #academic #pesquisa #resources
"""
print(f"A descrição do vídeo é:\n{description}")

# Gerando o audio falado na lingua desejada
print("Gerando o texto falado TTS")
texto_final = f"""Olá!
Você encontrou a página que faz resumo de artigos.
O artigo {titulos[0]}, publicado em {publisher}, por {authors}.
{traducao}.
Para mais resumos de artigos siga a página {os.getenv("PAGE_NAME")}
"""

audio, voice = voice.tts(texto_final)
voice_name = voice

# Caso seja um teste, salva na pasta de testes
if os.getenv("TEST").upper() == "TRUE":
    # Data atual
    dia = 1
    mes = 1
    ano = 1

    path = f'created_videos/{ano}/{mes}/{dia}'
    os.makedirs(path, exist_ok=True)
    files = os.listdir(path)

    path += f"/{len(files)}"
    os.makedirs(path, exist_ok=True)

# Recortando o áudio
shutil.move(audio, f"{path}/audio_gerado.mp3")
sleep(2)

# Dados do vídeo ############################

# Video de fundo
videos_files = os.listdir(r"videos/")
video_file = random.choice(videos_files)

# Metadados do vídeo
with open(f"{path}/metadados.json", mode="w+", encoding="UTF-8") as arq:
    json.dump({
        "publisher":publisher,
        "abstract":abstract,
        "DOI":DOI,
        "article_type":article_type,
        "titulos":titulos,
        "titulos_das_revistas":titulos_das_revistas,
        "language":language,
        "disponivel_em":disponivel_em,
        "authors":authors,
        "resumo_ia": resumo,
        "traducao": traducao,
        "texto_final":texto_final,
        "video_fundo":video_file,
        "description":description,
        "voice":voice_name,
    }, arq)

# Tempo do vídeo
audio_clip = AudioFileClip(f"{path}/audio_gerado.mp3")

#Video de fundo
video_clip = VideoFileClip(
    "videos/" + video_file,
    audio=False,
)
video_clip = video_clip.loop(duration = audio_clip.duration)


# Define o texto, a duração e a posição do texto

txt_clip = generate_animated_text(texto_final, video_clip.size, audio_clip.duration)

# Cria um vídeo a partir do texto e da imagem
video = CompositeVideoClip([
    video_clip,   
    txt_clip,
])

# # Adicionar áudio ao vídeo
video_clip = video.set_audio(audio_clip)

# # Salvar o vídeo
video_clip.write_videofile(f"{path}/video_gerado.mp4", fps=24, codec='libx264', preset='ultrafast')