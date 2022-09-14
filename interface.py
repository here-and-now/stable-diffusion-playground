from optimizedSD.helper import txt2img_helper, img2img_helper
from PIL import Image
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, CustomJS, Slider, Button, Div, DataTable, TableColumn, NumberFormatter, FileInput, RangeSlider, Select, TextAreaInput, TextInput
from bokeh.layouts import column, row
from bokeh.io import curdoc
import numpy as np
import glob
import time
import os
import io
import base64
import sys
sys.path.append('/home/os/gits/stable-diffusion/')
sys.path.append('/home/os/gits/stable-diffusion/')


def image_array(image):
    xdim, ydim = image.size
    print("Dimensions: ({xdim}, {ydim})".format(**locals()))
    # Create an array representation for the image `img`, and an 8-bit "4
    # layer/RGBA" version of it `view`.
    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
    # Copy the RGBA image into view, flipping it so it comes right-side up
    # with a lower-left origin
    view[:, :, :] = np.flipud(np.asarray(image))
    return img, view, xdim, ydim


def update_image(attrname, old, new):
    image = Image.open(select.value).convert('RGBA')
    img, view, xdim, ydim = image_array(image)
    source.data = dict(image=[img])


def import_file(attrname, old, new):
    # file_input returns b64 encoded string
    buf = io.BytesIO(base64.b64decode(file_input.value))
    image = Image.open(buf).convert('RGBA')
    img, view, xdim, ydim = image_array(image)
    source.data = dict(image=[img])


def txt2img_button_handler():
    parameter_dict = get_parameter_values()

    images = txt2img_helper(prompt=parameter_dict['prompt'], n_samples=parameter_dict['n_samples'], n_iter=parameter_dict['n_iter'],
             ddim_steps=parameter_dict['ddim_steps'], ddim_eta=parameter_dict['ddim_eta'],
             scale=parameter_dict['scale'], W=parameter_dict['W'], H=parameter_dict['H'], outdir=None)

       
def get_parameter_values():
    parameter_dict = {'prompt': prompt_input.value,
                      'n_samples': n_samples_slider.value,
                      'n_iter': n_iter_slider.value,
                      'ddim_steps': ddim_steps_slider.value,
                      'ddim_eta': ddim_eta_slider.value,
                      'scale': scale_slider.value,
                      'W': W_slider.value,
                      'H': H_slider.value,
                      'strength': strength_slider.value}
    return parameter_dict

    select.options = [x[1] for x in images]
    select.value = images[0][1]
    image = images[0][0].convert('RGBA')
    img, view, xdim, ydim = image_array(image)
    source.data = dict(image=[img])




def img2img_button_handler():
    parameter_dict = get_parameter_values()
    init_img = 'inputs/' + file_input.filename

    images = img2img_helper(init_img=init_img, n_samples=parameter_dict['n_samples'], n_iter=parameter_dict['n_iter'],
                            ddim_steps=parameter_dict['ddim_steps'], ddim_eta=parameter_dict['ddim_eta'],
                            scale=parameter_dict['scale'], W=parameter_dict['W'], H=parameter_dict['H'], strength=parameter_dict['strength'], outdir=None)

    select.options = [x[1] for x in images]
    select.value = images[0][1]

    image = images[0][0].convert('RGBA')
    img, view, xdim, ydim = image_array(image)

    source.data = dict(image=[img])


# get list of images
image_list = glob.glob('/home/os/gits/stable-diffusion-playground/imgs/*.png')
image_list.sort()
images = [Image.open(x).convert('RGBA') for x in image_list]
image = images[0]

img, view, xdim, ydim = image_array(image)
source = ColumnDataSource(data=dict(image=[img]))


### txt2img section ###
dim = max(xdim, ydim)
fig1 = figure(title='Stable Diffusion',
              x_range=(0, dim), y_range=(0, dim),
              tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save'
              )
fig1.image_rgba(image='image', x=0, y=0, dw=xdim, dh=ydim, source=source)
### end txt2img section ###

# img2img section ###
fig2 = figure(title='Stable Diffusion',
              x_range=(0, dim), y_range=(0, dim),
              tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save'
              )
fig2.image_rgba(image='image', x=0, y=0, dw=xdim, dh=ydim, source=source)
### end img2img section ###


### GUI ###


# Select tool
select = Select(title="Image:", value=image_list[0], options=image_list)
select.on_change('value', update_image)

# File input
file_input = FileInput(accept=".png")
file_input.on_change('value', import_file)

# prompt input
prompt_input = TextAreaInput(value="prompt here", rows=5, title="Text:")

txt2img_button = Button(label="Generate", button_type="success")
txt2img_button.on_click(txt2img_button_handler)

img2img_button = Button(label="Generate", button_type="success")
img2img_button.on_click(img2img_button_handler)

# Sliders
slider_ddim_eta = Slider(start=0.0, end=1.0, value=0.0,
                         step=0.01, title="ddim_eta")
slider_ddim_steps = Slider(start=0, end=500, value=10,
                           step=1, title="ddim_steps")
slider_scale = Slider(start=1.0, end=10.0, value=7.5, step=0.1, title="scale")
slider_n_samples = Slider(start=1, end=10, value=2, step=1, title="n_samples")
slider_n_iter = Slider(start=1, end=10, value=1, step=1, title="n_iter")
slider_W = Slider(start=0, end=1024, value=512, step=32, title="W")
slider_H = Slider(start=0, end=1024, value=512, step=32, title="H")
slider_strength = Slider(start=0.0, end=1.0, value=0.5,
                         step=0.01, title="strength")


layout_slider = column(slider_ddim_eta, slider_ddim_steps, slider_scale,
                       slider_n_samples, slider_n_iter, slider_W, slider_H, slider_strength)

# Layout
# txt2img
txt2img_layout = row(column(fig1, select), column(
    prompt_input, txt2img_button, layout_slider))
txt2img_tab = Panel(child=txt2img_layout, title='Text to Image')

# img2img
img2img_layout = row(column(fig1, select, file_input), column(
    prompt_input, img2img_button, layout_slider), column(fig2))
img2img_tab = Panel(child=img2img_layout, title='Image to Image')

# tab it
tabs = Tabs(tabs=[txt2img_tab, img2img_tab])

curdoc().add_root(tabs)
