from __future__ import unicode_literals
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/worst',
    'ignoreerrors': True,
    'outtmpl': '%(playlist_title)s-%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'postprocessor_args': ['ar 16000']
    }]
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=NtEcnowF0qM&t=1s'])
    #'postprocessor_args': ['ar 16000']
