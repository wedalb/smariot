import json
import requests
from websocket import WebSocketApp
from config_constants import HOME_ASSISTANT_ACCESS_TOKEN, HOME_ASSISTANT_BASE_URL

class HomeAssistantWebSocket:
    def __init__(self, base_url, token):
        """
        Initializes the WebSocket connection instance with the provided base URL and access token.

        Parameters:
        base_url (str): The base URL of the Home Assistant API.
        token (str): The access token for authenticating with the Home Assistant API.
        """
        self.base_url = base_url
        self.token = token
        self.ws = None

    def connect(self):
        """
        Establishes the WebSocket connection to the Home Assistant API and sets up event handlers.

        Parameters:
        None

        Usage:
        ha_ws = HomeAssistantWebSocket(home_assistant_url, token)
        ha_ws.connect()
        """
        ws_url = self.base_url.replace("http", "ws") + "/api/websocket"
        print(f"Connecting to WebSocket URL: {ws_url}")
        self.ws = WebSocketApp(
            ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()

    def on_open(self, ws):
        """
        Handles the WebSocket connection opening event. Sends an authentication message to the Home Assistant API.

        Parameters:
        ws: The WebSocket connection instance.

        Usage:
        This function is called internally by the WebSocketApp when the connection is opened.
        """
        print("Connected to Home Assistant WebSocket API")
        auth_message = {
            "type": "auth",
            "access_token": self.token
        }
        ws.send(json.dumps(auth_message))

    def on_message(self, ws, message):
        """
        Handles incoming WebSocket messages. Processes authentication responses and state change events.

        Parameters:
        ws: The WebSocket connection instance.
        message (str): The received message as a JSON string.

        Usage:
        This function is called internally by the WebSocketApp when a message is received.
        """
        message = json.loads(message)
        if message.get("type") == "auth_ok":
            print("Authentication successful")
            subscribe_message = {
                "id": 1,
                "type": "subscribe_events",
                "event_type": "state_changed"
            }
            ws.send(json.dumps(subscribe_message))
            # Fetch the initial state of the sensor
            self.fetch_initial_state()
        elif message.get("type") == "event":
            entity_id = message["event"]["data"]["entity_id"]
            if entity_id == "binary_sensor.vibration1_vibration":
                new_state = message["event"]["data"]["new_state"]["state"]
                print(f"State of {entity_id} changed to: {new_state}")

    def on_error(self, ws, error):
        """
        Handles errors that occur during the WebSocket connection.

        Parameters:
        ws: The WebSocket connection instance.
        error (str): The error message.

        Usage:
        This function is called internally by the WebSocketApp when an error occurs.
        """
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """
        Handles the WebSocket connection closing event.

        Parameters:
        ws: The WebSocket connection instance.
        close_status_code (int): The status code for the WebSocket closure.
        close_msg (str): The close message.

        Usage:
        This function is called internally by the WebSocketApp when the connection is closed.
        """
        print("Disconnected from Home Assistant WebSocket API")

    def fetch_initial_state(self):
        """
        Fetches the initial state of a specified sensor from the Home Assistant REST API.

        Parameters:
        None

        Usage:
        This function is called internally by the `on_message` method to get the initial state of the sensor.

        ha_ws.fetch_initial_state()
        """
        url = f"{self.base_url}/api/states/binary_sensor.lumi_lumi_vibration_aq1_vibration"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }
        print(f"Fetching initial state from URL: {url}")
        response = requests.get(url, headers=headers)
        print(f"Response: {response.status_code}, {response.text}")
        if response.status_code == 200:
            state = response.json().get("state")
            print(f"Initial state of binary_sensor.vibration1_vibration: {state}")
        else:
            print(f"Failed to get initial state. Status code: {response.status_code}")

if __name__ == "__main__":
    home_assistant_url = HOME_ASSISTANT_BASE_URL
    token = HOME_ASSISTANT_ACCESS_TOKEN
    ha_ws = HomeAssistantWebSocket(home_assistant_url, token)
    ha_ws.connect()
