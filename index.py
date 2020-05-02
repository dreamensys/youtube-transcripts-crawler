
from YoutubeScrapper import YoutubeScrapper
from FileHelper import FileHelper
from YoutubeAPIClient import YoutubeAPIClient
from Log import Log
import time

ys = YoutubeScrapper()
yc = YoutubeAPIClient()
fh = FileHelper()
lg = Log()

def scrappe_video(video_id, channel_id):
    lg.write_title('On channel: '+ channel_id +'. Inspecting ' + video_id + '...')
    file_name = video_id
    file_exists = fh.file_exists(file_name)

    if (not file_exists):
        lg.write_message('getting transcripts for ' + video_id)
        caption_info = ys.get_transcript_list_from_video_id(video_id)

        if (caption_info.is_success()):
            lg.write_message("creating file...")
            fh.create_cvs(caption_info.get_data(), file_name, ['time', 'text'])
            lg.write_message("File for "+ video_id + " was created!")
        else:
            lg.write_error('videoId: '+video_id + ', Description:' + caption_info.get_error_message())
    else:
        lg.write_message(file_name + " already processed!")

# Get channels info
playlist_id = "PLJx8aAjD-48-BjXrT-Ibp4QwxuT8bjxGD" #ChunkiLibraryTest
# playlist_id = "PLJx8aAjD-48-GiUdRzqH0LTQHTcO7JlO_" #ChunkiLibraryProd

channels = yc.get_playlist_channels(playlist_id)
for channel in channels:
    channel_id = channel['snippet']['channelId']
    # Get Videos from Channels
    videos = yc.get_channel_videos(channel_id)
    lg.write_title(str(len(videos)) + ' videos for channel ' + str(channel_id))
    for v in videos:
        video_id = v['snippet']['resourceId']['videoId']
        scrappe_video(video_id, str(channel_id))

#Disposing
ys.close_browser()
    











