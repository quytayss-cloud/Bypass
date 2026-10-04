from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp
import os
from ai_bypass import ai_engine

app = FastAPI(title="AI Multi-Platform Downloader - 4K & Hi-Res")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=DOWNLOAD_DIR), name="static")

class DownloadRequest(BaseModel):
    query: str
    quality: str = "1080p"

@app.get("/", response_class=HTMLResponse)
def read_root():
    return open("templates/index.html", "r", encoding="utf-8").read()

@app.post("/api/download")
def download_media(data: DownloadRequest):
    query = data.query.strip()
    quality = data.quality.lower()

    if not query:
        raise HTTPException(status_code=400, detail="Vui lòng nhập link hoặc tên nội dung!")

    if not query.startswith("http"):
        search_target = f"ytsearch1:{query}"
    else:
        search_target = query

    base_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'restrictfilenames': True,
    }

    if quality == "4k":
        base_opts.update({
            'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]/best',
            'merge_output_format': 'mp4',
        })
    elif quality == "2k":
        base_opts.update({
            'format': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]/best',
            'merge_output_format': 'mp4',
        })
    elif quality == "1080p":
        base_opts.update({
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
            'merge_output_format': 'mp4',
        })
    elif quality == "720p":
        base_opts.update({
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
            'merge_output_format': 'mp4',
        })
    elif quality == "alac":
        base_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'}],
        })
    elif quality == "flac":
        base_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'flac'}],
        })
    elif quality == "mp3_320":
        base_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
        })
    else:
        base_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        })

    final_opts = ai_engine.analyze_and_optimize_options(search_target, base_opts)

    try:
        with yt_dlp.YoutubeDL(final_opts) as ydl:
            info = ydl.extract_info(search_target, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            filename = ydl.prepare_filename(info)

            if quality == "alac" and not filename.endswith(".m4a"):
                filename = os.path.splitext(filename)[0] + ".m4a"
            elif quality == "flac" and not filename.endswith(".flac"):
                filename = os.path.splitext(filename)[0] + ".flac"
            elif quality in ["mp3_320", "mp3_192"] and not filename.endswith(".mp3"):
                filename = os.path.splitext(filename)[0] + ".mp3"

            basename = os.path.basename(filename)
            return {
                "status": "success",
                "title": info.get('title', 'Downloaded Media'),
                "download_url": f"/static/{basename}",
                "filename": basename
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tải xuống: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
