"""

This script sets up a logging configuration using Python's built-in `logging` module.
It defines the logging level, format, date format, and specifies handlers to direct log messages to
both a file and the console.

"""
import logging

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("../app.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

