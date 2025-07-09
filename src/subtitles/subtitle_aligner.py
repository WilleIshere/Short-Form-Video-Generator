import subprocess
from rich.console import Console
import os

MFA_MODELS_DIR = os.path.join(os.getcwd(), "mfa_models")
AENEAS_BIN = 'aeneas-cli.exe'

def align_audio_to_text(audio_path: str, text_path: str, out_path: str):
    console = Console()
    with console.status('Aligning tts to text...'):
        # cmd = [
        #     AENEAS_BIN,
        #     audio_path,                         # input audio file
        #     text_path,                              # input text file
        #     'task_language=eng|is_text_type=plain|os_task_file_format=json|os_task_file_levels=1',  # config string
        #     out_path,
        #     "--verbose"        # output file
        # ]

        os.system("mfa model download acoustic english_us_arpa")
        os.system("mfa model download dictionary english_us_arpa")
        os.system(f"mfa validate {MFA_MODELS_DIR} english_us_arpa english_us_arpa")

        #subprocess.call(cmd, check=True)
