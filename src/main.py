from src.utils.ffmpeg import check_ffmpeg
from src.text_to_speech.tts_wrapper import *
from src.utils.logger import info

import torch
from TTS.api import TTS

def main():
    info("Starting main process")
    ffmpeg_path = check_ffmpeg()
    info(f"ffmpeg path: {ffmpeg_path}")

    info("Checking device...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    info("Using device 'CPU', cuda not available..." if device == 'cpu' else "Using device 'GPU', cuda installation found...")

    info("Loading tts engine...")
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)

    speakers = tts.speakers
    for i, voice in enumerate(speakers):

        info(f"Generating audio.. ({i + 1}/{len(speakers)})")
        tts.tts_to_file(
            text="This is a test of the text-to-speech system. The quick brown fox jumps over the lazy dog. We are generating this audio to ensure that the TTS engine is working correctly and can handle longer sentences with natural prosody and clarity. Thank you for listening to this demonstration.",
            speaker="Uta Obando",
            language="en",
            file_path=f"tts_output/{voice}.wav"
        )
