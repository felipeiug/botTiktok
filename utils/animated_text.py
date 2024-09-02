import re
from moviepy.editor import *
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

def generate_animated_text(text:str, movie_size:tuple[float], max_duration:float):
    txt_clips = []

    padding = 0.005*movie_size[0]

    text = text.replace("\n", " ")
    font_size = movie_size[1]/25

    n_letras = len(text)
    time_letra = max_duration/n_letras

    # frases = sent_tokenize(text, language="portuguese")
    frases = re.split(r'(?<=[.!?,;]) +', text)

    time_start = 0
    for frase in frases:

        new_frase = ""
        for palavra in frase.split(" "):
            n_letras_palavra = len(palavra)

            if ((len(new_frase.split("\n")[-1]) + n_letras_palavra) * font_size) > (movie_size[0]-2*padding):
                new_frase += "\n"
            else:
                new_frase += " "
            
            new_frase += palavra

        n_letras_now = len(new_frase)
        time_texto = time_letra*n_letras_now

        txt_clip = TextClip(
            new_frase,
            fontsize=font_size,
            color='white',
            bg_color='transparent',
            size=movie_size
        )
        txt_clip = txt_clip.set_start(time_start).set_duration(time_texto).set_position('center')
        txt_clips.append(txt_clip)

        time_start += time_texto

    txt_clip = concatenate_videoclips(txt_clips)
    return txt_clip