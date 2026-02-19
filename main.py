from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import re

app = FastAPI()

# 🔐 CORS (Replace with your real frontend domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://allorapdf.com/i"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Request Model
class DownloadRequest(BaseModel):
    url: str

# 🔍 URL Validator (Only Instagram public links)
def is_valid_instagram_url(url: str):
    pattern = r"^(https?://)?(www\.)?instagram\.com/.+"
    return re.match(pattern, url)

@app.get("/")
def home():
    return {"status": "Backend Running Successfully"}

@app.post("/download")
async def download_instagram(request: DownloadRequest):

    if not is_valid_instagram_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid Instagram URL")

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "media_url": info.get("url")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to fetch media")
