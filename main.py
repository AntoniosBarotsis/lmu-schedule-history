import requests
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import warnings
import db
from dotenv import load_dotenv
import os

def is_dev() -> bool:
    dev = True
    mode = os.getenv("MODE")
    if mode is not None and mode.lower() == "production":
        dev = False
    
    return dev

def load_data_mock() -> dict:
    warnings.warn("Warning: Using mock data!")

    with open('res.json') as f:
        return json.load(f)
    
def load_data() -> dict:
    # TODO: Only really need `referer`. Delete the rest? Add `User-Agent`
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.lmuschedule.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.lmuschedule.com/',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }

    response = requests.get('https://api.lmuschedule.com/racingschedules', headers=headers)

    return response.json()

def previous_tuesday() -> datetime:
    date=datetime.now()
    days_since_tuesday = (date.weekday() - 1) % 7
    return date - timedelta(days=days_since_tuesday)

@dataclass
class Event:
    date: str
    race_type: str
    series: str
    difficulty: str
    circuit: str
    setup: str
    tire_warmers: str
    assists: str
    car_classes: list[str]
    fuel_usage: str
    tire_wear: int
    split_size: list[int]
    practice_length: int
    qualifying_length: int
    race_length: int
    safety_rank: str
    driver_rank: str
    damage: str
    driver_swaps: str
    track_limits: str
    limited_tires: str

def parse(body: dict) -> Event:
    # splitSize is sometimes just a number instead of a list, always make it a list
    split_size = body['splitSize']
    if isinstance(split_size, int):
        split_size = [split_size]

    return Event(
        date = previous_tuesday().strftime('%Y-%m-%d'),
        race_type = body['raceType'],
        series = body['series'],
        difficulty = body['difficulty'],
        circuit = body['circuit'],
        setup = body['setup'],
        tire_warmers = body['tireWarmers'],
        assists = body['assists'],
        car_classes = body['carClasses'],
        fuel_usage = body['fuelUsage'],
        tire_wear = body['tireWear'],
        split_size = split_size,
        practice_length = body['practiceLength'],
        qualifying_length = body['qualifyingLength'],
        race_length = body['raceLength'],
        safety_rank = body['safetyRank'],
        driver_rank = body['driverRank'],
        damage = body['damage'],
        driver_swaps = body['driverSwaps'],
        track_limits = body['trackLimits'].lower(),
        limited_tires = body['limitedTires'],
    )

def main(conn):
    res = None
    if is_dev():
        res = load_data_mock()
    else:
        res = load_data()

    db.ensure_init(conn)

    for event in res['body']:
        parsed = parse(event)

        exists = db.row_exists(conn, parsed.date, parsed.race_type, parsed.series)
        if not exists:
            db.row_insert(conn, parsed)

if __name__ == "__main__":
    load_dotenv()

    conn = db.get_conn(is_dev())

    if os.getenv('EXPORT') == "True":
        print('Exporting')
        db.export_tsv(conn)
    else:
        main(conn)

