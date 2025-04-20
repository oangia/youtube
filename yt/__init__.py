import yt_dlp
import webvtt
import os

def download_channel(channel):
    channel_url = 'https://www.youtube.com/@' + channel +'/videos'
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    
    return info

def download_audio(id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=" + id])

def download_transcript(id):
    url = 'https://www.youtube.com/watch?v=' + id

    # Set up yt_dlp options
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,         # download manual subtitles if available
        'writeautomaticsub': True,      # fallback to auto subtitles if manual not available
        'subtitleslangs': ['en'],       # target English only
        'subtitlesformat': 'vtt',
        'outtmpl': 'transcript.%(ext)s',
        'quiet': True,
    }
    
    # Download subtitles
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return vtt_to_text("transcript.en.vtt")

def vtt_to_text(filepath):
    transcript = []
    for caption in webvtt.read(filepath):
        transcript.append(caption.text)

    for i in range(len(transcript)) - 1:
        if transcript[i + 1] == transcript[i]:
            del transcript[i + 1]
    return '\n'.join(transcript)
