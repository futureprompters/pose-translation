import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", 'git+https://github.com/facebookresearch/detectron2.git@3ff5dd1cff4417af07097064813c9f28d7461d3c'])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'git+https://github.com/facebookresearch/detectron2@main#subdirectory=projects/DensePose'])


import argparse
import imageio
import numpy as np
import gradio as gr
import os
from PIL import Image
from subprocess import PIPE, run

from animate import PoseTranslation

from huggingface_hub import snapshot_download


snapshot_download(repo_id="runwayml/stable-diffusion-v1-5", local_dir="./stable-diffusion-v1-5")
snapshot_download(repo_id="stabilityai/sd-vae-ft-mse", local_dir="./sd-vae-ft-mse")
snapshot_download(repo_id="zcxu-eric/MagicAnimate", local_dir="./MagicAnimate")

is_spaces = True if "SPACE_ID" in os.environ else False
true_for_shared_ui = False


animator = PoseTranslation("configs/prompts/animation.yaml")

def animate(reference_image, reference_video_state, seed=1, steps=25, guidance_scale=7.5):
    return animator(reference_image, reference_video_state, seed, steps, guidance_scale)

with gr.Blocks() as demo:

    gr.Markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; text-align: center;">
        <a href="https://github.com/magic-research/magic-animate" style="margin-right: 20px; text-decoration: none; display: flex; align-items: center;">
        </a>
        <div>
            <h1 >PoseTranslation</h1>
            <h5 style="margin: 0;">Animate Your Photos with Movie Moves</h5>
        </div>
        </div>
        """)

    gr.Markdown(
        """
        Usage Guide:

1. **Generate Animated Motions:**
   - Paste your reference photo into the left window and the video from which you want to extract motions into the right window. Ensure that the video is no longer than 5 seconds.

2. **Example Selection:**
   - Optionally, you can select sample photos and videos from the examples below. Simply click on them.

3. **Parameter Manipulation:**
   - You can experiment with manipulating the generation parameters (increasing sampling steps, longer generation time, while the guidance scale tells the model how much it can use its "imagination")..

4. **Animation Process:**
   - Click on the "Animate" button to start the animation process.

5. **View Result:**
   - Once the process is complete, the resulting video will appear in the right window.
"""
    )

    gr.Markdown(
        """
     Notes:

- **Optimized Generation:**
  - The generation process is optimized for square photos and videos.

- **Improving Results:**
  - To enhance the results, ensure that the pose in the reference photo closely matches the starting pose in the video.

- **Best Results:**
  - The best results are achieved for faces with distinct shadows and contours.

- **Caution**
  - Please be aware that generating a single video may take up to 7 minutes.

  
  """
    )

    with gr.Row():
        reference_image  = gr.Image(label="Reference Image")
        reference_video  = gr.Video(format="mp4", label="Pose Video",max_length=5)
        animation = gr.Video(
            format="mp4",
            label="Animation Results",
            autoplay=True,
        )

    with gr.Row():
        random_seed         = gr.Textbox(label="Random seed", value=1, info="default: -1")
        sampling_steps      = gr.Textbox(label="Sampling steps", value=25, info="default: 25")
        guidance_scale      = gr.Textbox(label="Guidance scale", value=7.5, info="default: 7.5")
        submit              = gr.Button("Animate")

    def read_video(video):
        reader = imageio.get_reader(video)
        fps = reader.get_meta_data()['fps']
        return video

    def read_image(image, size=512):
        return np.array(Image.fromarray(image).resize((size, size)))

    reference_video.upload(
        read_video,
        reference_video,
        reference_video,
        queue=False
    )
    reference_image.upload(
        read_image,
        reference_image,
        reference_image,
        queue=False
    )
    submit.click(
        animate,
        [reference_image, reference_video, random_seed, sampling_steps, guidance_scale],
        animation
    )

    gr.Markdown("## Examples")
    gr.Examples(
        fn=animate,
        label="Reference image examples:",
        examples=[
            ["inputs/applications/source_image/im1.jpeg"],
            ["inputs/applications/source_image/im2.png"],
            ["inputs/applications/source_image/im3.png"],
            ["inputs/applications/source_image/im4.png"],
        ],
        inputs=[reference_image],
        outputs=animation,
        cache_examples=true_for_shared_ui
    )
    gr.Examples(
        fn=animate,
        label="Pose video examples:",
        examples=[
            ["inputs/applications/reference_video/vid1.mp4"],
            ["inputs/applications/reference_video/vid2.mp4"],
            ["inputs/applications/reference_video/vid3.mp4"],
            ["inputs/applications/reference_video/vid4.mp4"],
        ],
        inputs=[reference_video],
        outputs=animation,
        cache_examples=true_for_shared_ui
    )

    gr.Markdown(
        """
    The creation of this demo was made possible through the use of MagicAnimate and vid2densepose.
    - [vid2densepose](https://github.com/Flode-Labs/vid2densepose)
    - [MagicAnimate](https://showlab.github.io/magicanimate/)
"""
    )

demo.launch(share=True, show_api=False)