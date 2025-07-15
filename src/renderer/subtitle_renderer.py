from moviepy import ImageClip, concatenate_videoclips
import json
import os

def ms_to_hms(ms: int) -> str:
    seconds = ms // 1000
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def generate_subtitle_chunks(background_video_path: str, ffmpeg_path: str) -> None:
    with open('subtitle_images/data.json', 'r') as f:
        data: dict = json.load(f)

    clips = []
    max_end = 0
    for i in range(len(data.keys())):
        print(f"Processing chunk {i+1}/{len(data.keys())}")
        img_path, start_time, end_time, duration = data[str(i)].values()
        start = start_time / 1000
        end = end_time / 1000
        clip = ImageClip(img_path).with_start(start).with_duration(end - start)
        clips.append(clip)
        if end > max_end:
            max_end = end
    from moviepy import CompositeVideoClip
    result = CompositeVideoClip(clips, size=(1280, 720)).with_duration(max_end)
    return result


