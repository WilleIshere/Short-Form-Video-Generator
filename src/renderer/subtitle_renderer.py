from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, vfx
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
    num_chunks = len(data.keys())

    for i in range(num_chunks):
        print(f"Processing chunk {i+1}/{num_chunks}")
        entry = data[str(i)]

        img_path = entry['image']
        start_time_ms = entry['start']
        end_time_ms = entry['end']
        duration_ms = entry['duration']

        # Convert ms to seconds
        start = start_time_ms / 1000
        end = end_time_ms / 1000
        duration = end - start

        # Skip invalid durations
        if duration <= 0:
            print(f"Skipping chunk {i+1}: zero or negative duration.")
            continue

        # Create the ImageClip and add effects
        clip = (
            ImageClip(img_path)
                .with_start(start)
                .with_duration(duration)
                .with_effects([vfx.CrossFadeIn(duration=clip.duration/2)]) # Animation effect
                .with_position(('center', 'center'))  # Center subtitle images
        ) 
        clips.append(clip)

        # Track the maximum end time for the composite duration
        if end > max_end:
            max_end = end

    # Composite all subtitle image clips
    result = CompositeVideoClip(clips, size=(720, 1280)).with_duration(max_end)
    return result


