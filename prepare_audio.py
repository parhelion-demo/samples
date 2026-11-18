"""Copy the sample MP3s into the site's audio/ folder with all metadata removed.

Usage: python prepare_audio.py <folder with the mp3s> <site folder>

ID3 tags can hold artist names, titles, encoder settings and file paths.
ffmpeg copies the audio stream unchanged (no re-encoding) and drops every tag.
Requires ffmpeg on the PATH.
"""
import subprocess
import sys
from pathlib import Path

src, site = Path(sys.argv[1]), Path(sys.argv[2])
out = site / "audio"
out.mkdir(parents=True, exist_ok=True)

files = sorted(src.glob("*.mp3"))
if not files:
    sys.exit(f"No .mp3 files in {src}")
for f in files:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-map", "0:a", "-map_metadata", "-1",
                    "-c", "copy", "-id3v2_version", "0", str(out / f.name)], check=True)
    print(f.name)
print(f"Wrote {len(files)} files to {out}")
