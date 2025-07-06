import os
import json
from pprint import pprint
import requests
import shutil
import typing

VOICES = os.path.join(os.getcwd(), 'voices')
VOICES_JSON = os.path.join(os.getcwd(), 'voices.json')

def update_voices():
    voices = {}

    for lang in os.listdir(VOICES):
        voice_folder = os.path.join(VOICES, lang)
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

                    if file == "samples":
                        shutil.rmtree(file_path)


    with open(VOICES_JSON, 'w') as f:
        json.dump(voices, f)


def list_voices() -> dict:
    with open(VOICES_JSON, 'r') as f:
        voices = json.load(f)
    return voices
