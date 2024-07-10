# SMARIOT Smart Mirror Software

## Overview

SMARIOT is a smart mirror software designed to integrate with Home Assistant and various APIs to provide real-time weather updates, video playback, and other smart home functionalities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Weather Updates**: Get real-time weather information.
- **Video Playback**: Play videos based on the current weather conditions.
- **Home Assistant Integration**: Control and monitor your smart home devices.
- **Voice Assistant**: Interact with the system using voice commands.

## Setup

### Prerequisites

1. **Home Assistant Server**: Ensure you have a Home Assistant server set up and running. You can find the installation instructions [here](https://www.home-assistant.io/installation/).
2. **Python Environment**: Python 3.11+ should be installed on your system.
3. **Optional**: Ideally you have a smart mirror, but this can also be tested on a normal monitor and computer. 

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/wedalb/smariot.git
   cd SmariotSM
   ```
2. **Create a Virtual Environment:**

```
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```
3. ***Install Dependencies:***

```
pip install -r requirements.txt
```

### Configuration

Create a .env File: In the root directory, create a .env file and add the following API keys:

```
WEATHER_API_KEY=<your_weather_api_key>
OPENAI_API_KEY=<your_openai_api_key>
GROQ_API_KEY=<your_groq_api_key>
GENAI_API_KEY=<your_genai_api_key>
GOOGLE_PLACES_API_KEY=<your_google_places_api_key>
HOME_ASSISTANT_ACCESS_TOKEN=<your_home_assistant_access_token>
HOME_ASSISTANT_BASE_URL=<your_home_assistant_base_url>
```

### Running the Application

To start the smart mirror application, run the following command:

```
python ui/main_screen.py
```
## Project Structure
```
SmariotSM/
├── assets/
├── config/
├── services/
│   ├── assistant.py
│   ├── home_assistant.py
│   ├── video_player.py
│   ├── weather_api.py
│   └── webcam.jpg
├── ui/
│   └── main_screen.py
├── venv/
├── .env
├── config.py
├── README.md
├── requirements.txt
```
- assets/: Directory for static assets such as images and videos and the animations.
- config/: Configuration file for logging
- services/: Core services including the assistant, Home Assistant integration, video player, and weather API.
- ui/: User interface components, primarily the main screen.
- venv/: Virtual environment directory.
- .env: Environment variables file.
- config.py: Configuration script that contains constants
- README.md: Project documentation.
- requirements.txt: Python dependencies.
