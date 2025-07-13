# socialdbn

## Overview

**socialdbn** is a Python-based suite of CLI applications that automates the process of preparing, previewing, and posting new music track announcements to social media platforms.

It is designed to support artists and producers by streamlining the workflow from audio and artwork assets to multi-platform promotion, handling both pre-release hype and release announcements.

---

## Features

### 📀 1. Generate promotional video

* Inputs: `artist_name` and `track_name`.
* Looks up a picture (artwork) and an audio file in an S3 bucket matching the artist and track.
* Creates a video combining the image as the visual and the audio as the soundtrack.
* Saves the generated video back to the same S3 location.

### 📝 2. Create and confirm social media preview

* Given the `artist_name`, `track_name`, and a text file in the same S3 bucket:

  * Generates an HTML preview page displaying:

    * Artist name
    * Track name
    * Artwork
    * Generated video
    * Audio file
    * Text content (from the text file)
* Asks for user confirmation.
* Upon approval, generates a JSON file containing:

  * Artist & track info
  * URLs to artwork, audio, video in S3
  * The promotional text content.

### 🚀 3. Pre-release social media posting

* Takes the generated JSON file and creates a post via API calls.
* Initially supports Instagram.
* Designed for easy extension to platforms like X (Twitter), Facebook, Mastodon, Bluesky, YouTube.

### 🎧 4. Release announcement posting

* After the track is live on streaming platforms, run another CLI tool:

  * Inputs: `artist_name`, `track_name`, Spotify URL, Apple Music URL, Beatport URL.
  * Creates a new post announcing the release on the configured social media platforms.

---

## Workflow

```
[S3 bucket with artwork + audio + text]
           |
     [Step 1: generate video]
           |
     [Step 2: generate HTML preview]
           |
     [Review & confirm]
           |
     [Generates JSON metadata]
           |
[Step 3: post pre-release to social media]
           |
     [Track released on Spotify / Apple / Beatport]
           |
[Step 4: post release announcement to social media]
```

---

## Tech Stack

* 🐍 **Python 3.10+**
* ☁️ **AWS S3** (for storage of assets)
* 🖥 **ffmpeg** (for generating videos)
* 📜 **Jinja2** (for HTML preview templating)
* 🌐 **Requests / HTTP clients** (for API integration with social media platforms)
* 🚀 **Boto3** (for S3 operations)

---

## Future Enhancements

* Extend social media support to:

  * X (Twitter)
  * Facebook
  * Mastodon
  * Bluesky
  * YouTube
* CLI improvements:

  * `dry-run` mode to show what would be posted
  * More robust confirmation / rollback
* Webhook or event-driven triggers to automate end-to-end flow.

---

## Getting Started

```bash
git clone https://github.com/yourusername/socialdbn.git
cd socialdbn
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Contributing

Contributions, bug reports, and feature requests are welcome!
Please open an issue or submit a pull request.

---

## License

MIT License

---

## Author

Carlo Kruger


