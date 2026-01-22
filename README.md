# LMU Schedule History

This project collects weekly data about the [Le Mans Ultimate] race schedule and exports it to a
[Turso] database.

## Why

Fun!

After a while, there will be enough data to do some fun analysis on.

## How do I get the data?

The point of this project _is_ to be open source, including the data. However, as I am using
Turso's free tier, I don't want to give direct database access to avoid exceeding my quotas.

Right now, there is no way for anyone other than me to access the data (_though to be fair,
there isn't much of it to begin with, I started recording from the 20th of January week_) but I'll
figure something out eventually. I kinda want to set up monthly GitHub releases that include a
`tsv` dump or something like that.

If you are reading this in the future and I still haven't come around to it, **open an issue** and
I'll export everything manually!

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
