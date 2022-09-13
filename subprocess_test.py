from subprocess import Popen, PIPE, call
import sys
sys.path.append('/home/os/gits/stable-diffusion')


python_bin = '/home/os/gits/stable-diffusion/venv/bin/python3'
script = '/home/os/gits/stable-diffusion/optimizedSD/optimized_txt2img.py'


prompt = 'its dangerous to go alone'
height = 100
width = 100
n_iter = 1
ddim_steps = 100
n_samples = 10

options_dict = {'--prompt': prompt, '--H': height, '--W': width, '--n_iter': n_iter, '--ddim_steps': ddim_steps, '--n_samples': n_samples}

options = ' '.join([f'{k} {v}' if k != '--prompt' else f'{k} "{v}"' for k, v in options_dict.items()])


# activate_this_file = '/home/os/gits/stable-diffusion/venv/bin/activate_this.py'
# exec(open(activate_this_file).read(), dict(__file__=activate_this_file))

cmd = ' '.join([python_bin, script, options])
p = Popen([python_bin, script], stdout=PIPE, stderr=PIPE)

stdout, stderr = p.communicate()
print(stdout)
print(stderr)

