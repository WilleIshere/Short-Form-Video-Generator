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
        for segment in text_data['fragments']:
            s.status = f'Writing image: {count}'
            im = Image.new("RGBA", (1080, 1920))
            draw = ImageDraw.Draw(im)

            text_length = draw.textlength(segment['lines'][0], font)
            x = (im.width - text_length) / 2
            y = im.height / 2

            draw.text((x, y), segment['lines'][0], fill=(255, 255, 255), font=font)

            image_path = f'subtitle_images/{count}.png'
            im.save(image_path)

            image = {
                'image_path': image_path,
                'start': float(segment['begin']),
                'end': float(segment['end'])
            }
            images.append(image)

            count += 1
