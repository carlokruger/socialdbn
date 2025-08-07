#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import requests
import sys

from upload_s3 import upload_to_s3  # ✅ Import from new module


def download_file(url, dest_path):
    print(f"⬇️ Downloading {url}")
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print(f"❌ Failed to download {url}, status code {response.status_code}")
        sys.exit(1)
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
