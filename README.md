# sadge-pub

### Python scripts for getting more data from Google Takeout -> YouTube -> history -> watch-history.html

---

## Do you hate yourself for watching too much YouTube?

#### Well, sure! We all do.

But, now you can neurotically obsess over your extreme watchtimes like never before!

## Introducing, sadge-pub!

#### A one stop *Python script* that lets you go from Google Takeout's terrible dataset to one populated with video metadata, keywords, and channel insights

---

## Instructions:

1. Go to (Google Takeout)[https://takeout.google.com/settings/takeout]

2. Scroll to the bottom and check _YouTube and YouTube Music_

<img width="1440" alt="Screenshot 2023-07-16 at 1 32 12 AM" src="https://github.com/tylerckeller/sadge-pub/assets/96822088/9264231a-fa94-4b53-9b4a-ad3936660851">

3. Click _All data included_ and only select history (trust...)

<img width="1552" alt="Screenshot 2023-07-16 at 2 45 10 AM" src="https://github.com/tylerckeller/sadge-pub/assets/96822088/4a0c1b40-93a7-43c6-8765-42934fc21b06">

4. _Next Step_ -> _Create Export_

5. Download the .zip from Gmail

6. Unpack the .zip and move the watch-history.html file to the /sadge-pub/ directory

7. Run the following:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 sadge_scraper.py
```

8. Sit back, relax, and eat some popcorn while YT servers shit themselves over this **super-optimized** and not totally shit script (that will probably have to run for at least 16 hours...)

