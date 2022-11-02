import csv

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import (Categories, Comments, Genres, GenreTitle, Review,
                            Title, User)

PATH_TO_UPLOAD = 'static/data/'

FILES = [
    ('category.csv', Categories),
    ('genre.csv', Genres),
    ('users.csv', User),
    ('titles.csv', Title),
    ('genre_title.csv', GenreTitle),
    ('review.csv', Review),
    ('comments.csv', Comments),
]


class Command(BaseCommand):
    help = 'Загрузка scv'

    def handle(self, *args, **kwargs):
        for file_name, model in FILES:
            try:
                with open(
                        (PATH_TO_UPLOAD + file_name),
                        encoding='utf8'
                ) as file:
                    reader = csv.DictReader(file)
                    model.objects.all().delete()
                    for row in reader:
                        updated_row = {}
                        for field_name, value in row.items():
                            if field_name == 'category':
                                value = get_object_or_404(Categories, id=value)
                            elif field_name == 'author':
                                value = get_object_or_404(User, id=value)
                            updated_row[field_name] = value
                        model.objects.get_or_create(**updated_row)
                    print(file_name + ' loaded successfully')
            except Exception:
                print(file_name + ' loading failed')
