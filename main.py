#!/usr/bin/env python


import csv
import json
import logging
import os
import subprocess
from contextlib import suppress
from datetime import datetime
from pathlib import Path

TWITTER_TOKEN = os.environ['TWITTER_TOKEN']
TWITTER_USER = os.environ['TWITTER_USER']
DEFAULT_TIMEOUT = 10
DEFAULT_COUNT = 200
TWITTER_BASEURL = "https://api.twitter.com/1.1"
DATA_DIR = Path(__file__).parent / "data"


def get_twitter_followers(username: str, count: int) -> dict:
    command = f'curl -s "{TWITTER_BASEURL}/followers/list.json?screen_name={username}&count={count}" -H "Authorization: Bearer {TWITTER_TOKEN}"'
    output = subprocess.getoutput(command)
    return json.loads(output)


def get_followers(username: str) -> dict:
    data = get_twitter_followers(username, DEFAULT_COUNT)
    data = {user['id_str']: {'screen_name': user['screen_name'], 'name': user['name']} for user in data['users']}
    return data


def get_diff(old: dict, new: dict) -> tuple[list[str], list[str]]:
    added = list(set(new) - set(old))
    removed = list(set(old) - set(new))
    return sorted(added), sorted(removed)


def set_diff(date: str, followers: int,
             added_names: list[str], removed_names: list[str]):
    diff = DATA_DIR / 'diff.csv'

    row = [date, str(followers), str(added_names), str(removed_names)]
    logging.info(row)

    found = False
    rows = []
    headers = ['date', 'followers', 'added', 'removed']
    if diff.exists():
        with diff.open('r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = [r for r in reader]
            for i, r in enumerate(rows):
                if r[0] == date:
                    found = True
                    rows[i] = row
                    break

    if not found:
        rows.append(row)

    with diff.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def convert_id_to_display_entry(ids: list[str], data: dict) -> list[str]:
    return list(map(lambda id: f"{data[id]['name']} ({data[id]['screen_name']})", ids))


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = get_followers(TWITTER_USER)
    today = datetime.now().strftime('%Y_%m_%d')

    with suppress(FileExistsError):
        os.makedirs(DATA_DIR)

    latest_file = DATA_DIR / 'latest.json'
    today_file = DATA_DIR / f'{today}.json'

    with today_file.open('w') as f:
        json.dump(data, f, indent=4)

    latest_data = {}
    if latest_file.exists():
        with latest_file.open('r') as f:
            latest_data = json.load(f)

    added, removed = get_diff(latest_data, data)
    set_diff(today.replace('_', '/'),
             len(data),
             convert_id_to_display_entry(added, data),
             convert_id_to_display_entry(removed, latest_data))

    latest_file.unlink(missing_ok=True)
    today_file.rename(latest_file)


if __name__ == '__main__':
    main()
