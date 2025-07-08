import shutil
from PIL import Image, ImageDraw, ImageFont
import json
import os
import subprocess
import tempfile

import ffmpeg

import rich

def generate_subtitles(ffmpeg_bin: str, output_path="output.mp4", resolution=(1080, 1920), fps=30):
    if os.path.isdir('subtitle_images'):
        shutil.rmtree('subtitle_images')
    os.makedirs('subtitle_images', exist_ok=True)

    with open('tts_output/transcription.json', 'r') as f:
        text_data = json.load(f)

    font = ImageFont.truetype("fonts/Roboto.ttf", size=70)

    console = rich.console.Console()

    images = []

    with console.status('Writing images...') as s:
        count = 0
        for segment in text_data['segments']:
            for word in segment['words']:
                s.status = f'Writing image: {count}'
                im = Image.new("RGBA", (1080, 1920))
                draw = ImageDraw.Draw(im)

                text_length = draw.textlength(word['text'], font)
                x = (im.width - text_length) / 2
                y = im.height / 2

                draw.text((x, y), word['text'], fill=(255, 255, 255), font=font)

                image_path = f'subtitle_images/{count}.png'
                im.save(image_path)

                image = {
                    'image_path': image_path,
                    'start': word['start'],
                    'end': word['end']
                }
                images.append(image)

                count += 1

    filter_complex = []
    input_cmds = []
    total_duration = max(clip['end'] for clip in images)

    # Start with black background
    input_cmds += [
        '-f', 'lavfi',
        '-i', f'color=black:s={resolution[0]}x{resolution[1]}:d={total_duration}:r={fps}'
    ]

    for i, clip in enumerate(images):
        input_cmds += ['-loop', '1', '-t', str(clip['end'] - clip['start']), '-i', clip['image_path']]
        # overlay=x=0:y=0:enable='between(t,START,END)'
        overlay = f"[{i+1}:v]scale={resolution[0]}:{resolution[1]}[img{i}];" \
                    f"[v{i}]overlay=enable='between(t,{clip['start']},{clip['end']})'[v{i+1}]"
        if i == 0:
            overlay = f"[0:v][img0]{overlay}"
        filter_complex.append(overlay)

    final_filter = ";".join(filter_complex)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(final_filter)
            filter_file_path = f.name

    cmd = [
        ffmpeg_bin, "-y",
        *input_cmds,
        "-filter_complex_script", filter_file_path,
        "-map", f"[v{len(images)}]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    print("Running command:\n", " ".join(cmd))
    subprocess.run(cmd, check=True)
