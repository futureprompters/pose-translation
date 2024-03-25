import argparse
import inspect
from omegaconf import OmegaConf

import torch

from diffusers import AutoencoderKL, DDIMScheduler
from tqdm import tqdm
from transformers import CLIPTextModel, CLIPTokenizer

from magicanimate.models.unet_controlnet import UNet3DConditionModel
from magicanimate.models.controlnet import ControlNetModel
from magicanimate.models.appearance_encoder import AppearanceEncoderModel
from magicanimate.models.mutual_self_attention import ReferenceAttentionControl
from magicanimate.pipelines.pipeline_animation import AnimationPipeline
from accelerate.utils import set_seed


import vid2densepose.generate_densepose as dpg

from ma import MagicAnimate

import logging

logger = logging.getLogger(__name__)


class PoseTranslation:

    def __init__(self, config):
        logger.info(msg="Initializing PoseTranslation")
        *_, func_args = inspect.getargvalues(inspect.currentframe())
        func_args = dict(func_args)
        
        self.config  = OmegaConf.load(config)

        pipeline, unet, appearance_encoder, reference_control_reader, reference_control_writer = self._load_models()

        self.magicanimate = MagicAnimate(pipeline, unet, func_args, self.config, appearance_encoder, reference_control_reader, reference_control_writer)

        logger.info(msg="Config completed")
        

    def __call__(self, source_image, motion_sequence, random_seed, step, guidance_scale, size=512):

        random_seed = int(random_seed)
        step = int(step)
        guidance_scale = float(guidance_scale)
        # manually set random seed for reproduction
        if random_seed != -1: 
            torch.manual_seed(random_seed)
            set_seed(random_seed)
        else:
            torch.seed()

        denspose_video = dpg.generate_densepose(motion_sequence)

        return self.magicanimate(source_image, denspose_video, random_seed, step, guidance_scale, size)


    def _load_models(self):

        inference_config = OmegaConf.load(self.config.inference_config)
            
       
        ### >>> create animation pipeline >>> ###
        tokenizer = CLIPTokenizer.from_pretrained(self.config.pretrained_model_path, subfolder="tokenizer")
        text_encoder = CLIPTextModel.from_pretrained(self.config.pretrained_model_path, subfolder="text_encoder")
        if self.config.pretrained_unet_path:
            unet = UNet3DConditionModel.from_pretrained_2d(self.config.pretrained_unet_path, unet_additional_kwargs=OmegaConf.to_container(inference_config.unet_additional_kwargs))
        else:
            unet = UNet3DConditionModel.from_pretrained_2d(self.config.pretrained_model_path, subfolder="unet", unet_additional_kwargs=OmegaConf.to_container(inference_config.unet_additional_kwargs))
        appearance_encoder = AppearanceEncoderModel.from_pretrained(self.config.pretrained_appearance_encoder_path, subfolder="appearance_encoder").cuda()
        reference_control_writer = ReferenceAttentionControl(appearance_encoder, do_classifier_free_guidance=True, mode='write', fusion_blocks=self.config.fusion_blocks)
        reference_control_reader = ReferenceAttentionControl(unet, do_classifier_free_guidance=True, mode='read', fusion_blocks=self.config.fusion_blocks)
        if self.config.pretrained_vae_path is not None:
            vae = AutoencoderKL.from_pretrained(self.config.pretrained_vae_path)
        else:
            vae = AutoencoderKL.from_pretrained(self.config.pretrained_model_path, subfolder="vae")

        ### Load controlnet
        controlnet   = ControlNetModel.from_pretrained(self.config.pretrained_controlnet_path)

        vae.to(torch.float16)
        unet.to(torch.float16)
        text_encoder.to(torch.float16)
        controlnet.to(torch.float16)
        appearance_encoder.to(torch.float16)
        
        unet.enable_xformers_memory_efficient_attention()
        appearance_encoder.enable_xformers_memory_efficient_attention()
        controlnet.enable_xformers_memory_efficient_attention()

        pipeline = AnimationPipeline(
            vae=vae, text_encoder=text_encoder, tokenizer=tokenizer, unet=unet, controlnet=controlnet,
            scheduler=DDIMScheduler(**OmegaConf.to_container(inference_config.noise_scheduler_kwargs)),
        ).to("cuda")

        return pipeline, unet, appearance_encoder, reference_control_reader, reference_control_writer