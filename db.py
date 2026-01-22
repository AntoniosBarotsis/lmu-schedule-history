from main import Event
import warnings
from libsql import libsql
import os
import csv

def get_conn(dev=False):
    if dev:
        warnings.warn("Warning: Using mock database!")
        return libsql.connect("test.db")
    else:
        dbname = os.getenv("TURSO_DATABASE_NAME")
        url = os.getenv("TURSO_DATABASE_URL")
        auth_token = os.getenv("TURSO_AUTH_TOKEN")

        conn = libsql.connect(dbname, sync_url=url, auth_token=auth_token)
        conn.sync()
        return conn


def ensure_init(conn):
    create_table = """
      CREATE TABLE IF NOT EXISTS events(
          date TEXT,
          race_type TEXT,
          series TEXT,
          difficulty TEXT,
          circuit TEXT,
          setup TEXT,
          tire_warmers TEXT,
          assists TEXT,
          car_classes TEXT,
          fuel_usage TEXT,
          tire_wear INTEGER,
          split_size TEXT,
          practice_length INTEGER,
          qualifying_length INTEGER,
          race_length INTEGER,
          safety_rank TEXT,
          driver_rank TEXT,
          damage TEXT,
          driver_swaps TEXT,
          track_limits TEXT,
          limited_tires TEXT,

          PRIMARY KEY (date, race_type, series)
      );
          """

    conn.execute(create_table)

def row_exists(conn, date: str, race_type: str, series: str) -> bool:
    sql = """
SELECT count(*) FROM events WHERE 
    date = ? AND
    race_type = ? AND
    series = ?
"""
    cur = conn.execute(sql, (date,race_type,series,))
    count = cur.fetchone()[0]
    return count > 0

def row_insert(conn, event: Event):
    sql = """
INSERT OR IGNORE INTO events (date, race_type, series, difficulty, circuit, setup, tire_warmers, assists, car_classes, fuel_usage, tire_wear, split_size, practice_length, qualifying_length, race_length, safety_rank, driver_rank, damage, driver_swaps, track_limits, limited_tires)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

    conn.execute(sql, (event.date,
        event.race_type,
        event.series,
        event.difficulty,
        event.circuit,
        event.setup,
        event.tire_warmers,
        event.assists,
        ','.join(event.car_classes),
        event.fuel_usage,
        event.tire_wear,
        ','.join(f'{x}' for x in event.split_size),
        event.practice_length,
        event.qualifying_length,
        event.race_length,
        event.safety_rank,
        event.driver_rank,
        event.damage,
        event.driver_swaps,
        event.track_limits,
        event.limited_tires,))

    conn.commit()

def get_all(conn):
    cur = conn.execute('SELECT * FROM events;')
    names = list(map(lambda x: x[0], cur.description))

    return (names, cur.fetchall())

def export_tsv(conn):
    (names, data) = get_all(conn)

    with open('output.tsv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        
        writer.writerow(names)
        writer.writerows(data)
