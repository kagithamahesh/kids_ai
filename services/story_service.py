import os
import json
from dotenv import load_dotenv


from services.prompt_service import build_story_prompt
from services.llm_service import LLMService


class StoryService:
    def __init__(self):
         self.llm = LLMService()
    def generate_story(self,topic:str,age:int):
        prompt = build_story_prompt(topic,age)
        response = self.llm.generate(prompt)
        
        return response
        # print(prompt)
        # try:
        #     response = client.chat.completions.create(
        #         model="llama-3.3-70b-versatile",
        #         messages=[
        #             {
        #                 "role": "system",
        #                 "content": "You are an expert children's storyteller."
        #             },
        #             {
        #                 "role": "user",
        #                 "content": prompt
        #             }
        #         ],
        #         temperature=0.7
        #     )
        #     story = response.choices[0].message.content
            
        #     try:
        #         data = json.loads(story)
        #         required = ["title", "story", "scenes", "moral"]

        #         for key in required:
        #             if key not in data:
        #                 raise ValueError(f"{key} missing")

        #         return data
        #     except json.JSONDecodeError:
        #         return {
        #             "error": "LLM returned invalid JSON",
        #             "raw_response": story
        #         }
        # except Exception as e:
        #     return {
        #         "error":str(e)
        #     }
