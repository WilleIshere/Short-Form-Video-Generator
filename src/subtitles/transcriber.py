import os
import json
from src.utils.logger import info

try:
    import whisper_timestamped as whisper
except ImportError:
    whisper = None

def transcribe_audio(
    audio_path: str,
    model_name: str = "small.en",
    device: str = "",
    language: str = "en"
):
    """
    Transcribes the given audio file using whisper_timestamped.

    Args:
        audio_path (str): Path to the audio file to transcribe.
        model_name (str): Whisper model name to use.
        device (str): Device to use ('cuda' or 'cpu'). If None, will auto-detect.
        language (str): Language code for transcription.

    Returns:
        dict: The transcription result.
    """
    if whisper is None:
        raise ImportError("whisper_timestamped is not installed.")

    if not device:
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        info(f"Auto-selected device: {device}")

    info(f"Loading audio from: {audio_path}")
    audio = whisper.load_audio(audio_path)

    info(f"Loading Whisper model: {model_name} on device: {device}")
    model = whisper.load_model(model_name, device=device)

    info(f"Transcribing audio with language: {language}")
    result = whisper.transcribe(model, audio, language=language, verbose=False)

    return result

def save_transcription(result: dict, output_path: str):
    """
    Saves the transcription result to a JSON file.

    Args:
        result (dict): The transcription result.
        output_path (str): Path to save the JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    info(f"Saved transcription to: {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe audio to subtitles using Whisper.")
    parser.add_argument("audio_path", type=str, help="Path to the audio file to transcribe.")
    parser.add_argument("--model", type=str, default="small.en", help="Whisper model name.")
    parser.add_argument("--device", type=str, default=None, help="Device to use ('cuda' or 'cpu').")
    parser.add_argument("--language", type=str, default="en", help="Language code for transcription.")
    parser.add_argument("--output", type=str, default="transcription.json", help="Output JSON file path.")

    args = parser.parse_args()

    result = transcribe_audio(
        audio_path=args.audio_path,
        model_name=args.model,
        device=args.device,
        language=args.language
    )
    save_transcription(result, args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
