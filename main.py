import random

from time import sleep
from transformers import pipeline
from gtts import gTTS
from moviepy.editor import *
from deep_translator import GoogleTranslator

from utils import request

import moviepy.config as config
config.IMAGEMAGICK_BINARY = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'

# Obtendo o artigo para um tema
# tema = "atronomia+universo"

# artigo = None
# n = 0
# while artigo is None:
#     sleep(2)
#     url = f"https://api.crossref.org/works?sample=50"
#     artigos:list = request(url)['message']['items']

#     while len(artigos):
#         n+=1
#         print(f"Obtendo artigo - {n}")

#         artigo_escolhido = random.choice(artigos)
#         artigos.remove(artigo_escolhido)

#         doi = artigo_escolhido['DOI']

#         # Obtendo os dados do artigo pelo DOI
#         url = f"https://api.crossref.org/works/{doi}"
#         artigo_data:dict = request(url)['message']

#         if 'abstract' not in artigo_data.keys():
#             continue
        
#         artigo = artigo_data
#         break

# publisher = artigo.get('publisher')
# abstract = artigo.get('abstract').replace("<jats:p>", "").replace("</jats:p>", "")
# DOI = artigo.get('DOI')
# article_type = artigo.get('type')
# titulos = artigo.get('title')
# titulos_das_revistas = artigo.get('container-title')
# language = artigo.get('language', 'en')
# disponivel_em = artigo.get('URL')

# authors = ""
# for n, author in enumerate(artigo.get('author', [])):
#     if 'family' not in author or 'given' not in author:
#         continue
    
#     if authors != "":
#         authors += ", "
#     authors += author["family"] + " " + author['given'][0] + "."

#     if len(artigo.get('author', [])) >= 3:
#         authors += " et. al."
#         break
# if authors == "":
#     authors = "Unknown author"

# # Obtendo o resumo do resumo
# print("Criando um resumo do resumo do artigo")
# summarizer = pipeline("summarization", model="Falconsai/text_summarization")
# resumo = summarizer(abstract, max_length=200, min_length=30, do_sample=False)[0]['summary_text']

# # Obtendo o texto do script do vídeo
# print("Gerando o texto final do script")
# # generator = pipeline("text-generation", model="gpt2")
# # script = generator(texto, max_length=500, num_return_sequences=1)
# texto = f"""The article {titulos[0]}, published in {publisher} by {authors}. Is an article that talks about {resumo}"""


# # Traduzindo todos os textos
# print("Traduzindo todo o texto")
# tradutor = GoogleTranslator(source= language, target= "pt")
# traducao = tradutor.translate(texto)

# # Gerando o audio falado na lingua desejada
# print("Gerando o texto falado TTS")
# texto_final = f"Olá! Está é a página que faz resumo de artigos. {traducao}."
# tts = gTTS(text=texto_final, lang='pt')
# tts.save("audio_gerado.mp3")
# sleep(2)

# Dados do vídeo ############################

# Tempo do vídeo
audio_clip = AudioFileClip("audio_gerado.mp3")

# Imagem de fundo
image_clip = ImageClip(
    "F:/Fotos/10675-214.png",
    duration=2,
    # duration=audio_clip.duration
).resize(height=1920)

# Define o texto, a duração e a posição do texto
text = "Teste de texto"
txt_clip = TextClip(text, fontsize=70, color='white', bg_color='transparent', size=image_clip.size)
txt_clip = txt_clip.set_duration(
    2
    # audio_clip.duration
).set_position('center')

# Cria um vídeo a partir do texto e da imagem
video = CompositeVideoClip([image_clip, txt_clip])

# # Adicionar áudio ao vídeo
video_clip = video.set_audio(audio_clip)

# # Salvar o vídeo
video_clip.write_videofile("video_gerado.mp4", fps=24, codec='libx264', preset='ultrafast')