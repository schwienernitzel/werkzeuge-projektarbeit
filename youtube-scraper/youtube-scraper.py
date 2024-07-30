# @author: Felix Patryjas - https://github.com/schwienernitzel
# @date: 25-06-2024
# @title: Python-Script to read the videos of 'youtube-finder' scrape their user comments
# @version: v3.3

import csv
import json
import re
import unicodedata
import sys
import os

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from time import sleep

api_key = os.getenv('APIKEY')

if not api_key:
    print("\033[91mERROR: No Google API-Key found in the current runtime! Aborting...\033[0m")
    sleep(2)
    sys.exit(1)

video_ids_file = '../youtube-finder/out/videolist-20240626-0849.txt'

def video_reader(file_path):
    video_data = []
    try:
        with open(file_path, 'r') as file:
            video_ids = file.readlines()
            for video_id in video_ids:
                video_id = video_id.strip()
                if video_id and not video_id.startswith('#'):
                    video_data.append({'video_id': video_id, 'video_title': 'Unknown Title'})
        print(f"Total videos to process: {len(video_data)}")
    except Exception as e:
        print(f"Error reading video IDs from file: {e}")
    return video_data

def get_video_title(api_key, video_id):
    try:
        url = f'https://www.googleapis.com/youtube/v3/videos?key={api_key}&part=snippet&id={video_id}'
        response = urlopen(url)
        json_data = json.loads(response.read())
        title = json_data['items'][0]['snippet']['title']
        return title
    except Exception as e:
        print(f"Error fetching title for video ID {video_id}: {e}")
        return 'Unknown Title'

def comment_scraper(api_key, data):
    sleep(1)
    print("Starting comment scraping...")
    total = len(data)
    current = 0
    total_comments = 0
    string_to_file = 'comment_id\treplycount\tlikecount\tdate\ttime\temojis\tcomment\n'

    for info in data:
        video_id = info['video_id']
        video_title = get_video_title(api_key, video_id)

        url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet,replies&videoId={video_id}&maxResults=100'
        raw_url = url
        nextPageToken = None
        comment_id = 1
        current += 1
        sleep(1)
        print(f"Scraping comments for Video {current}/{total} - Title: {video_title} - ID: {video_id}")

        while comment_id < 100000:
            try:
                response = urlopen(url)
                json_data = json.loads(response.read())

                if 'items' not in json_data:
                    print(f"No comments found for video ID: {video_id}")
                    break

                last_nextPageToken = nextPageToken
                for item in json_data['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comment = re.sub('[\s]+', ' ', comment)
                    date = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    time = re.sub('.*T(\d\d:\d\d):\d\dZ', r'\1', date)
                    date = re.sub('T.*', '', date)
                    likecount = item['snippet']['topLevelComment']['snippet']['likeCount']
                    replycount = item['snippet']['totalReplyCount']
                    emojis = re.sub('[^\u263a-\U0001f645 \U00010000-\U0010ffff]', '', comment)
                    emojis = re.sub(' ', '', emojis)
                    string_to_file += f"{comment_id}\t{replycount}\t{likecount}\t{date}\t{time}\t{emojis}\t{comment}\n"
                    comment_id += 1
                    total_comments += 1

                nextPageToken = json_data.get('nextPageToken')
                if not nextPageToken or nextPageToken == last_nextPageToken:
                    break

                url = raw_url + f'&pageToken={nextPageToken}'
            except HTTPError as e:
                print(f"HTTP Error: Could not fetch comments for video ID: {video_id} => {e.code} - {e.reason}")
                break
            except URLError as e:
                print(f"URL Error: Could not fetch comments for video ID: {video_id} => {e.reason}")
                break
            except Exception as e:
                print(f"Unknown Error: Could not fetch comments for video ID: {video_id} => {e}")
                break

    string_to_file = string_to_file.strip()
    with open('out/raw.csv', 'w') as writefile:
        writefile.write(string_to_file)
    print("Done! File saved as 'raw.csv'.")
    sleep(2)
    print(f"Comment scraping completed. Total raw comments: {total_comments}")

video_data = video_reader(video_ids_file)
comment_scraper(api_key, video_data)