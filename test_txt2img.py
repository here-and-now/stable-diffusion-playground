import sys
sys.path.append('/home/os/gits/stable-diffusion/')
from optimized_txt2img import run_txt2img


prompt = "testen"
n_samples = 1
n_iter = 1
ddim_steps = 10
ddim_eta = 0.0
scale = 7.5
device = "cuda"
skip_grid = False
skip_save = False
outdir = None
fixed_code = False
unet_bs = 1
turbo = False
precision = "autocast"
format = "png"
sampler = "plms"
seed = None
outdir = 'output/'

run_txt2img(prompt=prompt, n_samples=n_samples, n_iter=n_iter, ddim_steps=ddim_steps, ddim_eta=ddim_eta, scale=scale, device=device, skip_grid=skip_grid, skip_save=skip_save, outdir=outdir, fixed_code=fixed_code, unet_bs=unet_bs, turbo=turbo, precision=precision, format=format, sampler=sampler, seed=seed)















