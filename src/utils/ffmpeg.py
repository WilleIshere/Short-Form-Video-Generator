import os
import shutil
import zipfile
import requests
import tempfile
from tqdm import tqdm
import urllib.request
from .logger import info, warning, error, success, debug

def check_ffmpeg() -> str:
    ffmpeg_exe = "ffmpeg.exe"
    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg_bin")
    ffmpeg_path = os.path.join(ffmpeg_dir, ffmpeg_exe)

    if os.path.isfile(ffmpeg_path):
        print(f"[INFO] ffmpeg already exists at: {ffmpeg_path}")
        return ffmpeg_path

    def human_readable_size(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def download_with_progress(url, filename):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                info(f"Download size: {human_readable_size(total_size)}")
                chunk_size = 1024 * 1024
                with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading ffmpeg") as pbar:
                    with open(filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                info(f"Download finished: {filename}")
        except ImportError:
            info("'requests' module not found, using urllib for download.")
            with urllib.request.urlopen(url) as response:
                total_size = int(response.getheader('Content-Length').strip())
                info(f"Download size: {human_readable_size(total_size)}")
            chunk_size = 1024 * 1024

            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading ffmpeg") as pbar:
                with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        out_file.write(chunk)
                        pbar.update(len(chunk))
            info(f"Download finished: {filename}")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "ffmpeg.zip")
        info(f"Created temporary directory: {tmpdir}")
        info(f"Downloading ffmpeg from: {url}")
        download_with_progress(url, zip_path)
        info(f"ffmpeg zip downloaded to: {zip_path}")
        info(f"Extracting ffmpeg zip...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
        info(f"Extraction complete. Searching for {ffmpeg_exe}...")

        for root, dirs, files in os.walk(tmpdir):
            debug(f"Scanning directory: {root}")
            if ffmpeg_exe in files:
                extracted_ffmpeg_path = os.path.join(root, ffmpeg_exe)
                info(f"Located ffmpeg.exe at: {extracted_ffmpeg_path}")
                os.makedirs(ffmpeg_dir, exist_ok=True)
                info(f"Copying ffmpeg.exe to: {ffmpeg_path}")
                shutil.copy2(extracted_ffmpeg_path, ffmpeg_path)
                success(f"ffmpeg.exe copied successfully to: {ffmpeg_path}")
                break
        else:
            error("ffmpeg.exe not found in the downloaded archive.")
            raise FileNotFoundError("ffmpeg.exe not found in the downloaded archive.")

    success(f"ffmpeg is ready at: {ffmpeg_path}")
    return ffmpeg_path
