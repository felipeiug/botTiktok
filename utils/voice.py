import os
import random
import glob

from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

class Voice:
    # Login
    xpath_user = "/html/body/div/div[2]/div/div[2]/div/div/div[2]/form/div[1]/input"
    xpath_pass = "/html/body/div/div[2]/div/div[2]/div/div/div[2]/form/div[2]/input"
    xpath_btn_entrar = "/html/body/div/div[2]/div/div[2]/div/div/div[2]/form/div[3]/button"

    # Texto e generate
    xpath_text_unput = "/html/body/div[1]/div[2]/div[4]/div[3]/div/div/div/div[1]/div/textarea"
    xpath_btn_generate_test = "/html/body/div[1]/div[2]/div[4]/div[3]/div/div/div/div[1]/div/div/div[1]/button/div/div[1]/div[2]/button"
    xpath_btn_generate = "/html/body/div[1]/div[2]/div[4]/div[3]/div/div/div/div[1]/div/div/button[2]"

    # Vozes
    xpath_btn_voices = "/html/body/div[1]/div[2]/div[4]/div[3]/div/div/div/div[1]/div/div/div[1]/button"
    class_voice = "text-sm truncate"

    # Download audio
    xpath_btn_download = "/html/body/div[1]/div[2]/div[4]/span/div/div[2]/div/div[2]/div[2]/div[3]/button[1]"

    def __init__(self):
        self.driver = webdriver.Chrome()
        sleep(0.5)
        self.driver.get('https://elevenlabs.io/app/speech-synthesis/text-to-speech')
        sleep(5)
        self.login_eleven_labs()

    def login_eleven_labs(self):
        print("Login Eleven Labs")

        user = os.getenv("ELEVEN_LABS_USER")
        password = os.getenv("ELEVEN_LABS_PASS")

        while True:
            try:
                user_element = self.driver.find_element(By.XPATH, self.xpath_user)
                break
            except Exception as e:
                pass

        user_element.send_keys(user)

        password_element = self.driver.find_element(By.XPATH, self.xpath_pass)
        password_element.send_keys(password)

        btn_element = self.driver.find_element(By.XPATH, self.xpath_btn_entrar)
        btn_element.click()

        print("Otendo text input")
        while True:
            try:
                self.text_input = self.driver.find_element(By.XPATH, self.xpath_text_unput)
                self.text_input.click()
                break
            except Exception as e:
                pass

        print("Otendo botão de gerar")
        if os.getenv("TEST").upper() == "TRUE":
            self.xpath_btn_generate = self.xpath_btn_generate_test
        while True:
            try:
                self.btn_generate = self.driver.find_element(By.XPATH, self.xpath_btn_generate)
                break
            except Exception as e:
                pass
    
    def get_voices(self):
        sleep(3)

        voices_return = {}

        voices_mask = [
            "Adam Stone - late night radio",
            "Shelley - Clear and confident British female",
            "Archie - English teen youth"
        ]
        while len(voices_return) == 0:
            for class_voice_ in self.class_voice.split(" "):
                voice_elems = self.driver.find_elements(By.CLASS_NAME, class_voice_)

                for voice in voice_elems:
                    try:
                        if voice.get_attribute("class") != self.class_voice:
                            continue
                    except Exception as e:
                        continue

                    if voice.text in voices_mask:
                        continue

                    voices_return[voice.text] = voice
        
        return voices_return

    def select_voice(self, voice_name:str|None = None):
        while True:
            try:
                print("Escolhendo as vozes")

                # Abrindo as vozes
                btn = self.driver.find_element(By.XPATH, self.xpath_btn_voices)
                sleep(1)
                btn.click()
                sleep(1)

                voices = self.get_voices()
                sleep(1)

                if voice_name not in voices:
                    voice_name = random.choice(list(voices.keys()))
                
                voices[voice_name].click()
                sleep(1)
                break

            except Exception as e:
                print(e)

        return voice_name

    def select_most_recently_mp3(self):
        downloads_path = str(Path.home() / "Downloads")
        mp3_files = glob.glob(os.path.join(downloads_path, '*.mp3'))
        
        if not mp3_files:
            raise FileNotFoundError("Nenhum arquivo .mp3 encontrado.")

        mp3_files.sort(key=os.path.getmtime, reverse=True)
        return mp3_files[0]

    def tts(self, text, voice_name:str|None=None): # Defined with Adam Voice.
        """voice_name = None, random voice"""

        voice = self.select_voice(voice_name)
        
        self.text_input.send_keys(text)
        sleep(0.5)
        
        self.btn_generate.click()
        sleep(1)

        while True:
            sleep(10)
            try:
                print("Aguardando audio gerado")
                btn = self.driver.find_element(By.XPATH, self.xpath_btn_download)

                if btn.get_attribute('aria-label') != "Download Audio":
                    continue

                sleep(1)
                btn.click()
                sleep(10)
                break
            except Exception as e:
                pass
        
        mp3_file = self.select_most_recently_mp3()
        sleep(15)
        return mp3_file, voice

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)

    voice = Voice()

    print("Eleven Labs Login")

    audio, voz = voice.tts("Teste de texto em português.")
    print(audio)