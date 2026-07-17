import re

class SubtitleService:

    def generate_subtitles(self, story, audio_duration):

        sentences = re.split(r'(?<=[.!?])\s+', story.strip())

        duration = audio_duration / len(sentences)

        subtitles = []

        current = 0

        for sentence in sentences:

            subtitles.append({
                "text": sentence,
                "start": current,
                "end": current + duration
            })

            current += duration

        return subtitles