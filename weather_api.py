from flask import Flask, request, jsonify
import os, requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.environ.get("OWM_API_KEY")

app = Flask(__name__)

@app.route("/weather", methods=["GET"])
def weather():
    # Ensure the server has an API key
    if not API_KEY:
        return jsonify({"error": "Server missing OWM_API_KEY"}), 500

    # Read ?city=... from the query string
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Please provide ?city=Name"}), 400

    try:
        r = requests.get(
            BASE_URL,
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10
        )
        r.raise_for_status()
        d = r.json()
        result = {
            "city": d["name"],
            "country": d["sys"]["country"],
            "temperature_c": d["main"]["temp"],
            "description": d["weather"][0]["description"],
            "humidity": d["main"]["humidity"],
            "wind_ms": d["wind"]["speed"],
        }
        return jsonify(result)
    except requests.exceptions.HTTPError as e:
        # Return the API's helpful error if present
        try:
            msg = e.response.json().get("message", e.response.text)
        except Exception:
            msg = str(e)
        return jsonify({"error": msg}), e.response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error: {e}"}), 503

if __name__ == "__main__":
    app.run(debug=True)
