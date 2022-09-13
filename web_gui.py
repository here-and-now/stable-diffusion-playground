import sys
sys.path.append('/home/os/gits/stable-diffusion/')
sys.path.append('/home/os/gits/stable-diffusion/')
import base64
import io
import os
import time
import glob
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Button, Div, DataTable, TableColumn, NumberFormatter, FileInput, RangeSlider, Select, TextAreaInput, TextInput
from bokeh.plotting import figure, show, output_file
from bokeh.models.widgets import Tabs, Panel


from PIL import Image

from optimizedSD.helper import txt2img_helper, img2img_helper

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
    prompt = text_area.value
    ddim_eta = slider_ddim_eta.value
    ddim_steps = slider_ddim_steps.value
    scale = slider_scale.value
    n_samples = slider_n_samples.value
    n_iter = slider_n_iter.value
    W = slider_W.value
    H = slider_H.value

    # images = txt2img_helper(prompt=prompt, n_samples=2, n_iter=1, ddim_steps = 10, ddim_eta=0.0, scale=7.5, W=512, H=512, outdir=None)
    images = txt2img_helper(prompt=prompt, n_samples=n_samples, n_iter=n_iter, ddim_steps = ddim_steps, ddim_eta=ddim_eta, scale=scale, W=W, H=H, outdir=None)
    select.options = [x[1] for x in images]
    select.value = images[0][1]

    image = images[0][0].convert('RGBA')
    img, view, xdim, ydim = image_array(image)

    source.data = dict(image=[img])

def img2img_button_handler():
    prompt = text_area.value
    ddim_eta = slider_ddim_eta.value
    ddim_steps = slider_ddim_steps.value
    scale = slider_scale.value
    n_samples = slider_n_samples.value
    n_iter = slider_n_iter.value
    W = slider_W.value
    H = slider_H.value

    # init_img = Image.open(select.value).convert('RGBA')
    init_img = select.value

    # images = txt2img_helper(prompt=prompt, n_samples=2, n_iter=1, ddim_steps = 10, ddim_eta=0.0, scale=7.5, W=512, H=512, outdir=None)
    images = img2img_helper(prompt=prompt, n_samples=n_samples, n_iter=n_iter, ddim_steps = ddim_steps, ddim_eta=ddim_eta, scale=scale, W=W, H=H, outdir=None, init_img=init_img)
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
text_area = TextAreaInput(value="prompt here", rows=5, title="Text:")

txt2img_button = Button(label="Generate", button_type="success")
txt2img_button.on_click(txt2img_button_handler)

img2img_button = Button(label="Generate", button_type="success")
img2img_button.on_click(img2img_button_handler)


# Sliders
slider_ddim_eta = Slider(start=0.0, end=1.0, value=0.0, step=0.01, title="ddim_eta")
slider_ddim_steps = Slider(start=1, end=100, value=10, step=1, title="ddim_steps")
slider_scale = Slider(start=1.0, end=10.0, value=7.5, step=0.1, title="scale")
slider_n_samples = Slider(start=1, end=10, value=2, step=1, title="n_samples")
slider_n_iter = Slider(start=1, end=10, value=1, step=1, title="n_iter")
slider_W = Slider(start=0, end=1024, value=512, step=32, title="W")
slider_H = Slider(start=0, end=1024, value=512, step=32, title="H")


layout_slider = column(slider_ddim_eta, slider_ddim_steps, slider_scale, slider_n_samples, slider_n_iter, slider_W, slider_H)

# Layout
#txt2img
txt2img_layout =  row(column(fig1, select), column(text_area, txt2img_button, layout_slider))
txt2img_tab = Panel(child=txt2img_layout, title='Text to Image')

#img2img
img2img_layout = row(column(fig1, select), column(text_area, img2img_button, layout_slider), column(fig2))
img2img_tab = Panel(child=img2img_layout, title='Image to Image')

# tab it
tabs = Tabs(tabs=[txt2img_tab, img2img_tab])

curdoc().add_root(tabs)

