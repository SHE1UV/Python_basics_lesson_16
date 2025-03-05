# Визуализация погодных данных

## Описание

Данный проект позволяет получить данные о погоде для указанного города, используя его координаты (широта и долгота), и построить график изменения температуры за выбранный период. Координаты города запрашиваются через API Opendatasoft, а данные о погоде — через Open-Meteo API. Погодные данные кэшируются локально, чтобы избежать повторных запросов к API.

## Функции проекта

* Получение координат города по его названию и коду страны.
* Получение почасовых данных о температуре с помощью Open-Meteo API за указанный диапазон дат.
* Построение графика изменения температуры с использованием библиотеки Matplotlib.
* Кэширование данных для предотвращения повторных запросов.

## Установка

1. Убедитесь, что у вас установлен Python версии 3.6 или выше.
2. Для работы с библиотекой matplotlib==3.10.1 в Windows может потребоваться установка Microsoft C++ Build Tools версии 14 и выше.
  * Установите Microsoft C++ Build Tools 14+ с официального сайта.
  * При установке выберите опцию "Desktop development with C++"
3. Убедитесь, что установлена библиотека NumPy.
  * Обычно NumPy устанавливается автоматически как зависимость Matplotlib, но если возникают ошибки, установите его вручную:

```bash
 pip install numpy
```
Зачем это нужно?

`matplotlib` использует `numpy` для работы с массивами чисел и математическими операциями. Если `numpy` не установлен, `matplotlib` может не работать.

4. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/ваш_пользователь/название_проекта.git
   cd название_проекта
   ```

4. Установите необходимые зависимости(библиотека NumPy там уже присутсвтует):

    ```bash
    pip install -r requirements.txt
    ```

## Использование

Для запуска скрипта введите в командной строке:

    ```bash
    python main.py <city_name> <country_code> <start_date> <end_date>
    ```

* <city_name> — название города (например, "Minsk").
* <country_code> — код страны (например, "BY" для Беларуси).
* <start_date> — начальная дата периода (в формате YYYY-MM-DD).
* <end_date> — конечная дата периода (в формате YYYY-MM-DD).

Пример:

    ```bash
    python main.py Minsk BY 2024-10-01 2024-10-07
    ```

## Требования к API

1. [Opendatasoft API](https://data.opendatasoft.com/api/explore/v2.1/console): для получения координат городов.
2. [Open-Meteo API](https://open-meteo.com/): для получения данных о погоде.

## Цели проекта

Код написан в учебных целях — для курса по Python на сайте [Devman](https://dvmn.org).
