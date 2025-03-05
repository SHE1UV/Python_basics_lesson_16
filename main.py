import requests_cache
import pandas as pd
from matplotlib import pyplot as plt
import requests
import argparse


def get_coordinates(city_name, country_code):
    url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records"

    params = {
        "where": f"place_name='{city_name}' and country_code='{country_code}'",
        "limit": 1,
        "select": "latitude,longitude",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  

        if response.json().get('total_count', 0) == 0:
            print(f"Город '{city_name}' не найден.")
            return None, None

        results = response.json().get('results', [])
        if results:
            latitude = results[0].get('latitude')
            longitude = results[0].get('longitude')

            if latitude is not None and longitude is not None:
                return latitude, longitude
            else:
                print(f"Координаты для города '{city_name}' не найдены.")
        else:
            print(f"Данные о городе '{city_name}' отсутствуют в ответе.")

    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")

    return None, None


def get_weather_info(latitude, longitude, start_date, end_date):
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": "Europe/Minsk"
    }

    try:
        response = cache_session.get(url, params=params)
        response.raise_for_status()

        if 'hourly' in response.json() and 'temperature_2m' in response.json()['hourly']:
            dates = response.json()['hourly']['time']
            temperatures = response.json()['hourly']['temperature_2m']

            weather_df = pd.DataFrame({'Date': pd.to_datetime(dates), 'Temperature': temperatures})
            return weather_df

        else:
            print("Данные о погоде отсутствуют.")
            return None

    except requests.RequestException as e:
        print(f"Ошибка при запросе данных OpenMeteo API: {e}")
        return None


def plot_temperature(weather_df, city_name):
    if weather_df is None or weather_df.empty:
        print("Нет данных для построения графика.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(weather_df['Date'], weather_df['Temperature'], marker='o')
    plt.title(f'График температуры в {city_name}')
    plt.xlabel('Дата')
    plt.ylabel('Температура (°C)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Получение погодных данных для указанного города и построение графика.")
    
    parser.add_argument('city_name', type=str, nargs='?', default='Minsk', help="Название города (по умолчанию 'Minsk')")
    parser.add_argument('country_code', type=str, nargs='?', default='BY', help="Код страны (по умолчанию 'BY')")
    parser.add_argument('start_date', type=str, nargs='?', default='2024-10-01', help="Начальная дата в формате YYYY-MM-DD (по умолчанию '2024-10-01')")
    parser.add_argument('end_date', type=str, nargs='?', default='2024-10-07', help="Конечная дата в формате YYYY-MM-DD (по умолчанию '2024-10-07')")

    args = parser.parse_args()

    city_name = args.city_name
    country_code = args.country_code
    start_date = args.start_date
    end_date = args.end_date
    
    latitude, longitude = get_coordinates(city_name, country_code)
    if latitude is None or longitude is None:
        print(f"Не удалось получить координаты для города '{city_name}'")
        return

    weather_df = get_weather_info(latitude, longitude, start_date, end_date)
    if weather_df is not None:
        plot_temperature(weather_df, city_name)


if __name__ == "__main__":
    main()








