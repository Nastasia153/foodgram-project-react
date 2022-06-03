import os
from django.conf import settings
from csv import DictReader
from django.core.management import BaseCommand, CommandError

from recipes.models import Ingredient

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

CSV_DIR = os.path.join(settings.BASE_DIR, 'static/data/')


class Command(BaseCommand):

    help = f"Loads data from {CSV_DIR}"

    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if Ingredient.objects.exists():
            print('ingredients data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading ingredients data")

        # Code to load the data into database
        try:
            for row in DictReader(
                    open(os.path.join(CSV_DIR, 'ingredients.csv'),
                    mode='r', encoding='utf-8', newline='')
            ):
                ingredient = Ingredient(
                    ingr_name=row['ingr_name'],
                    measurement_unit=row['measurement_unit'])
                ingredient.save()
        except Exception as error:
            raise CommandError(f'что-то пошло не так. {error}')
