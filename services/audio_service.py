import os
from moviepy import AudioFileClip, CompositeAudioClip


class AudioService:
    def __init__(self):
        os.makedirs("output/audio", exist_ok=True)

    def mix_audio(self, narration_path, music_path):
        # Validate files
        if not os.path.exists(narration_path):
            raise FileNotFoundError(f"Narration file not found: {narration_path}")

        if not os.path.exists(music_path):
            raise FileNotFoundError(f"Music file not found: {music_path}")

        # Load audio
        narration = AudioFileClip(narration_path)
        music = AudioFileClip(music_path)

        # Loop background music if it is shorter
        if music.duration < narration.duration:
            loops = int(narration.duration // music.duration) + 1
            music = music.with_effects([]).loop(duration=narration.duration)
        else:
            music = music.subclipped(0, narration.duration)

        # Lower background music volume
        music = music.with_volume_scaled(0.15)

        # Mix narration + music
        final_audio = CompositeAudioClip([music, narration])

        output_path = "output/audio/final_audio.mp3"

        final_audio.write_audiofile(
            output_path,
            fps=44100
        )

        # Release resources
        narration.close()
        music.close()
        final_audio.close()

        return output_path