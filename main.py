from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import json
import subprocess

app = FastAPI()

with open("jtv_config.json", "r") as f:
    config = json.load(f)

USERNAME = "Prajwal_07"
PASSWORD = "prajwal@521112"

@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "JioTV M3U Server with EPG is running."

@app.get("/playlist.m3u", response_class=PlainTextResponse)
def get_playlist(request: Request):
    user = request.query_params.get("u")
    pw = request.query_params.get("p")

    if user != USERNAME or pw != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = subprocess.run(
        ["python3", "jiotv.py", "--config", "jtv_config.json", "--output", "playlist.m3u"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail="Playlist generation failed.")

    with open("playlist.m3u", "r") as f:
        return f.read()

@app.get("/epg.xml", response_class=PlainTextResponse)
def get_epg():
    # This returns a very basic EPG XML (normally you would fetch it from an external API)
    return '''<?xml version="1.0" encoding="UTF-8"?>
<tv>
  <channel id="ColorsHD"><display-name>Colors HD</display-name></channel>
  <channel id="SonyTen1"><display-name>Sony Ten 1</display-name></channel>
  <channel id="StarPlus"><display-name>Star Plus</display-name></channel>
  <programme start="20250517080000 +0000" stop="20250517090000 +0000" channel="ColorsHD">
    <title>Shakti</title>
  </programme>
  <programme start="20250517090000 +0000" stop="20250517100000 +0000" channel="SonyTen1">
    <title>WWE Raw</title>
  </programme>
</tv>'''
