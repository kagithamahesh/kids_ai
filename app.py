from fastapi import FastAPI
from pydantic import BaseModel
from services.story_service import StoryService


app = FastAPI()

class StoryRequest(BaseModel):
    topic:str
    age:int

@app.post("/generate")
def generate_story(req:StoryRequest):
    service = StoryService()
    return service.generate_story(
        topic=req.topic,
        age=req.age
    )