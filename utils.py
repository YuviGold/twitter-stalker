import csv
import logging
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def get_diff(old: dict, new: dict) -> tuple[list[str], list[str]]:
    added = list(set(new) - set(old))
    removed = list(set(old) - set(new))
    return sorted(added), sorted(removed)


def set_diff(filename: str, date: str, amount: int,
             added_names: list[str], removed_names: list[str]):
    diff = DATA_DIR / filename

    row = [date, str(amount), str(added_names), str(removed_names)]
    logging.info(f'{filename}: {date=}, {amount=}, {added_names=}, {removed_names=}')

    found = False
    rows = []
    headers = ['date', 'amount', 'added', 'removed']
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
