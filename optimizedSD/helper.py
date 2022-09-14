from optimizedSD.optimized_txt2img import run_txt2img
from optimizedSD.optimized_img2img import run_img2img
# from optimized_txt2img import run_txt2img
# from optimized_img2img import run_img2img
import os
import sys
sys.path.append('/home/os/gits/stable-diffusion/')

def txt2img_helper(prompt=None, n_samples=2, n_iter=1, ddim_steps = 10, ddim_eta=0.0, scale=7.5, W=512, H=512, outdir=None):
    skip_grid = False
    skip_save = False
    fixed_code = False
    seed = None
    turbo = False
    precision = "autocast"
    device = "cuda"
    # sampler = "plms"
    sampler = "ddim"
    if outdir is None:
        outdir = 'output/'
    format = "png"

    unet_bs = 1
    f = 8 # downsampling factor
    C = 4 # latent channels

    images = run_txt2img(prompt=prompt, n_samples=n_samples, n_iter=n_iter, ddim_steps=ddim_steps, ddim_eta=ddim_eta, scale=scale, device=device, skip_grid=skip_grid, skip_save=skip_save, outdir=outdir, fixed_code=fixed_code, unet_bs=unet_bs, turbo=turbo, precision=precision, format=format, sampler=sampler, seed=seed, H=H, W=W, f=f, C=C)

    return images


def img2img_helper(prompt=None, n_samples=2, n_iter=1, ddim_steps = 10, ddim_eta=0.0, scale=7.5, W=512, H=512, outdir=None, init_img=None, strength=0.5):
    skip_grid = False
    skip_save = False
    fixed_code = False
    seed = None
    turbo = False
    precision = "autocast"
    device = "cuda"
    # sampler = "plms"
    sampler = "ddim"
    if outdir is None:
        outdir = 'output/'
    format = "png"
    # Workaround
    # https://github.com/ROCmSoftwarePlatform/MIOpen/issues/1204#issuecomment-947860840
    # terminate called after throwing an instance of 'miopen::Exception'
    # what():  /build/miopen-hip/src/MIOpen-rocm-5.2.3/src/hipoc/hipoc_program.cpp:300: Code object build failed. Source: naive_conv.cpp
    # export MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0
    # export MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_BWD=0
    # export MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_WRW=0
    os.environ["MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD"] = "0"
    os.environ["MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_BWD"] = "0"
    os.environ["MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_WRW"] = "0"

    unet_bs = 1
    f = 8 # downsampling factor
    C = 4 # latent channels or Classifier free guidance aka Cfg?

    images = run_img2img(prompt=prompt, n_samples=n_samples, n_iter=n_iter, ddim_steps=ddim_steps, ddim_eta=ddim_eta, scale=scale, device=device, skip_grid=skip_grid, skip_save=skip_save, outdir=outdir, fixed_code=fixed_code, unet_bs=unet_bs, turbo=turbo, precision=precision, format=format, sampler=sampler, seed=seed, H=H, W=W, f=f, C=C, init_img=init_img, strength=strength)

    return images













