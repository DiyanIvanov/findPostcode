import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findPostcode.settings')
django.setup()

import pandas as pd
from django.db import transaction
from api.models import Postcode


def update_db(data, stdout=None):
    def log(msg):
        if stdout:
            stdout.write(msg)

    def format_yyyymm(val):
        if pd.isna(val):
            return None
        val = int(val)
        return f"{val // 100}-{val % 100:02d}"



    log("Clean ONSPD data...")
    data['doterm'] = data['doterm'].apply(format_yyyymm)
    data['dointr'] = data['dointr'].apply(format_yyyymm)

    data['area'] = data['pcds'].str.extract(r'^([A-Z]{1,2})')
    data['district'] = data['pcds'].str.extract(r'^([A-Z]{1,2}[0-9][A-Z0-9]?)')

    log('Remove postcodes without Easting and Northing...')
    data = data.dropna(subset=['east1m'])

    log("Create records...")
    records = [
        Postcode(
            postcode=row['pcds'],
            area=row['area'],
            district=row['district'],
            date_introduced=row['dointr'],
            date_terminated=row['doterm'] if pd.notna(row['doterm']) else None,
            eastings=row['east1m'],
            northings=row['north1m'],
            latitude=row['lat'],
            longitude=row['long'],
        )
        for _, row in data.iterrows()
    ]

    stdout.write(f'Upserting {len(records)} postcodes...')

    batch_size = 1000
    with transaction.atomic():
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            Postcode.objects.bulk_create(
                batch,
                update_conflicts=True,
                unique_fields=['postcode'],
                update_fields=['date_terminated', 'eastings', 'northings', 'latitude', 'longitude']
            )
            log(f'  processed {min(i + batch_size, len(records))}/{len(records)}')

    log('DB update complete!')