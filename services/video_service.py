import os
from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)

from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut
from PIL import Image, ImageDraw, ImageFont


class VideoService:

    def __init__(self):
        os.makedirs("output/video", exist_ok=True)

    def generate_video(self, images, audio_path, subtitles):

        if not os.path.exists(audio_path):
            raise FileNotFoundError(audio_path)

        audio = AudioFileClip(audio_path)

        duration = audio.duration / len(images)

        image_clips = []

        for image in images:

            clip = (
                ImageClip(image)
                .resized(height=720)
                .with_duration(duration)
                .with_effects([
                    FadeIn(0.5),
                    FadeOut(0.5)
                ])
            )

            # Slow zoom effect
            clip = clip.resized(
                lambda t: 1 + 0.10 * (t / duration)
            )

            image_clips.append(clip)

        video = concatenate_videoclips(
            image_clips,
            method="compose"
        )

        video = video.with_audio(audio)

        subtitle_clips = []

        for i, sub in enumerate(subtitles):
            img = self.create_subtitle_image(
                sub["text"],
                i
            )
            clip = (
                ImageClip(img)
                .with_start(sub["start"])
                .with_duration(sub["end"] - sub["start"])
                .with_position(("center", 580))
             )
            subtitle_clips.append(clip)
        final_video = CompositeVideoClip(
            [video] + subtitle_clips
        )

        output_path = "output/video/story.mp4"

        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            temp_audiofile="output/video/temp-audio.m4a",
            remove_temp=True,
            ffmpeg_params=["-movflags", "+faststart"],
        )

        final_video.close()
        video.close()
        audio.close()

        return output_path


    def create_subtitle_image(self, text, index):
        width = 1280
        height = 120

        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(
                "C:/Windows/Fonts/arial.ttf",
                42
            )
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Black outline
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                draw.text(
                    (x + dx, y + dy),
                    text,
                    font=font,
                    fill="black"
                )

        # White text
        draw.text(
            (x, y),
            text,
            font=font,
            fill="white"
        )

        path = f"output/video/subtitle_{index}.png"

        image.save(path)

        return path

# import os
# from moviepy import ImageClip, AudioFileClip, concatenate_videoclips


# class VideoService:
#     def __init__(self):
#         os.makedirs("output/video", exist_ok=True)

#     def generate_video(self, images, audio_path):
#         # Validate audio file exists
#         if not audio_path or not os.path.exists(audio_path):
#            raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
#         # Load audio first
#         audio = AudioFileClip(audio_path)

#         print("Audio path:", audio_path)
#         print("Audio duration:", audio.duration)

#         duration = audio.duration / len(images)

#         clips = []

#         for image in images:
#             clip = (
#                 ImageClip(image)
#                 .with_duration(duration)
#             )
#             clips.append(clip)

#         final_video = concatenate_videoclips(
#             clips,
#             method="compose"
#         )

#         # Attach narration
#         final_video = final_video.with_audio(audio)

#         output_path = "output/video/story.mp4"
        

#         final_video.write_videofile(
#             output_path,
#             codec="libx264",
#             audio_codec="aac",
#             fps=24,
#             temp_audiofile="output/video/temp-audio.m4a",
#             remove_temp=True,
#             ffmpeg_params=["-movflags", "+faststart"]
#             # output_path,
#             # codec="libx264",
#             # audio_codec="aac",
#             # fps=24
#         )

#         final_video.close()
#         audio.close()

#         return output_path