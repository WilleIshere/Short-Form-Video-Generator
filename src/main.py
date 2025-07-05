from torch._prims_common import check
from src.utils.ffmpeg import check_ffmpeg
from src.text_to_speech.tts_wrapper import *
from src.text_to_speech.voice_manager import check_voices
from src.utils.logger import info

import torch
import json
import os

from pprint import pprint

PIPER = os.path.join(os.getcwd(), 'piper', 'piper.exe')


def main():
    info("Starting main process")
    ffmpeg_path = check_ffmpeg()
    info(f"ffmpeg path: {ffmpeg_path}")

    info("Checking device...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    info("Using device 'CPU', cuda not available..." if device == 'cpu' else "Using device 'GPU', cuda installation found...")

    check_voices()

    #os.system(f'{PIPER} --help')
    #os.system(
    #    f'echo "Once upon a time, in a quiet village nestled between rolling hills, there lived a curious fox named Finn. Every morning, Finn would explore the meadows, searching for new adventures and friends. One sunny day, he discovered a hidden path that led to a sparkling stream, where he met a wise old turtle who shared stories of distant lands. From that day on, Finn and the turtle became the best of friends, exploring the wonders of the world together." | {PIPER} -m en_US-ryan-high.onnx -c #en_US_ryan_high.onnx.json -f tts_output/test.wav --debug'
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
