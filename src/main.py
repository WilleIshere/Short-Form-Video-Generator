from src.renderer.subtitle_renderer import generate_subtitle_chunks
from src.renderer.final_renderer import render
from src.subtitles.subtitle_image_generator import generate_subtitle_images
from src.text_to_speech.tts_engine import TTSWrapper

from src.utils.text_processor import combine_text_files
from src.utils.ffmpeg import check_ffmpeg
from src.utils.cleaner import clean

from src.utils.loggr import info
from src.utils.settings_manager import Settings


TTS_PROVIDER = 'edge' # Piper is not used due to issues with aligning subtitle timestamps

def main():
    # Load subtitle manager (loads/creates subtitle_settings.ini)
    settings = Settings()
    clean()

    info("Checking ffmpeg installation...")
    ffmpeg_path = check_ffmpeg()
    info(f"ffmpeg path: {ffmpeg_path}")

    # info("Checking device...")
    # import torch
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # info("Using device 'CPU', cuda not available..." if device == 'cpu' else "Using device 'GPU', cuda installation found...")

    info("Processing text files...")
    combine_text_files('text.txt', 'title.txt', 'body.txt')
    with open('text.txt', 'r') as f:
        text = f.read()

    info("Generating tts...")
    tts = TTSWrapper(settings)
    voices = tts.get_voices()
    tts.generate(
        text=text, voice=voices[0],
        output_audio='tts_output/final_tts.wav',
        output_srt='tts_output/transcript.srt'
    )

    generate_subtitle_images(settings)

    subtitle_chunks = generate_subtitle_chunks(settings)
    render(
        settings,
        subs=subtitle_chunks,
    )
    

