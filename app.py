import requests
import json
from flask import Flask, render_template, request
import pprint

app = Flask(__name__)

def get_location_key(data, chosen_city):
    for city in data:
        if city['EnglishName'] == chosen_city:
            return city['Key']

def get_forecast(weather):
    forecast_data = []
    for x in weather['DailyForecasts']:
        forecast_data.append((
            x['Date'], "Minimum", x['Temperature']['Minimum']['Value'], "F", "Maximum",
            x['Temperature']['Maximum']['Value'], "F"
        ))
    return forecast_data

@app.route('/', methods=['GET', 'POST'])
def index():
    params = {
        "apikey": "kUrnRAQGMA5cJxdYkYccpSZahGasB4Xg"
    }

    if request.method == 'POST':
        ChosenCity = request.form['city'].title()
        try:
            response = requests.get("http://dataservice.accuweather.com/locations/v1/topcities/150/", params=params)
            data = response.json()

        except json.decoder.JSONDecodeError:
            print("Błąd podczas dekodowania danych JSON.")
            return render_template('form.html')  # Render 'form.html' template in case of JSON decoding error
        else:
            print(get_location_key(data, ChosenCity))
            try:
                responseweather = requests.get(
                    "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + get_location_key(data, ChosenCity),
                    params=params
                )
                weather = responseweather.json()
                forecast_data = get_forecast(weather)
            except json.decoder.JSONDecodeError:
                print("Bład podczas dekodowania danych JSON")
                return render_template('form.html')  # Render 'form.html' template in case of JSON decoding error

            return render_template('index.html', forecast_data=forecast_data,city=ChosenCity)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
