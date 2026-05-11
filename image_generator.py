from diffusers import StableDiffusionPipeline
import torch

class AIImageGenerator:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        if torch.cuda.is_available():
            self.pipe = self.pipe.to("cuda")
        else:
            self.pipe = self.pipe.to("cpu")

    def generate(self, prompt, filename="generated_image.png"):
        image = self.pipe(prompt).images[0]
        image.save(filename)
        return filename