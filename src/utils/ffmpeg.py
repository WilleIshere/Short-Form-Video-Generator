import os
import shutil
import zipfile
import requests
import tempfile
from tqdm import tqdm
import urllib.request
from sys import platform
from src.utils.loggr import info, warning, error, success, debug

WINDOWS_FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
LINUX_FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"

def check_ffmpeg() -> str:
    # Set up platform-specific names and paths
    if platform == 'win32':
        ffmpeg_exe = "ffmpeg.exe"
        op = 'w'
    else:
        ffmpeg_exe = "ffmpeg"
        op = 'l'
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

    import tarfile

    if op == 'w':
        url = WINDOWS_FFMPEG_URL
        archive_name = "ffmpeg.zip"
    else:
        url = LINUX_FFMPEG_URL
        archive_name = "ffmpeg.tar.xz"

    with tempfile.TemporaryDirectory() as tmpdir:
        archive_path = os.path.join(tmpdir, archive_name)
        info(f"Created temporary directory: {tmpdir}")
        info(f"Downloading ffmpeg from: {url}")
        download_with_progress(url, archive_path)
        info(f"ffmpeg archive downloaded to: {archive_path}")
        info(f"Extracting ffmpeg archive...")

        if op == 'w':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
        else:
            with tarfile.open(archive_path, 'r:xz') as tar_ref:
                tar_ref.extractall(tmpdir)
            # On Linux, ffmpeg binary is usually named 'ffmpeg' (not 'ffmpeg.exe')
            ffmpeg_exe = "ffmpeg"

        info(f"Extraction complete. Searching for {ffmpeg_exe}...")

        found = False
        for root, _, files in os.walk(tmpdir):
            debug(f"Scanning directory: {root}")
            if ffmpeg_exe in files:
                extracted_ffmpeg_path = os.path.join(root, ffmpeg_exe)
                info(f"Located {ffmpeg_exe} at: {extracted_ffmpeg_path}")
                os.makedirs(ffmpeg_dir, exist_ok=True)
                info(f"Copying {ffmpeg_exe} to: {ffmpeg_path}")
                shutil.copy2(extracted_ffmpeg_path, ffmpeg_path)
                # Ensure executable permissions on Linux
                if op == 'l':
                    os.chmod(ffmpeg_path, 0o755)
                success(f"{ffmpeg_exe} copied successfully to: {ffmpeg_path}")
                found = True
                break
        if not found:
            error(f"{ffmpeg_exe} not found in the downloaded archive.")
            raise FileNotFoundError(f"{ffmpeg_exe} not found in the downloaded archive.")

    success(f"ffmpeg is ready at: {ffmpeg_path}")
    return ffmpeg_path
