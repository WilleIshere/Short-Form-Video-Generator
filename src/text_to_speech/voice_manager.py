
import os

import json

from pprint import pprint

import requests

import typing
import zipfile
import shutil



VOICES = os.path.join(os.getcwd(), 'voices')

VOICES_JSON = os.path.join(os.getcwd(), 'voices.json')
VOICES_EN_US_ZIP = os.path.join(VOICES, 'en_US.zip')
VOICES_EN_GB_ZIP = os.path.join(VOICES, 'en_GB.zip')

def update_voices():
    # --- ZIP extraction logic ---
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
                    zip_ref.extractall(extract_folder)
                os.utime(extract_folder, (zip_mtime, zip_mtime))
    # --- End ZIP extraction logic ---

    voices = {}

    for lang in os.listdir(VOICES):
        voice_folder = os.path.join(VOICES, lang)
        if not os.path.isdir(voice_folder):
            continue
        voices[lang] = {}

        for voice in os.listdir(voice_folder):
            voices[lang][voice] = {}

            qualitys_folder = os.path.join(voice_folder, voice)
            for quality in os.listdir(qualitys_folder):
                voices[lang][voice][quality] = {}
                contents_folder = os.path.join(qualitys_folder, quality)

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
