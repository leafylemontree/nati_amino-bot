import youtube_dl
import subprocess
import sys

def download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'media/youtube/download.%(ext)s', 
        'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
        'extract-audio': True,
        }
    
    proc = subprocess.run(['rm', '-r', 'media/youtube'])
    proc = subprocess.run(['mkdir', 'media/youtube/'])

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url)
        duration = info['duration']

    proc = subprocess.run(['ffmpeg', '-i', 'media/youtube/download.mp3', '-acodec', 'pcm_u8', '-ar', '22050', '-segment_time', '00:03:00', '-f', 'segment', 'media/youtube/download%03d.wav'])
    proc = subprocess.run(['ls', 'media/youtube'])

    with open('media/youtube/list.bin', 'w+') as f:
        f.write(str(duration // 180))

download(sys.argv[1])
