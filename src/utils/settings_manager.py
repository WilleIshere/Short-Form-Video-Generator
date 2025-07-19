import configparser
import os

class Settings:
    def __init__(self, settings_file='config.ini'):
        self.config = configparser.ConfigParser()
        if os.path.exists(settings_file):
            self.config.read(settings_file)
        else:
            self.create_default_settings(settings_file)
            
    def create_default_settings(self, settings_file):
        self.config['Subtitles'] = {
            'font_path': 'assets/fonts/Roboto.ttf',
            'font_size': '72',
            'stroke_width': '4',
            'stroke_color': '0,0,0',
            'text_color': '255,255,255',
            'padding': '12',
            'align': 'center'
        }
        self.config['Video'] = {
            'background_video_path': 'assets/background_videos/background.mp4',
            'output_video_path': 'video_chunks/final_video.mp4',
            'resolution': '720x1280',
            'fps': '24',
        }
        self.config['Advanced Video'] {
            'codec': 'libx264',
            'audio_codec': 'aac',
            'preset': 'ultrafast',
            'ffmpeg_params': '-crf 30 -pix_fmt yuv420p'
        }
        self.config['TTS'] = {
            'provider': 'edge',
            'voice': 'default',
        }
        with open(settings_file, 'w') as configfile:
            self.config.write(configfile)
            