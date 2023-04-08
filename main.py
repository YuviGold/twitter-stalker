#!/usr/bin/env python


import json
import logging
import os
from contextlib import suppress
from datetime import datetime

from api import get_twitter_followers, get_twitter_friends
from utils import DATA_DIR, convert_id_to_display_entry, get_diff, set_diff

TWITTER_USER = os.environ['TWITTER_USER']


def calculate_diff(prefix: str, data: dict):
    today = datetime.now().strftime('%Y_%m_%d')
    latest_file = DATA_DIR / f'{prefix}_latest.json'
    today_file = DATA_DIR / f'{prefix}_{today}.json'

    with today_file.open('w') as f:
        json.dump(data, f, indent=4)

    latest_data = {}
    if latest_file.exists():
        with latest_file.open('r') as f:
            latest_data = json.load(f)

    added, removed = get_diff(latest_data, data)
    set_diff(f'{prefix}_diff.csv',
             today.replace('_', '/'),
             len(data),
             convert_id_to_display_entry(added, data),
             convert_id_to_display_entry(removed, latest_data))

    latest_file.unlink(missing_ok=True)
    today_file.rename(latest_file)


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    with suppress(FileExistsError):
        os.makedirs(DATA_DIR)

    calculate_diff('followers', get_twitter_followers(TWITTER_USER))
    calculate_diff('friends', get_twitter_friends(TWITTER_USER))


if __name__ == '__main__':
    main()
