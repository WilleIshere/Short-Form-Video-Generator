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

    # Load font once
    try:
        font = ImageFont.truetype('assets/fonts/Roboto.ttf', 72)
    except Exception:
        font = ImageFont.load_default()

    for sub in srt.subtitles:
        # Insert transparent gap image if needed
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

        # Prepare subtitle text and image size
        text = sub.text
        # Calculate text bounding box for tight cropping
        dummy_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        dummy_draw = ImageDraw.Draw(dummy_img)
        text_bbox = dummy_draw.textbbox((0, 0), text, font=font, align='center')
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        stroke_width = 4
        pad_x = stroke_width + 8  # Horizontal padding
        pad_y_top = stroke_width + 8  # Top padding
        pad_y_bottom = stroke_width * 2 + 8  # Extra bottom padding for descenders and stroke
        img_w = text_width + 2 * pad_x
        img_h = text_height + pad_y_top + pad_y_bottom

        # Create the subtitle image
        image_path = f'subtitle_images/subtitle_{sub_i}.png'
        image = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw stroke (outline)
        stroke_fill = (0, 0, 0)
        for dx in range(-stroke_width, stroke_width+1):
            for dy in range(-stroke_width, stroke_width+1):
                if dx != 0 or dy != 0:
                    draw.text((pad_x+dx, pad_y_top+dy), text, font=font, fill=stroke_fill)
        # Draw main text
        draw.text((pad_x, pad_y_top), text, fill=(255, 255, 255), font=font)

        image.save(image_path)
        data[i] = {
            'image': image_path,
            'start': sub.start,
            'end': sub.end,
            'duration': sub.end - sub.start,
            'width': img_w,
            'height': img_h
        }
        i += 1
        sub_i += 1
        prev_end = sub.end

    with open('subtitle_images/data.json', 'w') as f:
        json.dump(data, f, indent=4)
