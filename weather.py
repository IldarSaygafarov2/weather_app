import requests

import config
import utils
from db import queries as _db


def display_info(name, description, temp, speed, dt, sunrise, sunset):
    print(f"""
======================================
В городе {name} сейчас {description}
Температура воздуха: {temp} •C
Скорость ветра: {speed} м/c
Время отправки запроса: {dt}
Время восхода солнца: {sunrise}
Время заката солнца: {sunset}
======================================
""")


def get_weather():
    username = input('Enter your username: ')
    is_exists, user_id = _db.check_user_exists("weather.db", username)
    if not is_exists:
        print('[INFO] такого юзера нету')
        _db.add_user("weather.db", username)
        get_weather()
    else:
        while True:
            city = input("Введите название города, в котором хотите узнать погоду: ")

            if city == "show":
                data = _db.get_weather_data("weather.db", user_id)

                if not data:
                    print('нету данных')
                    continue

                for item in data:
                    name, temp, _, dt, sunset, sunrise, description, speed = item[1:-1]
                    display_info(name, description, temp, speed, dt, sunrise, sunset)
                continue

            if city == "save":
                weather = _db.get_all_weather("weather.db")
                result = []
                keys = ["weather_id","name", "temp", "tz", "dt", "sunset", "sunrise", "description", "speed", "user_id"]
                for item in weather:
                    result.append(dict(zip(keys, item)))
                print(result)

                continue

            if city == "restart":
                get_weather()
                continue

            if city == "clear":
                _db.delete_user_weather("weather.db", user_id)
                print('данные очищены')
                continue

            config.parameters["q"] = city

            response = requests.get(config.url, params=config.parameters).json()
            # pprint(response)  # dt, temp, name, sunrise, sunset, description, speed

            name = response["name"]
            temp = response["main"]["temp"]
            tz = response["timezone"]
            dt = utils.convert_seconds_to_datetime(seconds=response["dt"], timezone=tz)
            sunrise = utils.convert_seconds_to_datetime(seconds=response["sys"]["sunrise"], timezone=tz)
            sunset = utils.convert_seconds_to_datetime(seconds=response["sys"]["sunset"], timezone=tz)
            description = response["weather"][0]["description"]
            speed = response["wind"]["speed"]

            # добавление данных в таблицу
            _db.add_weather("weather.db",
                            city_name=name,
                            temp=temp,
                            timezone=tz,
                            created_at=dt,
                            sunset=sunset,
                            sunrise=sunrise,
                            description=description,
                            wind_speed=speed,
                            user_id=user_id)

            display_info(name, description, temp, speed, dt, sunrise, sunset)
