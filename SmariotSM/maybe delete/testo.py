import tkinter as tk
import threading
import logging
import time
import speech_recognition as sr

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Function to handle speech-to-text in a background thread
def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        logger.info("Calibrating microphone for ambient noise...")

    while True:
        try:
            with microphone as source:
                logger.info("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                logger.info("Recognizing speech...")
                text = recognizer.recognize_google(audio)
                logger.info(f"Heard: {text}")
        except sr.UnknownValueError:
            logger.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
        time.sleep(1)


# Tkinter Application class
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def print_hello(self):
        print("Hello")

    def create_widgets(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.master.destroy)
        self.quit_button.pack(side="left")

        self.print_button = tk.Button(self, text='Print', command=self.print_hello)
        self.print_button.pack(side="left")


if __name__ == "__main__":
    logger.info("Starting the application")

    # Create and start the Tkinter application in the main thread
    root = tk.Tk()
    root.title('Sample Application')
    app = Application(master=root)

    # Start the speech-to-text service in a separate thread
    speech_thread = threading.Thread(target=speech_to_text, daemon=True)
    speech_thread.start()

    # Start the Tkinter mainloop (must be in the main thread)
    try:
        app.mainloop()
    except Exception as e:
        logger.error(f"Error in Tkinter mainloop: {e}")

    logger.info("Application has exited")
