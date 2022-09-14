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

# def image_array(image):
    # xdim, ydim = image.size
    # print("Dimensions: ({xdim}, {ydim})".format(**locals()))
    # # Create an array representation for the image `img`, and an 8-bit "4
    # # layer/RGBA" version of it `view`.
    # img = np.empty((ydim, xdim), dtype=np.uint32)
    # view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
    # # Copy the RGBA image into view, flipping it so it comes right-side up
    # # with a lower-left origin
    # view[:, :, :] = np.flipud(np.asarray(image))
    # return img, view, xdim, ydim


# def update_on_select(attrname, old, new):
    # # update_image(images)
    # pass

# def import_file(attrname, old, new):
    # # file_input returns b64 encoded string
    # buf = io.BytesIO(base64.b64decode(file_input.value))
    # update_image(buf)

# def get_parameter_values():
    # parameter_dict = {'prompt': prompt_input.value,
                     # 'n_samples': slider_n_samples.value,
                     # 'n_iter': slider_n_iter.value,
                     # 'ddim_steps': slider_ddim_steps.value,
                     # 'ddim_eta': slider_ddim_eta.value,
                     # 'scale': slider_scale.value,
                     # 'W': slider_W.value,
                     # 'H': slider_H.value,
                     # 'strength': slider_strength.value}
    # return parameter_dict

# def txt2img_button_handler():
    # parameter_dict = get_parameter_values()
    # images = txt2img_helper(prompt=parameter_dict['prompt'], n_samples=parameter_dict['n_samples'], n_iter=parameter_dict['n_iter'],
                            # ddim_steps=parameter_dict['ddim_steps'], ddim_eta=parameter_dict['ddim_eta'],
                            # scale=parameter_dict['scale'], W=parameter_dict['W'], H=parameter_dict['H'], outdir=None)
    # update_image(images)

# def img2img_button_handler():
    # parameter_dict = get_parameter_values()
    # init_img = 'inputs/' + file_input.filename

    # images = img2img_helper(init_img=init_img, n_samples=parameter_dict['n_samples'], n_iter=parameter_dict['n_iter'],
                            # ddim_steps=parameter_dict['ddim_steps'], ddim_eta=parameter_dict['ddim_eta'],
                            # scale=parameter_dict['scale'], W=parameter_dict['W'], H=parameter_dict['H'], strength=parameter_dict['strength'], outdir=None)

    # update_image(images)

# def update_image(images):
    # # select.options = [x[1] for x in images]
    # # select.value = images[0][1]

    # select.options = images
    # select.value = images[0]

    # image = Image.open(select.value).convert('RGBA')
    # img, view, xdim, ydim = image_array(image)
    # source.data = dict(image=[img])

    # return img, view, xdim, xdim


# get list of images
# image_list = glob.glob('/home/os/gits/stable-diffusion-playground/imgs/*.png')
# image_list.sort()

# source = ColumnDataSource(data=dict(image=[img]))
# img, view, xdim, ydim = update_image(image_list)

### txt2img section ###


class StableDiffusionBokehApp():
    def __init__(self):
        self.source = ColumnDataSource(data=dict(image=[]))
        
        self.images_list = []
        self.active_image = None

        self.xdim, self.ydim = 500, 500
        self.dim = max(self.xdim, self.ydim)

        self.fig1 = figure(title='Stable Diffusion',
                      x_range=(0, self.dim), y_range=(0, self.dim),
                      tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save'
                      )
        # self.fig1.image_rgba(image='image', x=0, y=0, dw=self.xdim, dh=self.ydim, source=self.source)
        ### end txt2img section ###

        # img2img section ###
        self.fig2 = figure(title='Stable Diffusion',
                      x_range=(0, self.dim), y_range=(0, self.dim),
                      tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save'
                      )
        # self.fig2.image_rgba(image='image', x=0, y=0, dw=self.xdim, dh=self.ydim, source=self.source)
        ### end img2img section ###
        self.select = Select(title="Image:", value='Select input folder', options=['Select input folder', 'Select output folder'])
        # self.select.on_change('value', self.update_on_select)

        # File input
        self.file_input = FileInput(accept=".png")
        self.file_input.on_change('value', self.import_file)

        # prompt input
        self.prompt_input = TextAreaInput(value="prompt here", rows=5, title="Text:")
        self.txt2img_button = Button(label="Generate", button_type="success")
        self.txt2img_button.on_click(self.txt2img_button_handler)

        self.img2img_button = Button(label="Generate", button_type="success")
        self.img2img_button.on_click(self.img2img_button_handler)

        # Sliders
        self.slider_ddim_eta = Slider(start=0.0, end=1.0, value=0.0,
                                 step=0.01, title="ddim_eta")
        self.slider_ddim_steps = Slider(start=0, end=500, value=1,
                                   step=1, title="ddim_steps")
        self.slider_scale = Slider(start=1.0, end=10.0, value=7.5, step=0.1, title="scale")
        self.slider_n_samples = Slider(start=1, end=10, value=2, step=1, title="n_samples")
        self.slider_n_iter = Slider(start=1, end=10, value=1, step=1, title="n_iter")
        self.slider_W = Slider(start=0, end=1024, value=512, step=32, title="W")
        self.slider_H = Slider(start=0, end=1024, value=512, step=32, title="H")
        self.slider_strength = Slider(start=0.0, end=1.0, value=0.5,
                                 step=0.01, title="strength")
        self.layout_slider = column(self.slider_ddim_eta, self.slider_ddim_steps, self.slider_scale,
                               self.slider_n_samples, self.slider_n_iter, self.slider_W, self.slider_H, self.slider_strength)
        self.txt2img_layout = row(column(self.fig1, self.select), column(
            self.prompt_input, self.txt2img_button, self.layout_slider))
        self.txt2img_tab = Panel(child=self.txt2img_layout, title='Text to Image')

        # img2img
        self.img2img_layout = row(column(self.fig1, self.select, self.file_input), column(
            self.prompt_input, self.img2img_button, self.layout_slider), column(self.fig2))
        self.img2img_tab = Panel(child=self.img2img_layout, title='Image to Image')

        # tab it
        self.tabs = Tabs(tabs=[self.txt2img_tab, self.img2img_tab])

        curdoc().add_root(self.tabs)

    def update_on_select(self, attr, old, new):
        image = Image.open(new).convert('RGBA')
        img, view, xdim, ydim = image_array(image)
        self.source.data = dict(image=[img])

    def import_file(self, attr, old, new):
        image = Image.open(new).convert('RGBA')
        img, view, xdim, ydim = image_array(image)
        self.source.data = dict(image=[img])


    def get_parameter_values(self):
        parameter_dict = {
            'prompt': self.prompt_input.value,
            'ddim_eta': self.slider_ddim_eta.value,
            'ddim_steps': self.slider_ddim_steps.value,
            'scale': self.slider_scale.value,
            'n_samples': self.slider_n_samples.value,
            'n_iter': self.slider_n_iter.value,
            'W': self.slider_W.value,
            'H': self.slider_H.value,
            'strength': self.slider_strength.value
        }
        return parameter_dict

    def txt2img_button_handler(self):
        self.parameter_dict = self.get_parameter_values()
        self.images_list = txt2img_helper(prompt=self.parameter_dict['prompt'], ddim_eta=self.parameter_dict['ddim_eta'],
                                ddim_steps=self.parameter_dict['ddim_steps'], scale=self.parameter_dict['scale'],
                                n_samples=self.parameter_dict['n_samples'], n_iter=self.parameter_dict['n_iter'],
                                W=self.parameter_dict['W'], H=self.parameter_dict['H'])

        self.fig1.image_rgba(image='image', x=0, y=0, dw=self.xdim, dh=self.ydim, source=self.source)
        self.fig1.image_rgba(image='image', x=0, y=0, dw=self.xdim, dh=self.ydim, source=self.source)

        self.active_image = self.images_list[0]
        self.update_image()

    def img2img_button_handler(self):
        self.parameter_dict = self.get_parameter_values()
        self.images_list = img2img_helper(prompt=self.parameter_dict['prompt'], ddim_eta=self.parameter_dict['ddim_eta'],
                                ddim_steps=self.parameter_dict['ddim_steps'], scale=self.parameter_dict['scale'],
                                n_samples=self.parameter_dict['n_samples'], n_iter=self.parameter_dict['n_iter'],
                                W=self.parameter_dict['W'], H=self.parameter_dict['H'], strength=self.parameter_dict['strength'])

        self.fig1.image_rgba(image='image', x=0, y=0, dw=self.xdim, dh=self.ydim, source=self.source)
        self.fig1.image_rgba(image='image', x=0, y=0, dw=self.xdim, dh=self.ydim, source=self.source)

        self.active_image = self.images_list[0]
        self.update_image()


    def update_image(self):

        self.select.options = self.images_list
        self.select.value = self.active_image

        image = Image.open(self.active_image).convert('RGBA')
        xdim, ydim = image.size
        print("Dimensions: ({xdim}, {ydim})".format(**locals()))
        # Create an array representation for the image `img`, and an 8-bit "4
        # layer/RGBA" version of it `view`.
        img = np.empty((ydim, xdim), dtype=np.uint32)
        view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
        # Copy the RGBA image into view, flipping it so it comes right-side up
        # with a lower-left origin
        view[:, :, :] = np.flipud(np.asarray(image))

        self.source.data = dict(image=[img])












# StableDiffusionBokehApp()



