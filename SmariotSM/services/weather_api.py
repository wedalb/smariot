import requests
from config import MUNICH_LAT, MUNICH_LON, WEATHER_API_KEY, GOOGLE_PLACES_API_KEY
import logging

logger = logging.getLogger(__name__)

# Constants
BASE_URL_TEMPLATE = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={key}&lang=de&units=metric"
BASE_VIDEO = "../assets/animations/cloudy/default.mp4"
WINTER_VIDEO = "../assets/animations/snowy/default.mp4"
RAINY_VIDEO = "../assets/animations/rainy/default.mp4"
HEATY_VIDEO = "../assets/animations/heaty/default.mp4"
TEMP_THRESHOLD_COLD = 7
TEMP_THRESHOLD_HOT = 20

def get_weather_group(weather_id):
    """
    Maps weather condition codes to descriptive weather groups of the openweathermap-api.

    This function takes a weather condition code (weather_id) and returns a string that describes the general weather group
    associated with that code. The mapping is based on the OpenWeatherMap weather condition codes.

    Parameters:
    weather_id (int): The weather condition code to be mapped.

    Returns:
    str: A string representing the weather group. Possible return values are:
         - "Thunderstorm" for codes 200-232
         - "Drizzle" for codes 300-321
         - "Rain" for codes 500-531
         - "Snow" for codes 600-622
         - "Atmosphere" for codes 701-781
         - "Clear" for code 800
         - "Clouds" for codes 801-804
         - "Unknown" for any other codes

    Example:
    weather_group = get_weather_group(802)
    print(weather_group)  # Output: "Clouds"

    Notes:
    - The weather condition codes are based on the OpenWeatherMap API.
    - This function provides a simplified grouping of weather conditions for easier interpretation.
    """
    if 200 <= weather_id <= 232:
        return "Thunderstorm"
    elif 300 <= weather_id <= 321:
        return "Drizzle"
    elif 500 <= weather_id <= 531:
        return "Rain"
    elif 600 <= weather_id <= 622:
        return "Snow"
    elif 701 <= weather_id <= 781:
        return "Atmosphere"
    elif weather_id == 800:
        return "Clear"
    elif 801 <= weather_id <= 804:
        return "Clouds"
    else:
        return "Unknown"
def get_current_gps_coordinates():
    """
    Fetches and returns the current GPS coordinates using the Google Geolocation API.

    Parameters:
    None

    Returns:
    tuple: A tuple containing the latitude and longitude as floats if the request is successful.
           Returns the default Munich Latitude and Longitude if the request fails.

    Example:
    coordinates = get_current_gps_coordinates()
    if coordinates:
        logger.info(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
    else:
        logger.error("Failed to fetch GPS coordinates")

    Notes:
    - The `requests` module must be imported for making HTTP requests.
    - The `GOOGLE_PLACES_API_KEY` must be defined and contain a valid API key for the Google Geolocation API.
    - This function sends a POST request to the Google Geolocation API with the 'considerIp' parameter set to 'true'.
    - If the request is successful, the function logs and returns the accurate GPS coordinates (latitude and longitude).
    - If the request fails, the function logs an error message with the status code and response text, and returns the default Munich Latitude and Longitude.
    """
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + GOOGLE_PLACES_API_KEY
    data = {'considerIp': 'true'}

    try:
        logger.debug("Sending request to Google Geolocation API")
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        location = response.json()['location']
        logger.info(f"Accurate coordinates: {location['lat']}, {location['lng']}")
        return location['lat'], location['lng']
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred while fetching geolocation: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception occurred while fetching geolocation: {e}")
    except KeyError as e:
        logger.error(f"Key error occurred while processing geolocation data: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    logger.info(f"Returning default coordinates: Latitude {MUNICH_LAT}, Longitude {MUNICH_LON}")
    return MUNICH_LAT, MUNICH_LON
class WeatherHandler:
    """
    A class to handle weather-related operations, including fetching current weather data and determining
    appropriate video animations based on the weather conditions.

    The class initializes by fetching the current GPS coordinates and weather data, and determining the video
    to be displayed based on the weather conditions.

    Attributes:
    api_key (str): API key for accessing the weather service.
    base_url (str): Base URL for the weather API, formatted with current latitude, longitude, and API key.
    condition (str): Current weather condition description.
    temp (float): Current temperature in Celsius.
    group (str): Weather group determined by the weather condition ID.
    icon_url (str): URL of the weather icon.
    current_video (str): Path to the video animation corresponding to the current weather condition.

    Methods:
    __init__(): Initializes the WeatherHandler with current weather data and video.
    get_weather(): Fetches the current weather condition and temperature.
    get_weather_extended(): Fetches detailed weather information, including weather group and icon URL.
    get_current_video(): Determines the appropriate video animation based on the current weather conditions.
    """
    def __init__(self):
        """
        Initializes the WeatherHandler class by fetching current GPS coordinates and weather data,
        and determining the appropriate video animation.
        """
        logger.debug("Initializing WeatherHandler")
        self.api_key = WEATHER_API_KEY
        try:
            logger.debug("Fetching current GPS coordinates")
            latitude, longitude = get_current_gps_coordinates()
            logger.info(f"Fetched GPS coordinates: Latitude {latitude}, Longitude {longitude}")
        except Exception as e:
            logger.error(f"Error fetching GPS coordinates: {e}")
            latitude, longitude = MUNICH_LAT, MUNICH_LON

        self.base_url = BASE_URL_TEMPLATE.format(lat=latitude, lon=longitude, key=self.api_key)
        logger.debug("Formatted base URL for weather data: %s", self.base_url)

        try:
            self.condition, self.temp, self.group, self.icon_url = self.get_weather_extended()
            logger.info(
                f"Fetched weather data: Condition {self.condition}, Temperature {self.temp}°C, Group {self.group}, Icon URL {self.icon_url}")
        except Exception as e:
            logger.error(f"Error fetching extended weather data: {e}")
            self.condition, self.temp, self.group, self.icon_url = None, None, None, None

        self.current_video = self.get_current_video()
        logger.info(f"Determined current video: {self.current_video}")
    def get_weather(self):
        """
        Fetches and returns the current weather condition and temperature.

        Returns:
        tuple: A tuple containing:
            - current_weather (str): Description of the current weather condition in German.
            - temperature (float): Current temperature in Celsius.

        Logs any errors encountered during the request.

        Example:
        current_weather, temperature = weather_handler.get_weather()
        logger.info(f"Weather: {current_weather}, Temperature: {temperature}°C")
        """
        try:
            logger.debug("Fetching weather data from URL: %s", self.base_url)
            response = requests.get(self.base_url)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            data = response.json()
            weather_data = data['current']['weather'][0]
            weather_id = weather_data['id']
            current_weather = weather_data['description'].capitalize()  # Get description in German
            temperature = data['current']['temp']

            logger.info(f"Fetched weather data: {current_weather}, {temperature}°C")
            return current_weather, temperature
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred while fetching weather data: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception occurred while fetching weather data: {e}")
        except KeyError as e:
            logger.error(f"Key error occurred while processing weather data: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        return None, None
    def get_weather_extended(self):
        """
        Fetches and returns detailed weather information, including weather group and icon URL.

        Returns:
        tuple: A tuple containing:
            - current_weather (str): Description of the current weather condition in German.
            - temperature (float): Current temperature in Celsius.
            - weather_group (str): Weather group determined by the weather condition ID.
            - icon_url (str): URL of the weather icon.

        Logs any errors encountered during the request.

        Example:
        current_weather, temperature, weather_group, icon_url = weather_handler.get_weather_extended()
        logger.info(f"Weather: {current_weather}, Temperature: {temperature}°C, Group: {weather_group}, Icon URL: {icon_url}")
        """
        try:
            logger.debug("Fetching weather data from URL: %s", self.base_url)
            response = requests.get(self.base_url)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            data = response.json()
            weather_data = data['current']['weather'][0]
            weather_id = weather_data['id']
            current_weather = weather_data['description'].capitalize()  # Get description in German
            temperature = data['current']['temp']
            weather_group = get_weather_group(weather_id)
            weather_icon = weather_data['icon']
            icon_url = f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"

            logger.info(
                f"Fetched weather data: {current_weather}, {temperature}°C, {weather_group}, Icon URL: {icon_url}")
            return current_weather, temperature, weather_group, icon_url
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred while fetching weather data: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception occurred while fetching weather data: {e}")
        except KeyError as e:
            logger.error(f"Key error occurred while processing weather data: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        return None, None, None, None
    def get_current_video(self):
        """
        Determines and returns the appropriate video animation based on the current weather conditions.

        Returns:
        str: Path to the video animation corresponding to the current weather condition.

        Example:
        current_video = weather_handler.get_current_video()
        logger.info(f"Current video: {current_video}")
        """
        if not (self.condition and self.temp and self.group and self.icon_url):
            logger.error("Failed to fetch weather data. Using base video.")
            return BASE_VIDEO

        logger.debug(f"Current conditions: {self.condition}, Temp: {self.temp}°C, Group: {self.group}")

        if self.temp < TEMP_THRESHOLD_COLD or self.group == "Snow":
            logger.info("Selected winter video based on current weather conditions")
            return WINTER_VIDEO
        elif self.group in ["Drizzle", "Thunderstorm", "Rain"]:
            logger.info("Selected rainy video based on current weather conditions")
            return RAINY_VIDEO
        elif self.temp > TEMP_THRESHOLD_HOT or self.group in ["Atmosphere", "Clear"]:
            logger.info("Selected heaty video based on current weather conditions")
            return HEATY_VIDEO

        logger.info("Selected base video based on current weather conditions")
        return BASE_VIDEO

# Example usage
if __name__ == "__main__":
    weather_handler = WeatherHandler()
    if weather_handler.condition and weather_handler.temp and weather_handler.group and weather_handler.icon_url:
        print(
            f"Wetter: {weather_handler.condition}, Temperatur: {weather_handler.temp}°C, Gruppe: {weather_handler.group}, Icon URL: {weather_handler.icon_url}")
        print(weather_handler.current_video)
    else:
        print("Failed to fetch weather data")
