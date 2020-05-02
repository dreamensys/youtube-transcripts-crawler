# the Google API client needs to be installed, follow https://pypi.org/project/google-api-python-client/
from apiclient.discovery import build

class YoutubeAPIClient:
    def __init__(self):
        self.api_key = "YOUR API KEY"
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_videos_list(self, ids):
        results = []
        request = self.youtube.videos().list(
                    part="snippet",
                    id= ids)
        response = request.execute()
        results += response['items']
        return results

    def get_playlist_channels(self, playlist_id):
        items = []
        request = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=10)
        response = request.execute()
        items += response['items']
        video_ids = ""
        for item in items:
            video_ids += item['snippet']['resourceId']['videoId'] + ","

        x = self.get_videos_list(video_ids)
        return x

    def get_channel_videos(self, channel_id):
    
        # get Uploads playlist id
        res = self.youtube.channels().list(id=channel_id, 
                                    part='contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        videos = []
        next_page_token = None
        
        while 1:
            res = self.youtube.playlistItems().list(playlistId=playlist_id, 
                                            part='snippet', 
                                            maxResults=5,
                                            pageToken=next_page_token).execute()
            videos += res['items']
            next_page_token = res.get('nextPageToken')
            
            if next_page_token is None:
                break
        
        return videos