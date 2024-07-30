# @author: Felix Patryjas - https://github.com/schwienernitzel
# @date: 25-06-2024
# @title: Python-Script to auto-search YouTube videos and write their IDs ordered by year into a text file.
# @version: v1.5

from googleapiclient.discovery import build
from datetime import datetime
from time import sleep
import os
import langid
import sys

api_key = os.getenv('APIKEY')

if not api_key:
    print("\033[91mERROR: No Google API-Key found in the current runtime! Aborting...\033[0m")
    sleep(2)
    sys.exit(1)

print("Connecting to YouTube-API...")
youtube = build('youtube', 'v3', developerKey=api_key)
sleep(1)

def search_videos(query, start_date, end_date, max_results=50):
    print(f"Searching for year {start_date[:4]}...")
    search_request = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=max_results,
        publishedAfter=start_date,
        publishedBefore=end_date,
        relevanceLanguage='de'
    )
    search_response = search_request.execute()
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    return video_ids

def get_video_details(video_id):
    video_request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )
    video_response = video_request.execute()
    if not video_response['items']:
        return None
    video_details = video_response['items'][0]
    title = video_details['snippet']['title']
    comments_enabled = 'commentCount' in video_details['statistics']

    if langid.classify(title)[0] != 'de':
        return None

    return title, comments_enabled

print("Initializing python dictionary...")
start_date = datetime(year=2015, month=1, day=1).isoformat() + 'Z'
end_date = datetime(year=2024, month=12, day=31).isoformat() + 'Z'
videos_by_year = {str(year): [] for year in range(2015, 2025)}
sleep(1)

print("Conducting search query...")
for year in range(2015, 2025):
    videos_per_year = 50
    video_ids = search_videos("migrationspolitik", f"{year}-01-01T00:00:00Z", f"{year}-12-31T23:59:59Z", max_results=videos_per_year)
    for video_id in video_ids:
        video_details = get_video_details(video_id)
        if video_details:
            title, comments_enabled = video_details
            if comments_enabled:
                videos_by_year[str(year)].append(video_id)
    sleep(1)

print("Writing video IDs to a text file...")

timestamp = datetime.now().strftime('%Y%m%d-%H%M')
output_file = f"out/videolist-{timestamp}.txt"

with open(output_file, "w") as file:
    for year, video_ids in videos_by_year.items():
        file.write(f"# {year}\n")
        file.write("\n".join(video_ids))
        file.write("\n\n")

print(f"Done! Saved as: '{output_file}'.")