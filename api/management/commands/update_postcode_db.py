from django.core.management.base import BaseCommand, CommandError
import urllib.request
import tempfile
import zipfile
import os
import pandas as pd

from api.services.db_update_with_onspd import update_db


class Command(BaseCommand):
    help = 'Update postcode DB with ONSPD data from a given URL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            required=True,
            help='Download URL for the ONSPD file from ONS portal'
        )

    def handle(self, *args, **options):
        url = options['url']

        with tempfile.TemporaryDirectory(prefix='onspd_') as tmp_dir:
            zip_path = os.path.join(tmp_dir, 'data.zip')
            self.stdout.write(f'Temp folder: {tmp_dir}')

            self.stdout.write('Downloading ONSPD zip...')
            urllib.request.urlretrieve(url, zip_path)

            self.stdout.write('Extracting CSV...')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extract('Data/ONSPD_FEB_2026_UK.csv', tmp_dir)

            postcode_data = pd.read_csv(os.path.join(tmp_dir, 'Data/ONSPD_FEB_2026_UK.csv'))
            self.stdout.write(f'{postcode_data.shape}')

            update_db(postcode_data, self.stdout)
