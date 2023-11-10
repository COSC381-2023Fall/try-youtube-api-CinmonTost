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

    videos = []

    try:
        # Initial search
        search_response = youtube.search().list(
            q=options.q,
            part='id,snippet',
            maxResults=options.max_results
        ).execute()

        # Process the first page of results
        videos.extend(process_search_results(search_response))

        # Check for additional pages
        while 'nextPageToken' in search_response:
            next_page_token = search_response['nextPageToken']

            # Retrieve the next page of results
            search_response = youtube.search().list(
                q=options.q,
                part='id,snippet',
                maxResults=options.max_results,
                pageToken=next_page_token
            ).execute()

            # Process the next page of results
            videos.extend(process_search_results(search_response))

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    return videos

def process_search_results(response):
    videos = []

    # Add each video result to the videos list
    for search_result in response.get('items', []):
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
        # Split the results into two lists for the first and second pages
        first_page_results = video_results[:args.max_results]
        second_page_results = video_results[args.max_results:]

        print("First Page Results:")
        print(first_page_results)

        print("\nSecond Page Results:")
        print(second_page_results)

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
