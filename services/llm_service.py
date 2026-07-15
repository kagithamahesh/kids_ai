import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_BASE_URL")
)
class LLMService:
     def generate(self, prompt: str):
          print(prompt)
          try:
            response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                        {
                            "role": "system",
                            "content": "You are an expert children's storyteller."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7
                )
            story = response.choices[0].message.content
            try:
                data = json.loads(story)
                required = ["title", "story", "scenes", "moral"]

                for key in required:
                    if key not in data:
                        raise ValueError(f"{key} missing")

                return data
            except json.JSONDecodeError:
                return {
                    "error": "LLM returned invalid JSON",
                    "raw_response": story
                }
          except Exception as e:
            return {
                "error":str(e)
            }
          