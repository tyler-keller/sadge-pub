# sadge-pub

### Python script for getting more data from Google Takeout's YouTube watch-history.html

#### A one stop *Python script* that lets you go from Google Takeout's terrible dataset to one populated with video metadata, keywords, and channel insights

---

## Instructions:

1. Go to (Google Takeout)[https://takeout.google.com/settings/takeout]

2. Scroll to the bottom and check _YouTube and YouTube Music_

3. Click _All data included_ and only select history

4. _Next Step_ -> _Create Export_

5. Download the .zip from Gmail

6. Run the following:

```
git clone https://github.com/tyler-keller/sadge-pub.git`
```

9. Unpack the .zip and move the watch-history.html file to the ./sadge-pub/ directory

10. Run the following:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 sadge_scraper.py
```
  
Note: length of time to completion subject to watchtimes.

