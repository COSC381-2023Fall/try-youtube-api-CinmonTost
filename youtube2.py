#!/usr/bin/python

import argparse
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()

    videos = []

    # Add each video result to the videos list
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_info = {
                'title': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId']
            }
            videos.append(video_info)

    return videos


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()

    try:
        video_results = youtube_search(args)
        print(video_results)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
