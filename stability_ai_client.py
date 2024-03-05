import base64
import os
import requests

class StabilityClient:

    def __init__(self, api_key):
        self.engine_id = "stable-diffusion-xl-1024-v1-0"
        self.api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        self.api_key = api_key

        self.DEFAULT_NEGATIVE_PROMPT = 'ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers'

    def generate(self, prompt):
        if self.api_key is None:
            raise Exception("Missing Stability API key.")

        response = requests.post(
            f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": f"{prompt}",
                        "weight": 1
                    },
                    {
                        "text": self.DEFAULT_NEGATIVE_PROMPT,
                        "weight": -1
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            print("Non-200 response: " + str(response.text))

            return None

        data = response.json()
        # print(data)

        # since we are only generating one image for now
        image_base64 = data["artifacts"][0]['base64']
        # print(image_base64)
        return image_base64



# if __name__ == ''


