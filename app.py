from fastapi import FastAPI
from pydantic import BaseModel
from moviepy import AudioFileClip

from services.story_service import StoryService
from services.image_service import ImageService
from services.tts_service import TTSService
from services.video_service import VideoService
from services.audio_service import AudioService
from services.subtitle_service import SubtitleService

app = FastAPI()


class StoryRequest(BaseModel):
    topic: str
    age: int


@app.post("/generate")
def generate_story(req: StoryRequest):

    story_service = StoryService()
    image_service = ImageService()
    tts_service = TTSService()
    audio_service = AudioService()
    subtitle_service = SubtitleService()
    video_service = VideoService()

    # Generate Story
    story = story_service.generate_story(
        topic=req.topic,
        age=req.age
    )

    # Generate Images
    images = image_service.generate_images(
        story["scenes"]
    )

    # Generate Narration
    narration = tts_service.generate_audio(
        story["story"]
    )

    # Mix Background Music
    final_audio = audio_service.mix_audio(
        narration,
        "assets/music/happy.mp3"
    )

    # Get Audio Duration
    audio_clip = AudioFileClip(final_audio)

    subtitles = subtitle_service.generate_subtitles(
        story["story"],
        audio_clip.duration
    )

    audio_clip.close()

    # Generate Video
    video = video_service.generate_video(
        images=images,
        audio_path=final_audio,
        subtitles=subtitles
    )

    story["images"] = images
    story["audio"] = final_audio
    story["video"] = video
    story["subtitles"] = subtitles

    return story