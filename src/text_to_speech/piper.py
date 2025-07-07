import os
import sys
import subprocess
import urllib.request
import tarfile
import zipfile
import shutil
import stat

OUTPUT_DIR = os.path.join(os.getcwd(), 'tts_output')

def download_and_extract_piper():
    piper_dir = os.path.join(os.getcwd(), 'piper')
    if sys.platform.startswith("win"):
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip"
        archive_path = os.path.join(os.getcwd(), "piper_windows_amd64.zip")
        if not os.path.exists(piper_dir) or not os.path.exists(os.path.join(os.getcwd(), "piper.exe")):
            print("Downloading Piper for Windows...")
            urllib.request.urlretrieve(url, archive_path)
            if os.path.exists(piper_dir):
                shutil.rmtree(piper_dir)
            os.makedirs(piper_dir, exist_ok=True)
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
            os.remove(archive_path)
    elif sys.platform.startswith("linux"):
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz"
        archive_path = os.path.join(os.getcwd(), "piper_linux_x86_64.tar.gz")
        if not os.path.exists(piper_dir) or not os.path.exists(os.path.join(os.getcwd(), "piper")):
            print("Downloading Piper for Linux...")
            urllib.request.urlretrieve(url, archive_path)
            if os.path.exists(piper_dir):
                shutil.rmtree(piper_dir)
            os.makedirs(piper_dir, exist_ok=True)
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(os.getcwd())
            os.remove(archive_path)
        # Ensure the Piper binary is executable (always, before use)
        piper_path = os.path.join(os.getcwd(), "piper")
        if os.path.exists(piper_path):
            try:
                os.chmod(piper_path, 0o755)
            except Exception as e:
                raise RuntimeError(f"Failed to set executable permissions on Piper binary: {e}")
    else:
        raise NotImplementedError("Unsupported platform")

def generate(text: str, voice_path: str, config_path: str, output_path: str):
    # Determine Piper executable path
    if sys.platform.startswith("win"):
        PIPER = os.path.join(os.getcwd(), 'piper', 'piper.exe')
    elif sys.platform.startswith("linux"):
        PIPER = os.path.join(os.getcwd(), 'piper', 'piper')
    else:
        raise NotImplementedError("Unsupported platform")

    # Only download and extract Piper if the executable does not exist
    if not os.path.exists(PIPER):
        download_and_extract_piper()

    # On Linux, ensure the Piper binary is executable after download as well
    if sys.platform.startswith("linux") and os.path.exists(PIPER):
        try:
            os.chmod(PIPER, 0o755)
        except Exception as e:
            raise RuntimeError(f"Failed to set executable permissions on Piper binary: {e}")

    # Check again that Piper is executable before running
    if not os.access(PIPER, os.X_OK):
        raise PermissionError(f"Piper binary at {PIPER} is not executable. Please check file permissions.")

    output_file = os.path.join(OUTPUT_DIR, output_path)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Use subprocess.run to execute Piper and send text via stdin
    cmd = [
        PIPER,
        "-m", voice_path,
        "-c", config_path,
        "-f", output_file,
        "--debug",
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=text.encode("utf-8"))
