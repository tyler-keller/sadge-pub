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
        # Extract the matched group and convert it to a list
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

# Define a function to scrape data from a YouTube video page
def scrape_youtube_video(video_link):
    # Send a GET request to the video URL
    response = requests.get(video_link)

    # Load the page content into BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the required data
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
    while True:
        try:
            # Attempt to make the request
            data = scrape_youtube_video(url)
            return data
        except ConnectionError:
            # If a ConnectionError is raised, wait a few seconds and try again
            print("ConnectionError occurred. Waiting 10 seconds before retrying...")
            time.sleep(10)

# Open the file and read its content
with open('/mnt/data/watch-history.html', 'r') as file:
    content = file.read()

# Load the HTML content into BeautifulSoup using lxml parser
soup = BeautifulSoup(content, 'lxml')

# Find all the containers
containers = soup.find_all('div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')

# Initialize lists to store the extracted data
video_links = []
dates = []

# Iterate over the containers and extract the required information
for container in containers:
    # Find the 'a' tags within the container
    a_tags = container.find_all('a')
    
    # Check if the container has 'a' tags
    if a_tags:
        # The first 'a' tag contains the video link and title
        video_links.append(a_tags[0]['href'])
        
        # The date is the last piece of text within the container, after the second 'br' tag
        date = list(container.stripped_strings)[-1]
        dates.append(date)

# Create a DataFrame
df = pd.DataFrame({
    'video_link': video_links,
    'date': dates
})

# Load the CSV file into a DataFrame
df = pd.read_csv('watch_history.csv')

# Initialize an empty list to store the data
data = []

num_rows = 0
# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    video_link = row['video_link']
    date = row['date']

    # Scrape data from the video link
    video_data = robust_request(video_link)

    # Add the date to the video data
    video_data['watch_date'] = date

    # Add the video data to the list
    data.append(video_data)

    num_rows += 1

    time.sleep(.5)

    if num_rows > 50:
        # Convert the list of data to a DataFrame and save it to a CSV file
        pd.DataFrame(data).to_csv('expanded_watch_history.csv', index=False)
        num_rows = 0
