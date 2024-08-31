import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
import random

class Voice:

    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

    def clone_voice(self, name:str, audios:list[str], description:str|None = None):
        raise Exception("Esta versão não suporta clone de Voz")
        voice = self.client.clone(
            name=name,
            description=description,
            files=audios,
        )

        audio = self.client.generate(text="Olá! Eu sou a voz da Ananda clonada", voice=voice)

        return audio

    def get_voice(self, text, voz:str|None=None):
        voices = self.client.voices.get_all()
        voice = random.choice(voices.voices)

        if voz is not None:
            for voice_ in voices.voices:
                if voice_.name == voz:
                    voice = voice_
                    break
        

        audio = self.client.generate(text=text, voice=voice)
        return audio, voice

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)

    # voice = Voice()

    # audio = voice.get_voice("Teste de voz aleatória, vamos ver o que sai disso aqui.")

    # save(audio, "ananda.mp3")
    # play(audio)