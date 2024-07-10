import multiprocessing
import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime

from services.video_player import VideoPlayer
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

def update_clock(clock_label):
    now = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=now)
    clock_label.after(1000, update_clock, clock_label)

def run_start_listening():
    from services.assistant import start_listening
    start_listening()

def start_process():
    global listening_process
    listening_process = multiprocessing.Process(target=run_start_listening)
    listening_process.start()
    messagebox.showinfo("Started Listening", "Listening process started")

def stop_process():
    global listening_process
    if listening_process.is_alive():
        listening_process.terminate()
        listening_process.join()
        messagebox.showinfo("Stopped Listening", "Listening process stopped")

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("SMARIOT")
    root.geometry("1280x720")
    root.attributes("-fullscreen", True)
    root.configure(bg='black')

    logger.info("Created TKinter Application")

    # Main frame to hold all UI components
    main_frame = tk.Frame(root, bg="black")
    main_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=20, fill=tk.Y)

    # Frame for the greeting
    greeting_frame = tk.Frame(main_frame, bg="black")
    greeting_frame.pack(anchor=tk.NW, pady=(0, 20))

    # Label for greeting
    label = tk.Label(greeting_frame, text="Guten Tag", fg="white", bg="black", font=("Helvetica", 48))
    label.pack(padx=20, pady=20)

    # Frame for the clock on top right
    clock_frame = tk.Frame(root, bg="black")
    clock_frame.place(relx=1.0, y=10, anchor='ne')  # Place at top right

    # Label for clock
    clock_label = tk.Label(clock_frame, text="", fg="white", bg="black", font=("Helvetica", 24))
    clock_label.pack(padx=20, pady=20)
    update_clock(clock_label)

    # Frame for weather information
    weather_frame = tk.Frame(main_frame, bg="black")
    weather_frame.pack(anchor=tk.NW, pady=(0, 20))

    # Label for weather information
    weather_label = tk.Label(weather_frame, text="Aktuelles Wetter: Initializing...", fg="white", bg="black", font=("Helvetica", 24))
    weather_label.pack(padx=20, pady=20)

    # Frame for video player
    video_frame = tk.Frame(main_frame, bg="black")
    video_frame.pack(anchor=tk.NW, pady=(0, 20))

    # Initialize video player with the initial video path from WeatherHandler
    weather_handler = WeatherHandler()
    video_player = VideoPlayer(video_frame, weather_handler.current_video, max_width=600)

    # Update weather information display
    update_weather_display(weather_handler, weather_label, video_player)

    start_process()

    # Toggle fullscreen on Escape key press
    def toggle_fullscreen(event):
        is_fullscreen = root.attributes("-fullscreen")
        root.attributes("-fullscreen", not is_fullscreen)
        if not is_fullscreen:
            root.geometry("800x600")
        else:
            root.geometry("1280x720")

    root.bind("<Escape>", toggle_fullscreen)

    # Run the application
    root.mainloop()
    logger.info("Application closed")
