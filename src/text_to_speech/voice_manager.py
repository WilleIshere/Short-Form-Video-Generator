import os
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import sys
from typing import List, Dict, Tuple

VOICES_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "voices.json")
VOICES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "voices")

print_lock = threading.Lock()
spinner_cycle = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

def download_file(url, dest_path, voice_name, quality, filetype, active_downloads):
    key = (voice_name, quality, filetype)
    try:
        active_downloads[key] = True
        urllib.request.urlretrieve(url, dest_path)
        with print_lock:
            print(f"\n[{voice_name} - {quality}] Downloaded {filetype}: {dest_path}")
    except Exception as e:
        with print_lock:
            print(f"\n[{voice_name} - {quality}] Failed to download {filetype} from {url}: {e}")
    finally:
        active_downloads.pop(key, None)

def check_voices(max_workers=6):
    # Load voices.json
    with open(VOICES_JSON_PATH, "r", encoding="utf-8") as f:
        voices = json.load(f)

    os.makedirs(VOICES_DIR, exist_ok=True)

    download_tasks = []
    active_downloads = {}
    executor = ThreadPoolExecutor(max_workers=max_workers)
    stop_event = threading.Event()

    import shutil

    def progress_indicator():
        idx = 0
        MAX_DISPLAY = 2
        while not stop_event.is_set():
            with print_lock:
                # Clear the line using ANSI escape code
                sys.stdout.write("\r\033[K")
                if not active_downloads and all(f.done() for f in download_tasks):
                    sys.stdout.flush()
                    break
                sys.stdout.write("Downloading voices: ")
                items = list(active_downloads.keys())
                display_items = items[:MAX_DISPLAY]
                for i, (voice_name, quality, filetype) in enumerate(display_items):
                    spinner = spinner_cycle[(idx + i) % len(spinner_cycle)]
                    sys.stdout.write(f"{spinner} {voice_name} [{quality}] ({filetype})  ")
                if len(items) > MAX_DISPLAY:
                    sys.stdout.write(f"+{len(items) - MAX_DISPLAY} more...  ")
                sys.stdout.flush()
            idx += 1
            time.sleep(0.1)

    try:
        for lang, voices_by_lang in voices.items():
            for voice_name, qualities in voices_by_lang.items():
                for quality, files in qualities.items():
                    for filetype in ["model", "config"]:
                        url = files[filetype]
                        filename = url.split("/")[-1].split("?")[0]
                        dest_path = os.path.join(VOICES_DIR, filename)
                        if not os.path.exists(dest_path):
                            future = executor.submit(download_file, url, dest_path, voice_name, quality, filetype, active_downloads)
                            download_tasks.append(future)
                        else:
                            with print_lock:
                                print(f"[{voice_name} - {quality}] Already downloaded: {dest_path}")

        # Start progress indicator in a background thread
        indicator_thread = threading.Thread(target=progress_indicator)
        indicator_thread.start()

        # Wait for all downloads to finish
        for future in as_completed(download_tasks):
            pass

        indicator_thread.join()
        executor.shutdown()
        print("All downloads complete.")
    except KeyboardInterrupt:
        stop_event.set()
        print("\nDownload interrupted by user (Ctrl+C). Cleaning up...")
        executor.shutdown(wait=False, cancel_futures=True)
        # Wait for indicator to finish
        if 'indicator_thread' in locals():
            indicator_thread.join()
        print("Stopped all downloads.")

def get_voice_files(lang: str, quality: str) -> List[Dict[str, str]]:
   """
   Returns a list of dicts with 'voice', 'model', and 'config' for the given language and quality.
   """
   # Load voices.json
   with open(VOICES_JSON_PATH, "r", encoding="utf-8") as f:
       voices = json.load(f)
   result = []
   if lang not in voices:
       return result
   for voice_name, qualities in voices[lang].items():
       if quality in qualities:
           result.append({
               "voice": voice_name,
               "model": qualities[quality]["model"],
               "config": qualities[quality]["config"]
           })
   return result
