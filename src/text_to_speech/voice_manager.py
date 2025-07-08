import os
import json

from pprint import pprint

import requests

import typing
import zipfile
import shutil

import re
import os

from tqdm import tqdm

VOICES = os.path.join(os.getcwd(), 'voices')

VOICES_JSON = os.path.join(os.getcwd(), 'voices.json')
VOICES_EN_US_ZIP = os.path.join(VOICES, 'en_US.zip')
VOICES_EN_GB_ZIP = os.path.join(VOICES, 'en_GB.zip')

def update_voices():

    os.makedirs(VOICES, exist_ok=True)

    # Fetch release assets metadata
    get = requests.get('https://api.github.com/repos/WilleIshere/Short-Form-Video-Generator/releases/tags/_voice_models').json()
    assets = get['assets']

    # Only download zip files if their extracted folders are missing
    for asset in assets:
        name = asset['name']
        url = asset['browser_download_url']
        if not name.endswith('.zip'):
            continue
        extract_folder = os.path.join(VOICES, name[:-4])  # Remove .zip extension
        dest_path = os.path.join(VOICES, name)
        if not os.path.isdir(extract_folder):
            print(f"Downloading {name}...")
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                with open(dest_path, 'wb') as f, tqdm(
                    total=total, unit='B', unit_scale=True, unit_divisor=1024, desc=name
                ) as bar:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
        else:
            print(f"{extract_folder} already exists, skipping download of {name}.")

    # Extract zip files and clean up zip after extraction
    for file in os.listdir(VOICES):
        if file.endswith('.zip'):
            zip_path = os.path.join(VOICES, file)
            extract_folder = os.path.join(VOICES, file[:-4])  # Remove .zip extension

            zip_mtime = os.path.getmtime(zip_path)
            folder_exists = os.path.isdir(extract_folder)

            needs_extract = False
            if not folder_exists:
                needs_extract = True
            else:
                folder_mtime = os.path.getmtime(extract_folder)
                if zip_mtime > folder_mtime:
                    shutil.rmtree(extract_folder)
                    needs_extract = True

            if needs_extract:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    members = zip_ref.infolist()
                    with tqdm(total=len(members), unit='file', desc=f"Extracting {file}") as bar:
                        for member in members:
                            zip_ref.extract(member, extract_folder)
                            bar.update(1)
                os.utime(extract_folder, (zip_mtime, zip_mtime))
                print(f"Extracted {file} to {extract_folder}")

            # Clean up zip file after extraction
            if os.path.isdir(extract_folder):
                try:
                    os.remove(zip_path)
                    print(f"Removed zip file {zip_path}")
                except Exception as e:
                    print(f"Could not remove zip file {zip_path}: {e}")

    voices = {}

    for lang in os.listdir(VOICES):
        voice_folder = os.path.join(VOICES, lang)
        if not os.path.isdir(voice_folder):
            continue  # Skip files like .zip
        voices[lang] = {}

        for voice in os.listdir(voice_folder):
            voice_path = os.path.join(voice_folder, voice)
            if not os.path.isdir(voice_path):
                continue  # Skip files
            voices[lang][voice] = {}

            qualitys_folder = voice_path
            for quality in os.listdir(qualitys_folder):
                quality_path = os.path.join(qualitys_folder, quality)
                if not os.path.isdir(quality_path):
                    continue  # Skip files
                voices[lang][voice][quality] = {}
                contents_folder = quality_path

                for file in os.listdir(contents_folder):
                    file_path = os.path.join(contents_folder, file)
                    if file.endswith('.onnx'):
                        voices[lang][voice][quality]['model_path'] = file_path

                    if file.endswith('.onnx.json'):
                        voices[lang][voice][quality]['config_path'] = file_path

    with open(VOICES_JSON, 'w') as f:
        json.dump(voices, f)

def list_voices() -> dict:
    with open(VOICES_JSON, 'r') as f:
        voices = json.load(f)
    return voices
