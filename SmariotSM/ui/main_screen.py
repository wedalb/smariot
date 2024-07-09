import threading
import tkinter as tk

from services.assistant import start_listening
from services.video_player import VideoPlayer
import logging

from services.weather_api import WeatherHandler

# Logger for this module
logger = logging.getLogger(__name__)

def update_weather_display(weather_handler, weather_label, video_player):
    if weather_handler.condition and weather_handler.temp and weather_handler.group and weather_handler.icon_url:
        weather_info = f"Aktuelles Wetter: {weather_handler.condition}, {weather_handler.temp}°C"
    else:
        weather_info = "Failed to fetch weather data"

    weather_label.config(text=weather_info)
    video_player.update_video(weather_handler.current_video)

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("SMARIOT")
    root.geometry("1280x720")
    root.attributes("-fullscreen", True)
    root.configure(bg='black')

    logger.info("Created TKinter Application")

    # Label for greeting
    label = tk.Label(root, text="Guten Tag", fg="white", bg="black", font=("Helvetica", 48))
    label.pack(expand=True)

    # Label for weather information
    weather_label = tk.Label(root, text="Aktuelles Wetter: Initializing...", fg="white", bg="black",
                             font=("Helvetica", 24))
    weather_label.pack()

    # Initialize WeatherHandler
    weather_handler = WeatherHandler()

    # Initialize video player with the initial video path from WeatherHandler
    video_player = VideoPlayer(root, weather_handler.current_video)

    # Update weather information display
    update_weather_display(weather_handler, weather_label, video_player)

    # Toggle fullscreen on Escape key press
    def toggle_fullscreen(event):
        is_fullscreen = root.attributes("-fullscreen")
        root.attributes("-fullscreen", not is_fullscreen)
        if not is_fullscreen:
            root.geometry("800x600")
        else:
            root.geometry("1280x720")

    root.bind("<Escape>", toggle_fullscreen)

    # Start the speech recognition and response thread
    threading.Thread(target=start_listening, daemon=True).start()

    # Run the application
    root.mainloop()
    logger.info("Application closed")
