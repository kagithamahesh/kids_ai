import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)


class ImageService:
    def __init__(self):
        os.makedirs("output/images", exist_ok=True)

    def generate_image(self, prompt: str, output_path: str):

        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )

        image.save(output_path)

        return output_path

    def generate_images(self, scenes):
        paths = []

        for i, scene in enumerate(scenes):

            prompt = f"""
Cute cartoon illustration.
{scene}
Children's storybook.
Bright colors.
Friendly characters.
No text.
High quality.
"""

            path = f"output/images/scene{i+1}.png"

            self.generate_image(prompt, path)

            paths.append(path)

        return paths
# import os
# import requests
# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# load_dotenv()
# API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

# headers = {
#     "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"
# }

# class ImageService:
#     def __init__(self):
#          os.makedirs("output/images", exist_ok=True)

#     def generate_image(self,prompt:str,output_path:str):
#         response = requests.post(
#         API_URL,
#         headers=headers,
#         json={
#             "inputs":prompt
#         }  
#         )
#         if response.status_code !=200:
#             raise Exception(response.text)
#         with open(output_path,"wb") as f:
#             f.write(response.content)
#         return output_path
    
#     def generate_images(self, scenes):
#         paths = []
#         for i,scene in enumerate(scenes):
#             prompt = f"""
#                Cute cartoon illustration.
#                {scene}
#                Children's storybook.
#                Bright colors.
#                Friendly characters.
#                No text.
#                High quality.
#                """
#             path = f"output/images/scene{i+1}.png"

#             self.generate_image(prompt, path)

#             paths.append(path)
#         return paths 