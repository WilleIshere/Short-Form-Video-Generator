import subprocess

AENEAS_BIN = 'aeneas-cli.exe'

def align_audio_to_text(audio_path: str, text_path: str, out_path: str):
    cmd = [
        AENEAS_BIN,
        audio_path,                         # input audio file
        text_path,                              # input text file
        'task_language=eng|is_text_type=plain|os_task_file_format=json|os_task_file_levels=1',  # config string
        out_path                               # output file
    ]
    subprocess.run(cmd, check=True)
