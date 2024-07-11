import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import logging

# Logger for this module
logger = logging.getLogger(__name__)

VIDEO_MAX_WIDTH = 2400

class VideoPlayer:
    """
    A class to handle video playback in a Tkinter GUI.

    The VideoPlayer class is responsible for loading a video file, displaying its frames in a Tkinter Label widget, and
    providing methods to control the playback and update the video being played.

    Attributes:
    root (tk.Tk): The root Tkinter window or frame.
    video_path (str): The file path to the video to be played.
    video_stream (cv2.VideoCapture): The OpenCV video capture object.
    label (tk.Label): The Tkinter Label widget used to display video frames.

    Methods:
    __init__(root, video_path): Initializes the VideoPlayer with a Tkinter root window and a video file path.
    play_video(): Reads frames from the video file and updates the Tkinter Label widget.
    update_video(new_video_path): Updates the VideoPlayer to play a new video file.
    """
    def __init__(self, root, video_path, max_width=VIDEO_MAX_WIDTH):
        """
        Initializes the VideoPlayer with a Tkinter root window and a video file path.

        Parameters:
        root (tk.Tk): The root Tkinter window or frame.
        video_path (str): The file path to the video to be played.
        max_width (int): The maximum width of the video frame.

        Raises:
        ValueError: If the video file cannot be opened.
        """
        self.root = root
        self.video_path = video_path
        self.max_width = max_width

        logger.debug("Attempting to open video file: %s", self.video_path)
        # Attempt to open video file
        self.video_stream = cv2.VideoCapture(self.video_path)
        if not self.video_stream.isOpened():
            logger.error("Unable to open video file: %s", self.video_path)
            raise ValueError(f"Unable to open video file: {self.video_path}")

        logger.debug("Creating and packing label for video frames")
        # Create and pack label to display video frames
        self.label = Label(root, bg="black")
        self.label.pack(anchor=tk.NW, pady=20)

        logger.info("Starting video playback")
        # Start video playback
        self.play_video()

    def play_video(self):
        """
        Reads frames from the video file and updates the Tkinter Label widget.

        This method continuously reads frames from the video file, converts them to a format compatible with Tkinter,
        and updates the Label widget to display the frames. It also handles restarting the video when it reaches the end.

        Parameters:
        None

        Returns:
        None
        """
        ret, frame = self.video_stream.read()
        if ret:
            # Resize frame to fit max width
            height, width, _ = frame.shape
            if width > self.max_width:
                scale_ratio = self.max_width / width
                new_width = int(width * scale_ratio)
                new_height = int(height * scale_ratio)
                frame = cv2.resize(frame, (new_width, new_height))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.label.config(image=frame)
            self.label.image = frame
        else:
            logger.debug("Restarting video from the beginning")
            # Restart video if it reaches the end
            self.video_stream.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Schedule the next frame update
        self.root.after(10, self.play_video)

    def update_video(self, new_video_path):
        """
        Updates the VideoPlayer to play a new video file.

        This method releases the current video stream, opens a new video stream for the specified video file,
        and logs the change.

        Parameters:
        new_video_path (str): The file path to the new video to be played.

        Raises:
        ValueError: If the new video file cannot be opened.
        """
        logger.info("Updating video to new file: %s", new_video_path)
        self.video_path = new_video_path
        self.video_stream.release()  # Release the current video stream
        self.video_stream = cv2.VideoCapture(self.video_path)  # Open the new video stream
        if not self.video_stream.isOpened():
            logger.error("Unable to open video file: %s", self.video_path)
            raise ValueError(f"Unable to open video file: {self.video_path}")
        logger.info("Switched to new video: %s", self.video_path)
