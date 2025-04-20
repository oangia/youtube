import yt_dlp
import webvtt

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
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'vtt',
        'outtmpl': 'transcript.%(ext)s',
        'quiet': True,
    }
    
    # Download subtitles
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return vtt_to_text("transcript.en.vtt")

def vtt_to_text(filepath):
    text = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("WEBVTT") or "-->" in line or line.isdigit():
                continue
            text.append(line)
    return "\r\n".join(text)
