from moviepy import VideoFileClip, CompositeVideoClip, AudioFileClip

def render(subs, background_video_path='assets/background_videos/background.mp4', audio_path='tts_output/final_tts.wav'):
    background = VideoFileClip(background_video_path)
    tts_audio = AudioFileClip(audio_path)
    w, h = background.size
    background = background.cropped(x1=w/3, y1=0, x2=w*2/3, y2=h)
    background = background.resized((720, 1280))
    
    final = CompositeVideoClip([background.subclipped(0, max([subs.duration, tts_audio.duration])), subs])
    final = final.with_audio(tts_audio)
    final.write_videofile(
        'video_chunks/final_video.mp4',
        codec='libx264', fps=background.fps, 
        audio_codec='aac', preset='ultrafast',
        ffmpeg_params=['-crf', '30', '-pix_fmt', 'yuv420p']
    )
    
    background.close()
    tts_audio.close()
    subs.close()
    final.close()