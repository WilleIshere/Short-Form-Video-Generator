from moviepy import VideoFileClip, CompositeVideoClip, AudioFileClip

def render(settings, subs, audio_path='tts_output/final_tts.wav'):
    # Extract video and advanced settings
    video_settings = settings['Video']
    adv_settings = settings['Advanced Video']
    width, height = settings['Video']['resolution'].split('x')
    width, height = int(w), int(h)
    print(w, h)

    # Load background video and TTS audio
    background = VideoFileClip(video_settings['background_video_path'])
    tts_audio = AudioFileClip(audio_path)

    # Crop and resize background to 9:16 (720x1280)
    w, h = background.size
    background = background.cropped(x1=w/3, y1=0, x2=w*2/3, y2=h)
    background = background.resized((width, height))

    # Determine the final video duration
    final_duration = max(subs.duration, tts_audio.duration)

    # Composite background and subtitles
    composite = CompositeVideoClip([
        background.subclipped(0, final_duration),
        subs
    ]).with_audio(tts_audio)

    # Write the final video
    composite.write_videofile(
        video_settings['output_video_path'],
        codec=adv_settings['codec'],
        fps=int(video_settings['fps']),
        audio_codec=adv_settings['audio_codec'],
        preset=adv_settings['preset'],
    )

    # Cleanup
    background.close()
    tts_audio.close()
    subs.close()
    composite.close()