import asyncio

from edge_tts import Communicate, SubMaker
import edge_tts


def generate(text: str, voice, output_wav, output_srt):
    communicate = Communicate(text, voice)
    submaker = SubMaker()
    with open(output_wav, "wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)

    with open(output_srt, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())

def list_voices():
    voices_json = asyncio.run(edge_tts.list_voices())
    voices = []
    for voice in voices_json:
        if 'en-' in voice['Locale']:
            voices.append(voice['ShortName'])
    sorted_voices = sorted(voices)
    return sorted_voices
