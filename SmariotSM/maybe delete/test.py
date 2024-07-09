import os
from pathlib import Path
from openai import OpenAI

from config import OPENAI_API_KEY

#load_dotenv()
#SECRET_KEY = os.getenv("SECRET_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def text_to_speech(text):
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=f"{text}"
  )

  response.stream_to_file(speech_file_path)
  os.system("open speech.mp3")


if __name__ == "__main__":
  text_to_speech("Naww mein kleines kitty ich liebe dich?")
