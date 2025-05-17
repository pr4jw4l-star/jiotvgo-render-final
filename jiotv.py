import argparse
import json
import requests

def get_headers(config):
    return {
        "User-Agent": "JioTV",
        "appid": config.get("appid", "tv.jio.jioplay.tv"),
        "x-device-id": config["device_id"],
        "x-platform": "Android",
        "x-unique-id": config["unique_id"],
        "Authorization": f"Bearer {config['auth_token']}"
    }

def get_channels(config):
    url = "https://jiotvapi.cdn.jio.com/apis/v1.3/getchannelhome"
    headers = get_headers(config)
    params = {"langId": "6", "os": "android"}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        data = res.json()
        channels = []
        for section in data.get("result", []):
            for ch in section.get("channelList", []):
                channels.append({
                    "id": ch["channel_id"],
                    "name": ch["channel_name"]
                })
        return channels
    return []

def build_stream_url(channel_id, config):
    return (
        f"https://jiotv.live.cdn.jio.com/{channel_id}/{channel_id}_"
        f"{config.get('resolution', '720')}.m3u8"
    )

def generate_playlist(config_path, output_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    channels = get_channels(config)

    with open(output_path, "w") as f:
        f.write("#EXTM3U
")
        for ch in channels:
            stream_url = build_stream_url(ch["id"], config)
            f.write(f"#EXTINF:-1,{ch['name']}
{stream_url}
")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    generate_playlist(args.config, args.output)
