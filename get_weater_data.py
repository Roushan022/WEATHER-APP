# import requests
# from geopy.geocoders import Nominatim as N

# geolocator = N(user_agent="my_app")
# city = input("Enter city name: ")
# location = geolocator.geocode(city)
# lat=location.latitude
# lon=location.longitude
# if location:
#     print("City:", location.address)
#     print("Latitude:", location.latitude)
#     print("Longitude:", location.longitude)
# else:
#     print("City not found")

# API_key="bf88b2600613afddeed0fdf0847c3526"
# url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric"
# response=requests.get(url)
# if response.status_code==200:
#     data=response.json()
#     print(data['weather'][0]['main'])
#     temp_kel=data['main']['temp']
#     print(temp_kel)

import requests
from geopy.geocoders import Nominatim as N
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

geolocator = N(user_agent="my_app")

API_key = "bf88b2600613afddeed0fdf0847c3526"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/weather")
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Enter city name"}), 400

    location = geolocator.geocode(city)

    if location:
        lat = location.latitude
        lon = location.longitude
    else:
        return jsonify({"error": "City not found"}), 404

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        weather_main = data['weather'][0]['main']
        temp_kel = data['main']['temp']

        return jsonify({
            "city": location.address,
            "temperature": temp_kel,
            "weather": weather_main
        })

    else:
        return jsonify({"error": "Weather data not found"}), response.status_code


if __name__ == "__main__":
    app.run(debug=True)