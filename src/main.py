from src.utils.ffmpeg import check_ffmpeg
from src.text_to_speech.tts_wrapper import *
from src.text_to_speech.piper import generate
from src.text_to_speech.voice_manager import update_voices
from src.utils.logger import info

#import torch
import json
import os

from pprint import pprint


def main():
    #info("Starting main process")
    #ffmpeg_path = check_ffmpeg()
    #info(f"ffmpeg path: {ffmpeg_path}")

    #info("Checking device...")
    #device = "cuda" if torch.cuda.is_available() else "cpu"
    #info("Using device 'CPU', cuda not available..." if device == 'cpu' else "Using device 'GPU', cuda installation found...")

    update_voices()

    # Ensure tts_output directory exists
    os.makedirs('tts_output', exist_ok=True)

    #generate(
    #    "Once upon a time, in a quiet village nestled between rolling green hills, there lived a curious child named Sam. Every evening, Sam would sit by the window, watching the stars twinkle above and dreaming of adventures beyond the horizon. One night, a gentle breeze carried the sound of distant music, and Sam followed it into the forest, where magical creatures danced beneath the moonlight. From that night on, Sam knew that the world was full of wonder, and every day became a new adventure.",
    #    voice['model'],
    #    voice['config'],
    #    'test.wav'
    #)

    exit()
    info("Loading tts engine...")
    from TTS.api import TTS
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)

    speakers = tts.speakers
    print(speakers)
    for i, voice in enumerate(speakers):

        info(f"Generating audio.. ({i + 1}/{len(speakers)})")
        tts.tts_to_file(
            text="This is a test of the text-to-speech system. The quick brown fox jumps over the lazy dog. We are generating this audio to ensure that the TTS engine is working correctly and can handle longer sentences with natural prosody and clarity. Thank you for listening to this demonstration.",
            speaker="Uta Obando",
            language="en",
            file_path=f"tts_output/{voice}.wav"
        )
