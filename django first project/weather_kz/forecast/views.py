import requests
from django.shortcuts import render
from datetime import datetime

def get_weather(request):
    weather_data = None
    error = None

    def fix_icon_url(url):
        if url.startswith('http://'):
            return url.replace('http://', 'https://')
        return url

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            url = f'http://wttr.in/{city}?format=j1&lang=ru'
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                current_condition = data['current_condition'][0]
                today_date = datetime.now().strftime('%d %B %Y')

                forecast_days = []
                for day in data['weather']:
                    icon_url = fix_icon_url(day['hourly'][4]['weatherIconUrl'][0]['value'])
                    day_info = {
                        'date': day['date'],
                        'maxtemp': day['maxtempC'],
                        'mintemp': day['mintempC'],
                        'avgtemp': day['avgtempC'],
                        'description': day['hourly'][4]['lang_ru'][0]['value'],
                        'icon_url': icon_url,
                    }
                    forecast_days.append(day_info)

                hourly_forecast = []
                for hour in data['weather'][0]['hourly']:
                    icon_url = fix_icon_url(hour['weatherIconUrl'][0]['value'])
                    time_raw = int(hour['time'])
                    hour_str = f"{time_raw // 100:02d}:00"
                    hourly_forecast.append({
                        'time': hour_str,
                        'temp': hour['tempC'],
                        'description': hour['lang_ru'][0]['value'],
                        'icon_url': icon_url,
                    })

                weather_data = {
                    'city': city.title(),
                    'temp': current_condition['temp_C'],
                    'feels_like': current_condition['FeelsLikeC'],
                    'description': current_condition['lang_ru'][0]['value'],
                    'humidity': current_condition['humidity'],
                    'wind': current_condition['windspeedKmph'],
                    'date': today_date,
                    'forecast': forecast_days,
                    'hourly': hourly_forecast,
                }
            except Exception as e:
                error = 'Ошибка получения данных о погоде. Проверьте название города.'
        else:
            error = 'Введите название города.'

    return render(request, 'forecast/weather.html', {'weather': weather_data, 'error': error})
