import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut

class VideoService:
    def __init__(self):
        os.makedirs("output/video", exist_ok=True)

    def generate_video(self, images, audio_path):
        # Validate audio file exists
        if not audio_path or not os.path.exists(audio_path):
           raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
        # Load audio first
        audio = AudioFileClip(audio_path)

        print("Audio path:", audio_path)
        print("Audio duration:", audio.duration)

        duration = audio.duration / len(images)

        clips = []

        for image in images:
            clip = (
                ImageClip(image)
                .with_duration(duration)
                .resized(height=720)
                .with_effects([
                    FadeIn(0.5),
                    FadeOut(0.5)
                ])
            )
            # Slow zoom from 100% to 110%
            clip = clip.resized(
                lambda t: 1 + 0.10 * (t / duration)
            )

            clips.append(clip)

        final_video = concatenate_videoclips(
            clips,
            method="compose"
        )

        # Attach narration
        final_video = final_video.with_audio(audio)

        output_path = "output/video/story.mp4"

        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            temp_audiofile="output/video/temp-audio.m4a",
            remove_temp=True,
            ffmpeg_params=["-movflags", "+faststart"]
        )

        final_video.close()
        audio.close()

        return output_path


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