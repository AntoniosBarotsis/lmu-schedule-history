import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime, timedelta

def previous_tuesday():
    date=datetime.now()
    days_since_tuesday = (date.weekday() - 1) % 7
    return date - timedelta(days=days_since_tuesday)

@dataclass
class Event:
    title: str
    track: str
    sr: str
    duration: str

def main():
    res = requests.get('https://www.racecontrol.gg')
    soup = BeautifulSoup(res.content, 'html.parser')
    # print(soup.prettify())

    content = soup.css.select("body > div.container > section:nth-child(1) > div > div > ul > li > div > div > div.race-info > h4")
    event_titles = [el.contents[0] for el in content]

    content = soup.css.select("body > div.container > section:nth-child(1) > div > div > ul > li > div > div > div.race-info > div:nth-child(3) > span:nth-child(3)")
    event_tracks = [el.contents[0].strip() for el in content]

    content = soup.css.select("body > div.container > section:nth-child(1) > div > div > ul > li > div > div > div.race-info > div:nth-child(2) > span:nth-child(3)")
    event_durations = [el.contents[0].strip() for el in content]

    content = soup.css.select("body > div.container > section:nth-child(1) > div > div > ul > li > div > div > div > span")
    event_sr = [el.contents[2].strip() for el in content]

    events = []
    for i in range(len(event_titles)):
        events.append(Event(event_titles[i], event_tracks[i], event_durations[i], event_sr[i]))

    for event in events:
        print(event)
        
    last_tuesday = previous_tuesday()
    print(f"Most recent Tuesday: {last_tuesday.date()}")

if __name__ == "__main__":
    main()
# body > div.container > section:nth-child(1) > div.glide.position-relative.glide--ltr.glide--slider.glide--swipeable > div > ul