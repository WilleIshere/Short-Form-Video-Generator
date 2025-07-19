import configparser
import os

class Settings(configparser.ConfigParser):
    def __init__(self, settings_file='config.ini'):
        super().__init__()
        if os.path.exists(settings_file):
            self.read(settings_file)
        else:
            self.create_default_settings(settings_file)
            
    def create_default_settings(self, settings_file):
        self['Subtitles'] = {
            'font_path': 'assets/fonts/Roboto.ttf',
            'font_size': '72',
            'stroke_width': '4',
            'stroke_color': '0,0,0',
            'text_color': '255,255,255',
            'padding': '12',
            'align': 'center'
        }
        self['Video'] = {
            'background_video_path': 'assets/background_videos/background.mp4',
            'output_video_path': 'video_chunks/final_video.mp4',
            'resolution': '720x1280',
            'fps': '24',
        }
        self['Advanced Video'] = {
            'codec': 'libx264',
            'audio_codec': 'aac',
            'preset': 'ultrafast',
        }
        self['TTS'] = {
            'provider': 'edge',
            'voice': 'default',
        }
        with open(settings_file, 'w') as configfile:
            self.write(configfile)
            