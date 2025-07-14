#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import sys

def generate_video(image_path, audio_path, output_path):
    cmd = [
        "ffmpeg",
        "-y",              # overwrite output
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
    parser = argparse.ArgumentParser(description="Generate video from image and audio")
    parser.add_argument("--image", required=True, help="Path to image file (jpg/png)")
    parser.add_argument("--audio", required=True, help="Path to audio file (mp3/wav)")
    args = parser.parse_args()

    image_path = Path(args.image).resolve()
    audio_path = Path(args.audio).resolve()

    if not image_path.exists():
        print(f"❌ Image file does not exist: {image_path}")
        sys.exit(1)
    if not audio_path.exists():
        print(f"❌ Audio file does not exist: {audio_path}")
        sys.exit(1)

    # Build output path in same directory as the image
    output_dir = image_path.parent
    output_name = f"{image_path.stem}_{audio_path.stem}.mp4"
    output_path = output_dir / output_name

    generate_video(image_path, audio_path, output_path)

if __name__ == "__main__":
    main()
