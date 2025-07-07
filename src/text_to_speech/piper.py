import os
from pprint import pprint
import subprocess

PIPER = os.path.join(os.getcwd(), 'piper', 'piper.exe')
OUTPUT_DIR = os.path.join(os.getcwd(), 'tts_output')

def generate(text: str, voice_path: str, config_path: str, output_path: str):
    cmd = [
        PIPER,
        "-m", voice_path,
        "-c", config_path,
        "-f", os.path.join(OUTPUT_DIR, output_path),
        "--debug",
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=text.encode("utf-8"))
