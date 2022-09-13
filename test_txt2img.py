import sys
sys.path.append('/home/os/gits/stable-diffusion/')
sys.path.append('/home/os/gits/stable-diffusion-playground/optimizedSD/')
from optimized_txt2img import run_txt2img



def txt2img_helper(prompt=None, n_samples=10, n_iter=1, ddim_steps = 10, ddim_eta=0.0, scale=7.5, W=512, H=512):
    skip_grid = False
    skip_save = False
    fixed_code = False
    seed = None
    turbo = False
    precision = "autocast"
    device = "cuda"
    # sampler = "plms"
    sampler = "ddim"
    outdir = 'output/'
    format = "png"

    unet_bs = 1
    f = 8 # downsampling factor
    C = 4 # latent channels

    images = run_txt2img(prompt=prompt, n_samples=n_samples, n_iter=n_iter, ddim_steps=ddim_steps, ddim_eta=ddim_eta, scale=scale, device=device, skip_grid=skip_grid, skip_save=skip_save, outdir=outdir, fixed_code=fixed_code, unet_bs=unet_bs, turbo=turbo, precision=precision, format=format, sampler=sampler, seed=seed, H=H, W=W, f=f, C=C)

    return images

txt2img_helper('dog', n_samples=10, n_iter=1, ddim_steps = 10, ddim_eta=0.0, scale=7.5, W=512, H=512)










