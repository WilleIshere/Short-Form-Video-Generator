import json

def generate_subtitle_chunks(background_video_path: str):
    with open('subtitle_images/data.json', 'r') as f:
        data: dict = json.load(f)

    for i in range(len(data.keys())):
