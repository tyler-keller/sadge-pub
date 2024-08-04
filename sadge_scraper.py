import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

def get_title(html):
    match = re.search(r'"title":\s*{\s*"simpleText":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_category(html):
    match = re.search(r'"category":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_length(html):
    match = re.search(r'"lengthSeconds":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_video_id(html):
    match = re.search(r'"videoId":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_keywords(html):
    match = re.search(r'"keywords":\s*\[(.*?)\]', html)
    if match:
        keywords_string = '[' + match.group(1) + ']'
        keywords_list = json.loads(keywords_string)
        return keywords_list
    else:
        return None

def get_thumbnail(html):
    match = re.search(r'"url":\s*"([^"]*)",\s*"width":\s*1920,\s*"height":\s*1080', html)
    return match.group(1) if match else None

def get_upload_date(html):
    match = re.search(r'"uploadDate":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_view_count(html):
    match = re.search(r'"viewCount":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_channel_id(html):
    match = re.search(r'"channelId":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_author(html):
    match = re.search(r'"author":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def get_channel_profile(html):
    match = re.search(r'"ownerProfileUrl":\s*"([^"]*)"', html)
    return match.group(1) if match else None

def scrape_youtube_video(video_link):
    response = requests.get(video_link)

    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "video_url": video_link,
        "video_title": get_title(str(soup)),
        "length_seconds": get_length(str(soup)),
        "keywords": get_keywords(str(soup)),
        "thumbnail": get_thumbnail(str(soup)),
        "view_count": get_view_count(str(soup)),
        "category": get_category(str(soup)),
        "upload_date": get_upload_date(str(soup)),
        "channel_id": get_channel_id(str(soup)),
        "channel_name": get_author(str(soup)),
        "channel_url": get_channel_profile(str(soup)),
    }

    return data

def robust_request(url):
    count = 0
    while True:
        try:
            data = scrape_youtube_video(url)
            return data
        except Exception as e:
            count += 1
            print("ConnectionError occurred. Waiting 10 seconds before retrying...")
            time.sleep(10)
            if count >= 3:
                count = 0
                raise e

print("Parsing watch history.html")

# if html:
# with open('watch-history.html', 'r') as file:
#     content = file.read()

# soup = BeautifulSoup(content, 'lxml')

# containers = soup.find_all('div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')

# video_links = []
# dates = []

# for container in containers:
#     a_tags = container.find_all('a')
    
#     if a_tags:
#         video_links.append(a_tags[0]['href'])
        
#         date = list(container.stripped_strings)[-1]
#         dates.append(date)

# df = pd.DataFrame({
#     'video_link': video_links,
#     'date': dates
# })
    
# print("Finished parsing the watch history.html")
# print(df.head(10))
from datetime import datetime
import time

df = pd.read_json('./data/history/watch-history.json')
date_string = datetime.now().strftime('%Y_%m_%d')

data = []

num_rows = 0
for index, row in df.iterrows():

    video_link = row['titleUrl']

    try:
        video_data = robust_request(video_link)
    except Exception as e:
        print(f"Failed to scrape {video_link}")
        print(e)
        continue

    video_data['watch_date'] = row['time']

    data.append(video_data)

    num_rows += 1

    time.sleep(.01)

    if num_rows > 50:
        pd.DataFrame(data).to_csv(f'expanded_watch_history_{date_string}.csv', index=False)
        print(f"Saved the data to expanded_watch_history.csv ({index}/{df.shape[0]})")
        num_rows = 0

    print(f"Processed row {index}/{len(df)}")

pd.DataFrame(data).to_csv(f'expanded_watch_history_{date_string}.csv', index=False)

print("Finished scraping the watch history")