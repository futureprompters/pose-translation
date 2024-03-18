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

from animate import MagicAnimate

from huggingface_hub import snapshot_download


snapshot_download(repo_id="runwayml/stable-diffusion-v1-5", local_dir="./stable-diffusion-v1-5")
snapshot_download(repo_id="stabilityai/sd-vae-ft-mse", local_dir="./sd-vae-ft-mse")
snapshot_download(repo_id="zcxu-eric/MagicAnimate", local_dir="./MagicAnimate")

is_spaces = True if "SPACE_ID" in os.environ else False
true_for_shared_ui = False


animator = MagicAnimate()

def animate(reference_image, reference_video_state, seed=1, steps=25, guidance_scale=7.5):
    return animator(reference_image, reference_video_state, seed, steps, guidance_scale)

with gr.Blocks() as demo:

    gr.HTML(
        """
        <div style="display: flex; justify-content: center; align-items: center; text-align: center;">
        <a href="https://github.com/magic-research/magic-animate" style="margin-right: 20px; text-decoration: none; display: flex; align-items: center;">
        </a>
        <div>
            <h1 >PoseTranslation</h1>
            <h5 style="margin: 0;">vid2densepose+MagicAnimate</h5>
        </div>
        </div>
        """)
    

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
            ["inputs/applications/source_image/im3.jpg"],
            ["inputs/applications/source_image/im4.png"]
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
        ],
        inputs=[reference_video],
        outputs=animation,
        cache_examples=true_for_shared_ui
    )

demo.launch(share=True, show_api=False)
