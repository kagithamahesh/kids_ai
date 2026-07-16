import os
import asyncio
import edge_tts


class TTSService:
    def __init__(self):
        os.makedirs("output/audio", exist_ok=True)
    
    async def _generate(self, text:str,output_path: str):
        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-AvaMultilingualNeural"
          )
        await communicate.save(output_path)

    def generate_audio(self, text: str):

        output_path = "output/audio/story.mp3"

        asyncio.run(
            self._generate(text, output_path)
        )

        return output_path