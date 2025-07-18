# upload_s3.py

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from pathlib import Path

def upload_to_s3(local_file: Path, bucket: str, s3_key: str) -> bool:
    """
    Uploads a local file to an S3 bucket at the specified key.

    :param local_file: Path to the file to upload
    :param bucket: S3 bucket name
    :param s3_key: Destination key in the S3 bucket
    :return: True if upload succeeds, False otherwise
    """
    print(f"\n⬆️ Uploading {local_file} to s3://{bucket}/{s3_key}")
    s3 = boto3.client("s3")
    try:
        s3.upload_file(str(local_file), bucket, s3_key)
        print(f"✅ Upload confirmed: s3://{bucket}/{s3_key}")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"❌ Upload failed: {e}")
        return False


if __name__ == "__main__":
    # Example usage (for testing):
    from sys import argv
    if len(argv) != 4:
        print("Usage: python upload_s3.py <local_file> <bucket> <s3_key>")
    else:
        local = Path(argv[1])
        success = upload_to_s3(local, argv[2], argv[3])
        print("✅ Success" if success else "❌ Failure")
