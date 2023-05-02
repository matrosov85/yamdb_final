"""
Кастомная management-команда Django для импорта данных из csv фалйов
в базу данных с помощью Django ORM.

Использование:
$ python manage.py csv_import [--csv file_name] [--model model_name]
                              [--app app_name]

Пример использования:
$ python manage.py csv_import --csv titles.csv --model Title --app reviews

Если все параметры указаны верно, то в результате в модель Title
из приложения reviews будут импортированы данные из фалйа titles.csv
и в терминале появится сообщение:

Загузка данных из файла titles.csv в модель Title
Записей добавлено: 32
"""

import os
import csv

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import ForeignKey

from api_yamdb.settings import TEST_DB_DIR


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str)
        parser.add_argument('--model', type=str)
        parser.add_argument('--app', type=str)

    def handle(self, *args, **options):
        file_name = options['csv']
        file_path = os.path.join(TEST_DB_DIR, file_name)
        model = apps.get_model(options['app'], options['model'])
        with open(file_path, encoding='utf-8') as csv_file:
            print(f'Загузка данных из файла {file_name} '
                  f'в модель {model.__name__}')
            reader = csv.DictReader(csv_file)
            record_count = 0
            for row in reader:
                record = {}
                for key, value in row.items():
                    model_field = model._meta.get_field(key)
                    if (
                        isinstance(model_field, ForeignKey)
                        and not key.endswith('_id')
                    ):
                        related_model = model_field.remote_field.model
                        record[key] = related_model.objects.get(pk=value)
                    else:
                        record[key] = value
                model.objects.update_or_create(**record)
                record_count += 1
            print(f'Записей добавлено: {record_count}')
