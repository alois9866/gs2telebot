import csv
import datetime
import os
from typing import Iterable
import requests


SKIP_COLUMNS = [1]
YES_VALUE = 'да'


def get_start_date() -> datetime.date:
    start_date_param = os.getenv('START_DATE', datetime.datetime.now().strftime('%d.%m.%Y'))
    return datetime.datetime.strptime(start_date_param, '%d.%m.%Y').date()


def get_url() -> str:
    url = os.getenv('SHEET_URL')
    if not url:
        raise ValueError('SHEET_URL is not set')
    return url


def download_sheet() -> list[str]:
    resp = requests.get(get_url(), allow_redirects=True)
    if resp.status_code != 200:
        raise Exception(f'unable to get data from "{get_url()}": status_code={resp.status_code}: {resp.content}')
    return resp.content.decode().splitlines()


def get_dates(lines: Iterable[str], from_date: datetime.date = datetime.date.min) -> list[datetime.date]:
    reader = csv.DictReader(lines)

    dates = []
    for row in reader:
        date: datetime.date | None = None
        yes = True
        for i, key in enumerate(row):
            if i == 0:
                date = datetime.datetime.strptime(row[key], '%d.%m.%Y').date()
                continue
            if i in SKIP_COLUMNS:
                continue
            if row[key].lower() != YES_VALUE:
                yes = False

        if not date or date < from_date:
            continue
        if yes:
            dates.append(date)

    return dates


if __name__ == '__main__':
    print(get_dates(download_sheet(), get_start_date()))

