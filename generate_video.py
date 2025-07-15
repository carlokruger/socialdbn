#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import requests
import sys
import boto3
from botocore.exceptions import BotoCoreError, ClientError


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


def sanitize_text_for_ffmpeg(text):
    # Escape minimal set needed for ffmpeg drawtext
    return (
        text.replace(":", "\\:")
            .replace("'", "\\'")
    )


def generate_video(image_path, audio_path, lines, output_path):
    filter_parts = []
    base_y = int(1080 * 0.6)  # start around 60% height
    line_spacing = 80

    for i, line in enumerate(lines):
        y_pos = base_y + i * line_spacing
        clean_line = sanitize_text_for_ffmpeg(line.strip())
        drawtext = (
            f"drawtext=text='{clean_line}':"
            f"fontfile=/Library/Fonts/Arial.ttf:"
            f"x=(w-text_w)/2:y={y_pos}:"
            f"fontcolor=black:fontsize=60:"
            f"box=1:boxcolor=white@0.5:boxborderw=50"
        )
        filter_parts.append(drawtext)

    filter_str = ",".join(filter_parts)

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-vf", filter_str,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]

    print("\n*** FFMPEG COMMAND ***")
    print(' '.join(cmd))
    print("**********************\n")

    subprocess.run(cmd, check=True)
    print(f"✅ Video saved to: {output_path}")


def upload_to_s3(local_file, bucket, s3_key):
    print(f"⬆️ Uploading {local_file} to s3://{bucket}/{s3_key}")
    s3 = boto3.client("s3")
    try:
        s3.upload_file(str(local_file), bucket, s3_key)
        print(f"✅ Upload confirmed: s3://{bucket}/{s3_key}")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"❌ Upload failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate video with overlay text from S3 and upload final to S3")
    parser.add_argument("--artist", required=True, help="Artist name")
    parser.add_argument("--track", required=True, help="Track name")
    args = parser.parse_args()

    base_url = f"https://socialdbndata.s3.us-east-1.amazonaws.com/{args.artist}/{args.track}"

    image_path = Path(f"{args.track}_albumart.png")
    audio_path = Path(f"{args.track}_snippet.wav")
    blurb_path = Path(f"{args.track}_blurb.txt")
    hashtags_path = Path(f"{args.track}_hashtags.txt")
    output_path = Path(f"{args.artist} - {args.track}.mp4")

    download_file(f"{base_url}/albumart.png", image_path)
    download_file(f"{base_url}/snippet.wav", audio_path)
    download_file(f"{base_url}/blurb.txt", blurb_path)
    download_file(f"{base_url}/hashtags.txt", hashtags_path)

    blurb_lines = blurb_path.read_text(encoding="utf-8").strip().splitlines()
    hashtags_line = hashtags_path.read_text(encoding="utf-8").strip()
    all_lines = blurb_lines + [hashtags_line]

    generate_video(image_path, audio_path, all_lines, output_path)

    for f in [image_path, audio_path, blurb_path, hashtags_path]:
        try:
            f.unlink()
            print(f"🧹 Deleted temporary file: {f}")
        except Exception as e:
            print(f"⚠️ Could not delete {f}: {e}")

    # Upload final video to S3
    bucket_name = "socialdbndata"
    s3_key = f"{args.artist}/{args.track}/{output_path.name}"
    upload_success = upload_to_s3(output_path, bucket_name, s3_key)

    if upload_success:
        try:
            output_path.unlink()
            print(f"🧹 Deleted local video after successful upload: {output_path}")
        except Exception as e:
            print(f"⚠️ Could not delete local video: {e}")
    else:
        print(f"⚠️ Keeping local copy since upload failed: {output_path}")


if __name__ == "__main__":
    main()