# This python Script does not work for large playlists !

# Needed for to avoid errors
from __future__ import unicode_literals
# Youtube Download Libary
import youtube_dl

# Sources
#    https://github.com/rg3/youtube-dl/blob/master/README.md#readme

ydl_opts = {
    'format': 'bestaudio/worst', # no good audio quality is needed
    'ignoreerrors': True,
    'outtmpl': '%(playlist_title)s-%(title)s.%(ext)s', # name to download to
    'postprocessors': [{
        'key': 'FFmpegExtractAudio', # save only audio
        'preferredcodec': 'wav', # save as wav
        'postprocessor_args': ['ar 16000'] # sample rate = 16000
    }]
}

# Downlaod embedded in Python
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=NtEcnowF0qM&t=1s'])
