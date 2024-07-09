from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
import argparse
from datetime import datetime
import pytz
from config import OPENAI_API_KEY, DEFAULT_LOCATION, ASSISTANT_PROMPT, WEATHER_API_KEY
from speech_handler import SpeechHandler
from services.weather_api import WeatherHandler

# Initialize OpenAI

def get_weather(location=DEFAULT_LOCATION):
    weather_handler = WeatherHandler(WEATHER_API_KEY)
    condition, temp = weather_handler.get_weather()
    if condition and temp:
        return f"Weather condition: {condition}, Temperature: {temp}°C"
    else:
        return "Failed to fetch weather data"

def get_current_time(location=DEFAULT_LOCATION):
    location_mapping = {
        "New York": "America/New_York",
        "Berlin": "Europe/Berlin",
        "Munich": "Europe/Berlin"
    }
    timezone = location_mapping.get(location, "Etc/UTC")
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime(f"Aktuelle Uhrzeit in {location}: %Y-%m-%d %H:%M:%S")

def get_response_from_chatgpt(api_key, messages, functions, model="gpt-4-0613"):
    response = client.chat.completions.create(api_key=api_key,
    model=model,
    messages=messages,
    functions=functions,
    function_call="auto")
    return response

def main():
    parser = argparse.ArgumentParser(description="Chat with SMARIOT from the command line.")
    parser.add_argument("--model", type=str, default="gpt-4-0613", help="The model to use (default: gpt-4-0613)")
    args = parser.parse_args()

    functions = [
        {
            "name": "get_weather",
            "description": "Get the current weather for the default location.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    ]

    messages = [
        {"role": "system", "content": ASSISTANT_PROMPT},
        {"role": "user", "content": "Hallo! Wie geht's?"}
    ]

    print("Chat with SMARIOT. Type 'exit' to end the conversation.")
    speech_handler = SpeechHandler()
    while True:
        print("you:")
        prompt = speech_handler.speech_to_text_from_mic()
        if prompt.lower() == "exit":
            break

        messages.append({"role": "user", "content": prompt})
        response = get_response_from_chatgpt(OPENAI_API_KEY, messages, functions, args.model)
        reply = "Ich habe leider nichts verstanden"
        # Handle function call
        if response.choices[0].finish_reason == "function_call":
            function_call = response.choices[0].message.function_call
            function_name = function_call["name"]

            if function_name == "get_weather":
                weather_info = get_weather()
                current_time_info = get_current_time()
                full_response = weather_info + current_time_info
                messages.append({"role": "function", "name": "get_weather", "content": full_response})

                # Pass the weather info back to ChatGPT for further processing
                response = get_response_from_chatgpt(OPENAI_API_KEY, messages, functions, args.model)
                reply = response.choices[0].message.content
                print(f"SMARIOT: {reply}")
                messages.append({"role": "assistant", "content": reply})
            elif function_name == "get_current_time":
                current_time_info = get_current_time()
                messages.append({"role": "function", "name": "get_current_time", "content": current_time_info})

                # Pass the time info back to ChatGPT for further processing
                response = get_response_from_chatgpt(OPENAI_API_KEY, messages, functions, args.model)
                reply = response.choices[0].message.content
                print(f"SMARIOT: {reply}")
                messages.append({"role": "assistant", "content": reply})
            else:
                reply = f"SMARIOT: Ich bin mir nicht sicher, wie ich die Funktion '{function_name}' ausführen soll."
                print(reply)
        else:
            reply = response.choices[0].message.content
            print(f"SMARIOT: {reply}")
            messages.append({"role": "assistant", "content": reply})

            if len(messages) > 10 and all(msg['role'] == 'assistant' for msg in messages[-5:]):
                weather_info = get_weather()
                current_time_info = get_current_time()
                full_weather_info = f"{weather_info} {current_time_info}"
                messages.append({"role": "function", "name": "get_weather", "content": full_weather_info})
                print(f"SMARIOT: {full_weather_info}")
                reply = full_weather_info
        speech_handler.text_to_speech(reply)

if __name__ == "__main__":
    main()
