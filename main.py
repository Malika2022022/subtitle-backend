import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/subtitles/{video_id}")
async def get_subtitles(video_id: str, lang: str = "en"):
    try:
        response = requests.get(
            "https://www.searchapi.io/api/v1/search",
            params={
                "engine": "youtube_transcripts",
                "video_id": video_id,
                "lang": lang,
                "api_key": os.environ.get("SEARCHAPI_KEY"),
            }
        )
        data = response.json()
        if "transcripts" not in data:
            raise HTTPException(status_code=404, detail="No transcripts found")
        return {
            "video_id": video_id,
            "language": lang,
            "subtitles": data["transcripts"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
