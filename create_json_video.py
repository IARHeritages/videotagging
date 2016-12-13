from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import settings
import json
import click


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = settings.GOOGLE_APIKEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def _extract_video_info(item):
    """Extract youtube video information from snippet dict"""
    video_id = item['id']['videoId']
    video_url = 'https://www.youtube.com/watch?v=' + video_id
    oembed = '<iframe width="512" height="512" ' \
        'src="https://www.youtube.com/embed/{}" ' \
        'frameborder="0" allowfullscreen></iframe>'.format(video_id)
    return {'video_url': video_url, 'oembed': oembed}

@click.command()
@click.option('--query', default='roman empire britain', help="Your YOUTUBE query")
@click.option('--duration', default='short', help="It could be short or long")
@click.option('--published', default='2016-01-01T00:00:00Z', help="It should be a date YYYY-MM-DD")
@click.option('--region', default='GB', help="Use a Region Code")
@click.option('--max', default='50', help="It should be less than 50")
@click.option('--output', default='videos.json', help="Name of the output video")
def youtube_search(query, duration, published, region, max, output):
    """Search in youtube and save the results in videos.json file."""
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(q=query,
                                            part="id,snippet",
                                            maxResults=max,
                                            type="video",
                                            videoDuration=duration,
                                            publishedAfter=published,
                                            regionCode=region,
                                            ).execute()

    videos = []
    nextPageToken = search_response.get('nextPageToken', None)
    for search_result in search_response.get("items", []):
        tmp = search_result.copy()
        tmp.update(_extract_video_info(search_result))
        videos.append(tmp)

    while len(search_response.get('items', [])) > 0 and nextPageToken != None:
        search_response = youtube.search().list(q=query,
                                         part="id,snippet",
                                         maxResults=max,
                                         type="video",
                                         videoDuration=duration,
                                         publishedAfter=published,
                                         regionCode=region,
                                         pageToken=nextPageToken
                                         ).execute()
        nextPageToken = search_response.get('nextPageToken', None)
        for search_result in search_response.get("items", []):
            videos.append(search_result)

    with open(output, 'w') as file:
        file.write(json.dumps(videos))

if __name__ == "__main__":
  youtube_search()
