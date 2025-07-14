#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import requests
import sys

def download_file(url, dest_path):
    print(f"⬇️ Downloading {url}")
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print(f"❌ Failed to download {url}, status code {response.status_code}")
        sys.exit(1)
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print(f"✅ Saved to {dest_path}")

def generate_video(image_path, audio_path, output_path):
    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    print(f"\nRunning ffmpeg:\n{' '.join(cmd)}\n")
    subprocess.run(cmd, check=True)
    print(f"✅ Video saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate video from image and audio on S3")
    parser.add_argument("--artist", required=True, help="Artist name")
    parser.add_argument("--track", required=True, help="Track name")
    args = parser.parse_args()

    base_url = f"https://socialdbndata.s3.us-east-1.amazonaws.com/{args.artist}/{args.track}"

    # Local filenames
    image_path = Path(f"{args.track}_albumart.png")
    audio_path = Path(f"{args.track}_snippet.wav")
    output_path = Path(f"{args.track}.mp4")

    # Download files
    download_file(f"{base_url}/albumart.png", image_path)
    download_file(f"{base_url}/snippet.wav", audio_path)

    # Generate video
    generate_video(image_path, audio_path, output_path)

    # Cleanup
    for f in [image_path, audio_path]:
        try:
            f.unlink()
            print(f"🧹 Deleted temporary file: {f}")
        except Exception as e:
            print(f"⚠️ Could not delete {f}: {e}")

if __name__ == "__main__":
    main()
