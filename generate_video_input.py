#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
from PIL import Image
import sys
import shutil

# Set up supported resolutions and template filenames
RESOLUTIONS = {
    "landscape": "1920x1080.png",
    "square": "1080x1080.png",
    "portrait": "1080x1350.png",
    "reel": "720x1280.png"
}

TEMPLATES_DIR = Path("templates")
DATA_DIR = Path("data")
GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)

def overlay_artwork_on_template(template_path: Path, artwork_path: Path, output_path: Path, margin: int = 100):
    """
    Overlays the artwork onto the center of the template and saves it to output_path.
    """
    print(f"🎨 Overlaying artwork onto {template_path.name}")
    try:
        template = Image.open(template_path).convert("RGBA")
        artwork = Image.open(artwork_path).convert("RGBA")
    except Exception as e:
        print(f"❌ Failed to open image: {e}")
        sys.exit(1)

    max_width = template.width - 2 * margin
    max_height = template.height - 2 * margin
    artwork.thumbnail((max_width, max_height), Image.LANCZOS)

    x = (template.width - artwork.width) // 2
    y = (template.height - artwork.height) // 2

    template.paste(artwork, (x, y), artwork)
    template.save(output_path, format="PNG")
    print(f"✅ Saved overlay image: {output_path}")

def locate_artwork(artist: str, track: str) -> Path:
    path = DATA_DIR / artist / track / "artwork.png"
    if not path.exists():
        print(f"❌ Could not find artwork at {path}")
        sys.exit(1)
    return path

def call_generate_video_script(artist: str, track: str, base_image_path: Path, label: str):
    """
    Calls generate_video.py with appropriate arguments and image input.
    """
    video_script = Path("generate_video.py")
    if not video_script.exists():
        print("❌ generate_video.py not found!")
        sys.exit(1)

    print(f"🎬 Calling generate_video.py for {label} resolution...")

    cmd = [
        "python3", str(video_script),
        "--artist", artist,
        "--track", track,
        "--image", str(base_image_path),
        "--label", label  # optional: can help suffix or tag output
    ]
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="Generate videos for multiple resolutions")
    parser.add_argument("--artist", required=True, help="Artist name")
    parser.add_argument("--track", required=True, help="Track name")
    args = parser.parse_args()

    artwork_path = locate_artwork(args.artist, args.track)

    for label, template_name in RESOLUTIONS.items():
        template_path = TEMPLATES_DIR / template_name
        if not template_path.exists():
            print(f"⚠️ Template not found: {template_path}")
            continue

        output_image = GENERATED_DIR / f"{args.artist}_{args.track}_{label}.png"
        overlay_artwork_on_template(template_path, artwork_path, output_image)

        # Call video generation
        call_generate_video_script(args.artist, args.track, output_image, label)

        # Optional: delete composite image after use
        try:
            output_image.unlink()
            print(f"🧹 Removed temporary image: {output_image}")
        except Exception as e:
            print(f"⚠️ Could not delete temp image: {e}")

if __name__ == "__main__":
    main()
