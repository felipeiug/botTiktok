import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
import random

class Voice:
    mask_voices_ids = [
        None,
        "IKne3meq5aSn9XLyUdCD"
    ]
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

    def get_voice(self, text, voice_id:str|None="pNInz6obpgDQGcFmaJgB"): # Defined with Adam Voice.
        """voice_id = None, random voice"""
        
        voices = self.client.voices.get_all()

        if voice_id is None:
            voice_id = None
            while voice_id in self.mask_voices_ids:
                voice = random.choice(voices.voices)
                voice_id = voice.voice_id
        else:
            for voice_ in voices.voices:
                if voice_.voice_id == voice_id:
                    voice = voice_
                    break
            else:
                voice = random.choice(voices.voices)
        
        audio = self.client.generate(text=text, voice=voice)
        return audio, voice

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)

    # voice = Voice()

    # audio = voice.get_voice("Teste de voz aleatória, vamos ver o que sai disso aqui.")

    # save(audio, "ananda.mp3")
    # play(audio)