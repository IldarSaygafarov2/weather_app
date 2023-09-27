from datetime import datetime


def convert_seconds_to_datetime(seconds: int, timezone: int) -> str:
    """
        Принимает секунды, конвертирует в обычное время
        используя часовой пояс
    """
    return datetime.utcfromtimestamp(seconds + timezone).strftime("%m/%d/%Y, %H:%M:%S")


def make_weather_dict(**kwargs):
    return kwargs
