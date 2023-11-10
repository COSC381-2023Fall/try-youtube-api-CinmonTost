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

        # Process the specified page of results
        specified_page_results = process_search_results(search_response, options.page_number)
        videos.extend(specified_page_results)

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    return videos

def process_search_results(response, page_number):
    videos = []

    # Calculate the starting index for the specified page
    start_index = (page_number - 1) * response['pageInfo']['resultsPerPage']

    # Add each video result to the videos list for the specified page
    for i, search_result in enumerate(response.get('items', [])):
        if search_result['id']['kind'] == 'youtube#video':
            video_info = {
                'title': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId']
            }
            # Check if the current video is within the specified page
            if start_index <= i < start_index + response['pageInfo']['resultsPerPage']:
                videos.append(video_info)

    return videos


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results per page', default=25)
    parser.add_argument('--page-number', help='Page number', type=int, default=1)
    args = parser.parse_args()

    try:
        video_results = youtube_search(args)
        print(f"Results for Page {args.page_number}:\n")
        print(video_results)

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
