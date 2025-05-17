import json
import argparse

def generate_playlist(config_path, output_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    channels = [
        {"channel_id": "101", "channel_name": "Colors HD"},
        {"channel_id": "102", "channel_name": "Sony Ten 1"},
        {"channel_id": "103", "channel_name": "Star Plus"}
    ]

    with open(output_path, "w") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            stream_url = f"https://jiotv.live.cdn.jio.com/{ch['channel_id']}/{ch['channel_id']}_index.m3u8"
            f.write(f"#EXTINF:-1,{ch['channel_name']}\n{stream_url}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    generate_playlist(args.config, args.output)
