from fastapi import FastAPI
from pydantic import BaseModel
from services.story_service import StoryService
from services.image_service import ImageService
from services.tts_service import TTSService
from services.video_service import VideoService
from services.audio_service import AudioService
app = FastAPI()

class StoryRequest(BaseModel):
    topic:str
    age:int

@app.post("/generate")
def generate_story(req:StoryRequest):
    service = StoryService()
    image_service = ImageService()
    tts_service = TTSService()
    video_service = VideoService()
    audio_service = AudioService()

    story = service.generate_story(
        topic=req.topic,
        age=req.age
    )
    images = image_service.generate_images(story["scenes"])
    # audio = tts_service.generate_audio(story["story"])
    
    narration = tts_service.generate_audio(story["story"])
    final_audio = audio_service.mix_audio(
                narration,
                "assets/music/happy.mp3"
                )
    video = video_service.generate_video(
        images=images,
        audio_path=final_audio
     )
    
    story["images"] = images
    story["audio"] = final_audio
    story["video"] = video
    return story