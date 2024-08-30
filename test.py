from TTS.api import TTS

models = TTS().list_models().models_dict
models_tts = models['tts_models']
models_vocoder = models['vocoder_models']
models_voice = models['voice_conversion_models']

print(models)