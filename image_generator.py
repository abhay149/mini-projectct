from diffusers import (
    AutoPipelineForText2Image,
    DPMSolverMultistepScheduler
)

import torch


class AIImageGenerator:

    def __init__(self):

        # ==========================================
        # BEST REALISTIC SDXL MODEL
        # ==========================================
        self.model_id = "RunDiffusion/Juggernaut-XL-v9"

        # ==========================================
        # DEVICE DETECTION
        # ==========================================
        if torch.backends.mps.is_available():
            self.device = "mps"
            self.dtype = torch.float16
            print("🚀 Using Apple Metal GPU (MPS)")
        else:
            self.device = "cpu"
            self.dtype = torch.float32
            print("⚠ Using CPU")

        # ==========================================
        # LOAD PIPELINE
        # ==========================================
        print("🎨 Loading AI Model...")

        self.pipe = AutoPipelineForText2Image.from_pretrained(
            self.model_id,
            torch_dtype=self.dtype,
            use_safetensors=True,
            variant="fp16" if self.device == "mps" else None
        )

        # ==========================================
        # BETTER SCHEDULER
        # ==========================================
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )

        # ==========================================
        # MOVE TO DEVICE
        # ==========================================
        self.pipe = self.pipe.to(self.device)

        # ==========================================
        # PERFORMANCE OPTIMIZATION
        # ==========================================
        self.pipe.enable_attention_slicing()
        self.pipe.enable_vae_slicing()

        print("✅ AI Image Generator Ready")

    # ==========================================
    # GENERATE IMAGE
    # ==========================================
    def generate(
        self,
        prompt,
        filename="generated_image.png",
        negative_prompt=None,
        width=832,
        height=1216,
        steps=40,
        guidance_scale=5,
        seed=42
    ):

        # ==========================================
        # NEGATIVE PROMPT
        # ==========================================
        if negative_prompt is None:
            negative_prompt = """
            blurry,
            low quality,
            distorted,
            deformed,
            ugly,
            bad anatomy,
            extra fingers,
            extra hands,
            malformed face,
            bad eyes,
            cropped,
            duplicate,
            watermark,
            text,
            logo,
            unrealistic,
            noisy,
            oversaturated,
            abstract,
            weird architecture,
            mutated hands,
            poorly drawn face
            """

        # ==========================================
        # CLEAN PROFESSIONAL PROMPT
        # ==========================================
        enhanced_prompt = f"""
        RAW photo,
        realistic photography,
        cinematic lighting,
        professional DSLR photography,
        realistic skin texture,
        sharp focus,
        detailed eyes,
        depth of field,
        bokeh,
        movie still,

        {prompt}
        """

        # ==========================================
        # RANDOM SEED
        # ==========================================
        generator = torch.Generator(
            device=self.device
        ).manual_seed(seed)

        # ==========================================
        # GENERATE IMAGE
        # ==========================================
        print("🎨 Generating High Quality Image...")

        image = self.pipe(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator
        ).images[0]

        # ==========================================
        # SAVE IMAGE
        # ==========================================
        image.save(filename)

        print(f"✅ Image saved as: {filename}")

        return filename


# ==========================================
# TESTING
# ==========================================
if __name__ == "__main__":

    generator = AIImageGenerator()

    prompt = """
    A realistic Indian man wearing black hoodie,
    sitting inside futuristic AI laboratory,
    blue holographic computer screens,
    cyberpunk atmosphere,
    rain outside glass window,
    realistic face,
    cinematic movie lighting
    """

    generator.generate(
        prompt=prompt,
        filename="ai_hacker.png",
        width=832,
        height=1216,
        steps=40,
        guidance_scale=5,
        seed=42
    )