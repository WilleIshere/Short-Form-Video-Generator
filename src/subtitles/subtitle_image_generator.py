import pysrt

from PIL import Image, ImageDraw, ImageFont
import os

def generate_subtitle_images():
    data = {}

    srt = pysrt.open('tts_output/transcript.srt')

    prev_end = 0
    i = 0
    sub_i = 0
    for sub in srt:
        if sub.start > prev_end:
            image_path = 'subtitle_images/transparent.png'
            data[i] = {
                'image': image_path,
                'start': sub.start.seconds,
                'end': sub.end.seconds,
                'duration': sub.end.seconds - sub.start.seconds
            }
            i += 1
        image_path = f'subtitle_images/subtitle_{sub_i}.png'
        image = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((50, 350), sub.text, fill=(255, 255, 255), font=font)
        image.save(image_path)
        data[i] = {
            'image': image_path,
            'start': sub.start.seconds,
            'end': sub.end.seconds,
            'duration': sub.end.seconds - sub.start.seconds
        }
        prev_end = sub.end
        i += 1
        sub_i += 1

    with open('subtitle_images/data.json', 'w') as f:
        import json
        json.dump(data, f, indent=4)
