import os
import argparse
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str, api_key: str) -> dict:
    params = {"q": city, "appid": api_key, "units": "metric"}
    r = requests.get(BASE_URL, params=params, timeout=10)
    r.raise_for_status()  # if API returns 4xx/5xx, this throws
    d = r.json()
    return {
        "city": d["name"],
        "country": d["sys"]["country"],
        "temp_c": d["main"]["temp"],
        "feels_c": d["main"]["feels_like"],
        "humidity": d["main"]["humidity"],
        "wind_ms": d["wind"]["speed"],
        "description": d["weather"][0]["description"],
    }

def main():
    parser = argparse.ArgumentParser(description="Get current weather for a city.")
    parser.add_argument("city", help="City name, e.g. London")
    args = parser.parse_args()

    api_key = os.environ.get("OWM_API_KEY")
    if not api_key:
        raise SystemExit("Missing API key. Set OWM_API_KEY env var first.")

    try:
        w = fetch_weather(args.city, api_key)
        print(f"Weather in {w['city']}, {w['country']}: {w['temp_c']}°C "
              f"(feels {w['feels_c']}°C), {w['description']}. "
              f"Humidity {w['humidity']}%, wind {w['wind_ms']} m/s.")
    except requests.exceptions.HTTPError as e:
        # show helpful API error from server if possible
        try:
            msg = e.response.json().get("message", e.response.text)
        except Exception:
            msg = str(e)
        print(f"API error {e.response.status_code}: {msg}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")

if __name__ == "__main__":
    main()
