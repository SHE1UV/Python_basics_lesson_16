import requests_cache
import pandas as pd
from matplotlib import pyplot as plt
import requests
import argparse


def get_coordinates(city_name, country_code):
    url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records"
    params = {"where": f"place_name='{city_name}' and country_code='{country_code}'", "limit": 1, "select": "latitude,longitude"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])
        if not results:
            raise ValueError(f"Не удалось найти координаты для города '{city_name}'")
        return results[0]['latitude'], results[0]['longitude']
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка запроса: {e}")


def get_weather_info(latitude, longitude, start_date, end_date):
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {"latitude": latitude, "longitude": longitude, "start_date": start_date, "end_date": end_date, "hourly": "temperature_2m", "timezone": "Europe/Minsk"}
    
    try:
        response = cache_session.get(url, params=params)
        response.raise_for_status()
        data = response.json().get('hourly', {})
        if not data.get('temperature_2m'):
            raise ValueError("Данные о погоде отсутствуют.")
        return pd.DataFrame({'Date': pd.to_datetime(data['time']), 'Temperature': data['temperature_2m']})
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка при запросе данных OpenMeteo API: {e}")


def plot_temperature(weather_df, city_name):
    if weather_df.empty:
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
    parser.add_argument('city_name', type=str, nargs='?', default='Minsk')
    parser.add_argument('country_code', type=str, nargs='?', default='BY')
    parser.add_argument('start_date', type=str, nargs='?', default='2024-10-01')
    parser.add_argument('end_date', type=str, nargs='?', default='2024-10-07')
    args = parser.parse_args()
    
    try:
        latitude, longitude = get_coordinates(args.city_name, args.country_code)
        weather_df = get_weather_info(latitude, longitude, args.start_date, args.end_date)
        plot_temperature(weather_df, args.city_name)
    except ValueError as e:
        print(f"Ошибка: {e}")
    except RuntimeError as e:
        print(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
