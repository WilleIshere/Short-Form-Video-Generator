from src.subtitles.subtitle_aligner import align_audio_to_text
from src.subtitles.subtitle_generator import generate_subtitles
from src.text_to_speech.tts_wrapper import (
    prepare_tts_output_dir,
    generate_tts_chunks,
    combine_audio_chunks,
    OUTPUT_DIR
)
from src.text_to_speech.voice_manager import update_voices, list_voices
from src.utils.text_processor import text_to_words, combine_text_files
from src.utils.ffmpeg import check_ffmpeg
from src.utils.loggr import info

import os
import json


def main():
    info("Starting main process")
    ffmpeg_path = check_ffmpeg()
    info(f"ffmpeg path: {ffmpeg_path}")

    info("Checking device...")
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    info("Using device 'CPU', cuda not available..." if device == 'cpu' else "Using device 'GPU', cuda installation found...")

    update_voices()
    voice = list_voices()['en_US']['amy']['low']

    # Prepare TTS output directory
    prepare_tts_output_dir(OUTPUT_DIR)

    # Generate TTS for title
    with open("title.txt", "r", encoding="utf-8") as f:
        title_text = f.read()
    title_chunk_files = generate_tts_chunks(
        text=title_text,
        voice=voice,
        prefix="title",
        output_dir=OUTPUT_DIR
    )

    # Generate TTS for body
    with open("body.txt", "r", encoding="utf-8") as f:
        body_text = f.read()
    body_chunk_files = generate_tts_chunks(
        text=body_text,
        voice=voice,
        prefix="chunk",
        output_dir=OUTPUT_DIR
    )

    # Combine all TTS audio into one file
    final_path = os.path.join(OUTPUT_DIR, 'final_tts.wav')
    combine_audio_chunks(
        chunk_files=title_chunk_files + body_chunk_files,
        output_path=final_path
    )

    text_path = 'text.txt'
    combine_text_files(text_path, 'title.txt', 'body.txt')

    words_path = 'words.txt'
    text_to_words(text_path, words_path)

    aligned_path = 'tts_output/transcription.json'
    align_audio_to_text(final_path, words_path, aligned_path)

    subs = generate_subtitles()

    render_
