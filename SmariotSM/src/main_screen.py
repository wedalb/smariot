import multiprocessing
import threading
import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime
import cv2
import numpy as np

from video_player import VideoPlayer
from weather_api import WeatherHandler

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

def detect_waving(waving_detected):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)
    hand_positions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply background subtractor
        fg_mask = background_subtractor.apply(frame)
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue

            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            if h > w:  # Likely a hand
                hand_positions.append((x + w // 2, y + h // 2))
                if len(hand_positions) > 20:
                    hand_positions.pop(0)
                    if is_waving(hand_positions):
                        print("Waving detected!")
                        waving_detected.value = 1
                        hand_positions.clear()

        # Add a delay to prevent high CPU usage
        cv2.waitKey(30)

    cap.release()
    cv2.destroyAllWindows()

def is_waving(hand_positions):
    if len(hand_positions) < 20:
        return False

    movements = [hand_positions[i + 1][0] - hand_positions[i][0] for i in range(len(hand_positions) - 1)]
    positive_movements = [m for m in movements if m > 0]
    negative_movements = [m for m in movements if m < 0]

    return len(positive_movements) > 5 and len(negative_movements) > 5

def start_processes(waving_detected):
    global listening_process, waving_process
    listening_process = multiprocessing.Process(target=run_start_listening)
    waving_process = multiprocessing.Process(target=detect_waving, args=(waving_detected,))
    listening_process.start()
    waving_process.start()
    messagebox.showinfo("Processes Started", "Listening and waving detection processes started")

def stop_processes():
    global listening_process, waving_process
    if listening_process.is_alive():
        listening_process.terminate()
        listening_process.join()
    if waving_process.is_alive():
        waving_process.terminate()
        waving_process.join()
    messagebox.showinfo("Processes Stopped", "Listening and waving detection processes stopped")

def check_waving(label, waving_detected):
    if waving_detected.value == 1:
        label.config(text="Hi! :)")
        root.after(5000, reset_label, label, waving_detected)  # Reset label after 5 seconds
    root.after(100, check_waving, label, waving_detected)

def reset_label(label, waving_detected):
    label.config(text="Guten Tag")
    waving_detected.value = 0

if __name__ == "__main__":
    waving_detected = multiprocessing.Value('i', 0)

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

    start_processes(waving_detected)

    # Check for waving detection periodically
    root.after(100, check_waving, label, waving_detected)

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
    stop_processes()
