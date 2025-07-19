import subtitle_parser

from PIL import Image, ImageDraw, ImageFont
import json
import os

def generate_subtitle_images():
    data = {}

    with open('tts_output/transcript.srt', 'r') as f:
        srt = subtitle_parser.SrtParser(f)
        srt.parse()

    prev_end = 0
    i = 0
    sub_i = 0
    for sub in srt.subtitles:
        if sub.start > prev_end:
            gap_path = f'subtitle_images/subtitle_gap_{i}.png'
            gap_img = Image.new('RGBA', (720, 1280), (0, 0, 0, 0))
            gap_img.save(gap_path)
            data[i] = {
                'image': gap_path,
                'start': prev_end,
                'end': sub.start,
                'duration': sub.start - prev_end
            }
            i += 1
        image_path = f'subtitle_images/subtitle_{sub_i}.png'
        image = Image.new('RGBA', (720, 1280), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype('assets/fonts/Roboto.ttf', 72)
        except Exception:
            font = ImageFont.load_default()
        # Center the text
        text = sub.text
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (720 - text_width) // 2
        y = (1280 - text_height) // 2
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        image.save(image_path)
        data[i] = {
            'image': image_path,
            'start': sub.start,
            'end': sub.end,
            'duration': sub.end - sub.start
        }
        i += 1
        sub_i += 1
        prev_end = sub.end

    with open('subtitle_images/data.json', 'w') as f:
        json.dump(data, f, indent=4)
