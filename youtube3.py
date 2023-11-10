import argparse
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query, max_results):
   
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key

    # Create a YouTube API service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Perform the search
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    # Extract video information from the search response
    videos = []
    for item in search_response.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            video_info = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnails': item['snippet']['thumbnails'],
                'channelTitle': item['snippet']['channelTitle'],
                'publishTime': item['snippet']['publishTime']
            }
            videos.append(video_info)

    return videos

if __name__ == '__main__':
    # Check for command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python youtube.py <query> <max_results>")
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2])

    # Run the YouTube search and get videos
    videos = youtube_search(query, max_results)

    # Print the list of videos
    print(videos)
