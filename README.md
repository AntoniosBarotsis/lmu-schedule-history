# LMU Schedule History

This project collects weekly data about the [Le Mans Ultimate] race schedule and exports it to a
[Turso] database.

## Why

Fun!

After a while, there will be enough data to do some fun analysis on.

## How do I get the data?

To avoid exceeding Turso's free tier quotas, I'll automatically export the database as a `tsv` file
and upload it in a GitHub [releases] on the **first of each month**.

## What data is being collected?

I just have one table that corresponds to the following class:

```py
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
```

## Attributions

The data is collected from <https://www.lmuschedule.com/>.

[Le Mans Ultimate]: https://lemansultimate.com
[Turso]: https://turso.tech
[releases]: https://github.com/AntoniosBarotsis/lmu-schedule-history/releases/latest
