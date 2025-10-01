import requests
from django.shortcuts import render

def get_weather(request):
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            url = f'http://wttr.in/{city}?format=j1&lang=ru'
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                # Извлечём данные
                current_condition = data['current_condition'][0]
                weather_data = {
                    'city': city.title(),
                    'temp': current_condition['temp_C'],
                    'description': current_condition['lang_ru'][0]['value'],
                    'feels_like': current_condition['FeelsLikeC'],
                    'humidity': current_condition['humidity'],
                    'wind': current_condition['windspeedKmph'],
                }
            except Exception:
                error = 'Ошибка получения данных о погоде. Проверьте название города.'
        else:
            error = 'Введите название города.'

    return render(request, 'forecast/weather.html', {'weather': weather_data, 'error': error})


