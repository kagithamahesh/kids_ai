from fastapi import FastAPI
from pydantic import BaseModel
from services.story_service import StoryService
from services.image_service import ImageService
from services.tts_service import TTSService
from services.video_service import VideoService

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
    
    story = service.generate_story(
        topic=req.topic,
        age=req.age
    )
    images = image_service.generate_images(story["scenes"])
    audio = tts_service.generate_audio(story["story"])
    video = video_service.generate_video(
        images=images,
        audio_path=audio
     )
    
    
    story["images"] = images
    story["audio"] = audio
    story["video"] = video
    return story