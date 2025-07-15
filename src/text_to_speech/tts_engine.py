import src.text_to_speech.edge_tts_wrapper as edge

class TTSWrapper:
    def __init__(self, provider: str):
        if provider == 'edge':
            self.provider = edge

    def generate(self, text: str, voice: str, output_audio: str, output_srt: str):
        self.provider.generate(text, voice, output_audio, output_srt)

    def get_voices(self):
        return self.provider.list_voices()
