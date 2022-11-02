import datetime as dt

from rest_framework import serializers


def validate_year(value):
    year = dt.date.today().year
    if not 0 < value < year:
        raise serializers.ValidationError('Проверьте год выпуска')


def validate_rating(value):
    if not 1 <= value <= 10:
        raise serializers.ValidationError('Неверно указан рейтинг')
