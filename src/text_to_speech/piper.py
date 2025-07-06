import os
import subprocess

PIPER = os.path.join(os.getcwd(), 'piper', 'piper.exe')

def generate(text: str, voice_path: str, config_path: str, output_path: str):
    print('Generating tts...')
    print(f"[DEBUG] Text to synthesize:\n{text}\n")
    cmd = [
        PIPER,
        "-m", voice_path,
        "-c", config_path,
        "-f", os.path.join(os.getcwd(), output_path),
        "--debug",
        "--input-stdin"
    ]
    print(f"[DEBUG] Command to run:\n{' '.join(cmd)}\n")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=text.encode("utf-8"))
    print('done!')
    print("[DEBUG] Piper stdout:\n", stdout.decode(errors="replace"))
    print("[DEBUG] Piper stderr:\n", stderr.decode(errors="replace"))
    output_full_path = os.path.join(os.getcwd(), output_path)
    if os.path.exists(output_full_path):
        print(f"[DEBUG] Output file generated: {output_full_path}")
    else:
        print(f"[DEBUG] Output file NOT found: {output_full_path}")
