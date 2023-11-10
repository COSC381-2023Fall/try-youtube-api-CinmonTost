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
        for page_number in range(options.starting_page, options.ending_page + 1):
            # Make a request for each page in the specified range
            search_response = youtube.search().list(
                q=options.q,
                part='id,snippet',
                maxResults=options.max_results,
                pageToken=None if page_number == 1 else options.page_token
            ).execute()

            # Process the results for the current page
            page_results = process_search_results(search_response)
            videos.extend(page_results)

            # Save the nextPageToken for the next iteration
            options.page_token = search_response.get('nextPageToken')

            # Break if there are no more pages
            if 'nextPageToken' not in search_response:
                break

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
    parser.add_argument('--max-results', help='Max results per page', default=25)
    parser.add_argument('--starting-page', help='Starting page number', type=int, default=1)
    parser.add_argument('--ending-page', help='Ending page number', type=int, default=1)
    parser.add_argument('--page-token', help='Page token for pagination', default=None)
    args = parser.parse_args()

    try:
        video_results = youtube_search(args)
        print(f"Results for Pages {args.starting_page} to {args.ending_page}:\n")
        print(video_results)

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
