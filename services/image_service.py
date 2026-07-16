import os
import time
import requests
from urllib.parse import quote


class ImageService:
    def __init__(self, max_retries=3, backoff_seconds=2):
        os.makedirs("output/images", exist_ok=True)
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def generate_image(self, prompt, output_path):

        url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"

        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(
                    url,
                    timeout=120,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                if response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return output_path

                # Retry on transient server-side errors (rate limiting,
                # Cloudflare hiccups, etc). Fail fast on real client errors.
                if response.status_code in (429, 500, 502, 503, 504, 520, 521, 522, 523, 524):
                    last_error = Exception(
                        f"Transient error {response.status_code}: {response.text[:200]}"
                    )
                else:
                    raise Exception(f"Image generation failed ({response.status_code}): {response.text[:200]}")

            except requests.RequestException as e:
                last_error = e

            if attempt < self.max_retries:
                time.sleep(self.backoff_seconds * attempt)

        raise Exception(f"Image generation failed after {self.max_retries} attempts: {last_error}")

    def generate_images(self, scenes):
        paths = []

        for i, scene in enumerate(scenes):

            clean_scene = " ".join(scene.split())

            prompt = (
                "Cute cartoon illustration. "
                f"{clean_scene} "
                "Children's storybook. Disney Pixar style. "
                "Bright colors. Friendly animals. High quality."
            )

            path = f"output/images/scene{i+1}.png"

            self.generate_image(prompt, path)

            paths.append(path)

        return paths

# import os
# import requests
# from urllib.parse import quote


# class ImageService:
#     def __init__(self):
#         os.makedirs("output/images", exist_ok=True)

#     def generate_image(self, prompt, output_path):

#         url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"

#         response = requests.get(url, timeout=120)

#         if response.status_code != 200:
#             raise Exception(response.text)

#         with open(output_path, "wb") as f:
#             f.write(response.content)

#         return output_path

#     def generate_images(self, scenes):
#         paths = []

#         for i, scene in enumerate(scenes):

#             prompt = f"""
#             Cute cartoon illustration.
#             {scene}
#             Children's storybook.
#             Disney Pixar style.
#             Bright colors.
#             Friendly animals.
#             High quality.
#             """

#             path = f"output/images/scene{i+1}.png"

#             self.generate_image(prompt, path)

#             paths.append(path)

#         return paths

# import os
# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# load_dotenv()

# client = InferenceClient(
#     provider="hf-inference",
#     api_key=os.getenv("HUGGINGFACE_API_KEY")
# )


# class ImageService:
#     def __init__(self):
#         os.makedirs("output/images", exist_ok=True)

#     def generate_image(self, prompt: str, output_path: str):

#         image = client.text_to_image(
#             prompt,
#             model="black-forest-labs/FLUX.1-schnell"
#         )

#         image.save(output_path)

#         return output_path

#     def generate_images(self, scenes):
#         paths = []

#         for i, scene in enumerate(scenes):

#             prompt = f"""
# Cute cartoon illustration.
# {scene}
# Children's storybook.
# Bright colors.
# Friendly characters.
# No text.
# High quality.
# """

#             path = f"output/images/scene{i+1}.png"

#             self.generate_image(prompt, path)

#             paths.append(path)

#         return paths
# # import os
# # import requests
# # from dotenv import load_dotenv
# # from huggingface_hub import InferenceClient

# # load_dotenv()
# # API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

# # headers = {
# #     "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"
# # }

# # class ImageService:
# #     def __init__(self):
# #          os.makedirs("output/images", exist_ok=True)

# #     def generate_image(self,prompt:str,output_path:str):
# #         response = requests.post(
# #         API_URL,
# #         headers=headers,
# #         json={
# #             "inputs":prompt
# #         }  
# #         )
# #         if response.status_code !=200:
# #             raise Exception(response.text)
# #         with open(output_path,"wb") as f:
# #             f.write(response.content)
# #         return output_path
    
# #     def generate_images(self, scenes):
# #         paths = []
# #         for i,scene in enumerate(scenes):
# #             prompt = f"""
# #                Cute cartoon illustration.
# #                {scene}
# #                Children's storybook.
# #                Bright colors.
# #                Friendly characters.
# #                No text.
# #                High quality.
# #                """
# #             path = f"output/images/scene{i+1}.png"

# #             self.generate_image(prompt, path)

# #             paths.append(path)
# #         return paths 