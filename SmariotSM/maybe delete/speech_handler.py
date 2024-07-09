import speech_recognition as sr

from config import ASSISTANT_PROMPT, TTS_LANGUAGE, OPENAI_API_KEY
from gtts import gTTS
import os
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)


class SpeechHandler:

    def __init__(self, language=TTS_LANGUAGE):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        self.voice_input = self.speech_to_text_from_mic()
        self.text_output =  ""
        self.messages = [{"role": "system", "content": ASSISTANT_PROMPT}]

    def text_to_speech(self, text):
        tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
        tts.save('output.mp3')
        os.system("open output.mp3")  # For Mac, use 'open'. For Windows, use 'start'. For Linux, use 'xdg-open'.


    def speech_to_text_from_mic(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        try:
            with microphone as source:
                print("Bitte sprich etwas ...")
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.listen(source, timeout=5)
                print("Verarbeite die Aufnahme...")
                text = recognizer.recognize_google(audio_data, language='de-DE')
                self.voice_input = text

                print("Erkannter Text: ", text)
                return text

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            return "Ich konnte dich nicht verstehen"
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))
            return ""
        except sr.WaitTimeoutError:
            print("Speech Recognition timed out")
            return ""
        except KeyboardInterrupt:
            print("Beenden durch Benutzereingabe")
            return ""
        except Exception as e:
            print(f"Unknown Error: {e}")
            return ""



