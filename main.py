from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
ytt = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=os.environ.get("fzytktuv"),
        proxy_password=os.environ.get("obm06om4uar4"),
    )
)
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
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.list(video_id)


        transcript = None
        for t in transcript_list:
            if t.language_code == lang:
                transcript = t
                break


        if transcript is None:
            for t in transcript_list:
                if t.language_code == "en":
                    transcript = t
                    break


        if transcript is None:
            transcript = next(iter(ytt.list(video_id)))

        data = transcript.fetch()

        return {
            "video_id": video_id,
            "language": transcript.language_code,
            "subtitles": [
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration
                }
                for snippet in data
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
