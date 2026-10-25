"""Download the Taobao display-ad click dataset used in this course.

Source: "Ad Display/Click Data on Taobao.com" by Alibaba, https://tianchi.aliyun.com/dataset/56,
licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/).
The files come from a copy on Hugging Face that needs no account. The download is pinned to a
fixed revision of that copy and checked against known SHA-256 checksums, so everyone gets
exactly the same files.

Usage: python download_data.py
"""

import hashlib
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = "https://huggingface.co/datasets/Angrybird12/ad-display_click-data_taobao.com"
REVISION = "29af49a45b296680c66304a2a1c597cae3eb81f7"
FILES = {
    "raw_sample.csv": "aad792d63b81b5b7788f91e35364975b83ce3fdb923009fdfb6f798545d2b93d",
    "ad_feature.csv": "358a298178a6286196b82fe151024c63f4b081cf7685f1ebf8ff4da776e3c745",
    "user_profile.csv": "63355e02e302768d79db658e0f25498f368b4b5e037318bc67973835380a0532",
}
DATA_DIR = Path(__file__).resolve().parent / "data" / "taobao"
CHUNK = 1 << 20


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, target: Path) -> None:
    partial = target.with_suffix(target.suffix + ".part")
    with urllib.request.urlopen(url) as response, partial.open("wb") as out:
        total = int(response.headers.get("Content-Length", 0))
        done = 0
        while chunk := response.read(CHUNK):
            out.write(chunk)
            done += len(chunk)
            if total:
                print(f"\r  {target.name}: {done / total:6.1%} of {total / 1e6:,.0f} MB", end="", flush=True)
    print()
    partial.replace(target)


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, expected in FILES.items():
        target = DATA_DIR / name
        if target.exists() and sha256(target) == expected:
            print(f"  {name}: already downloaded")
            continue
        try:
            download(f"{REPO}/resolve/{REVISION}/{name}", target)
        except urllib.error.URLError as error:
            if isinstance(error.reason, ssl.SSLCertVerificationError):
                print(
                    "SSL certificates are not set up for this Python. On macOS with the python.org "
                    "installer, run 'Install Certificates.command' from your Python folder and retry.",
                    file=sys.stderr,
                )
            raise
        if sha256(target) != expected:
            target.unlink()
            print(f"  {name}: checksum mismatch, so the file was removed. Please run the script again.", file=sys.stderr)
            return 1
    print(f"All files are in {DATA_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
