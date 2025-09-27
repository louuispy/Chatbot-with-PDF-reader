import re
from youtube_transcript_api import YouTubeTranscriptApi

def transcript_video(url_video):
    ytt_api = YouTubeTranscriptApi()
    url = re.search(r"(?<=youtu\.be/)[^?]+", url_video).group(0)
    transcription = ytt_api.fetch(url, languages=['pt'], preserve_formatting=True)

    document = ''

    for doc in transcription:
        document += doc.text

    return document

