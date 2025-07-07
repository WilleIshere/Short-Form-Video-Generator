import os
import re
import shutil
from typing import List

from pydub import AudioSegment
from rich.console import Console

from src.text_to_speech.piper import generate, OUTPUT_DIR
from src.utils.logger import info

console = Console()

def split_sentences(text: str) -> List[str]:
    """
    Splits the input text into sentences using punctuation.
    """
    return re.split(r'(?<=[.!?])\s+', text)

def generate_tts_chunks(
    text: str,
    voice: dict,
    prefix: str,
    output_dir: str = OUTPUT_DIR
) -> List[str]:
    """
    Generates TTS audio chunks for each sentence in the text.

    Args:
        text (str): The input text to synthesize.
        voice (dict): Voice configuration with 'model_path' and 'config_path'.
        prefix (str): Prefix for output wav files (e.g., 'title', 'chunk').
        output_dir (str): Directory to save the output wav files.

    Returns:
        List[str]: List of paths to generated wav files.
    """
    sentences = split_sentences(text)
    chunk_files = []
    for i, sentence in enumerate(sentences):
        with console.status(f'Generating {prefix} TTS ({i + 1}/{len(sentences)})', spinner='material'):
            if sentence.strip():
                chunk_filename = f'{prefix}_{i}.wav'
                generate(
                    sentence.strip(),
                    voice['model_path'],
                    voice['config_path'],
                    chunk_filename
                )
                chunk_path = os.path.join(output_dir, chunk_filename)
                chunk_files.append(chunk_path)
                print(f'Saved "{chunk_filename}"')
    return chunk_files

def combine_audio_chunks(
    chunk_files: List[str],
    output_path: str
) -> None:
    """
    Combines multiple wav files into a single wav file.

    Args:
        chunk_files (List[str]): List of wav file paths to combine.
        output_path (str): Path to save the combined wav file.
    """
    with console.status(f'Combining TTS audios into "{output_path}"', spinner='material'):
        combined = AudioSegment.empty()
        for wav_file in chunk_files:
            audio = AudioSegment.from_wav(wav_file)
            combined += audio
        combined.export(output_path, format='wav')
        print(f'Saved final TTS as: "{output_path}"')

def prepare_tts_output_dir(output_dir: str = "tts_output"):
    """
    Removes and recreates the TTS output directory.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
