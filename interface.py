from optimizedSD.helper import txt2img_helper, img2img_helper
from PIL import Image
import bokeh
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, CustomJS, Slider, Button, Div, DataTable, TableColumn, NumberFormatter, FileInput, RangeSlider, Select, TextAreaInput, TextInput, ImageURL, ImageRGBA
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


class StableDiffusionBokehApp():
    def __init__(self):

        self.images_list = []
        self.active_image = None
        self.source = ColumnDataSource(data=dict(image=[]))

        self.xdim, self.ydim = 500, 500
        self.dim = max(self.xdim, self.ydim)

        # Figures
        self.fig1 = figure(title='Stable Diffusion',
                           x_range=(0, self.dim), y_range=(0, self.dim),
                           tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save'
                           )
        self.fig2 = figure(title='Stable Diffusion: img2img result',
                           x_range=(0, self.dim), y_range=(0, self.dim),
                           tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save'
                           )
        self.fig1.image_rgba(image='image', x=0, y=0,
                             dw=self.xdim, dh=self.ydim, source=self.source)
        self.fig2.image_rgba(image='image', x=0, y=0,
                             dw=self.xdim, dh=self.ydim, source=self.source)

               # File input
        self.file_input = FileInput(accept=".png")
        self.file_input.on_change('filename', self.import_file)

        # prompt input
        self.prompt_input = TextAreaInput(
            value="prompt here", rows=5, title="Text:")

        # Buttons
        self.txt2img_button = Button(label="txt2img", button_type="success")
        self.img2img_button = Button(label="img2img", button_type="success")

        # Button handlers
        self.txt2img_button.on_click(self.txt2img_button_handler)
        self.img2img_button.on_click(self.img2img_button_handler)

        # Sliders
        self.slider_ddim_eta = Slider(start=0.0, end=1.0, value=0.0,
                                      step=0.01, title="ddim_eta")
        self.slider_ddim_steps = Slider(start=0, end=500, value=1,
                                        step=1, title="ddim_steps")
        self.slider_scale = Slider(
            start=1.0, end=10.0, value=7.5, step=0.1, title="scale")
        self.slider_n_samples = Slider(
            start=1, end=100, value=10, step=1, title="n_samples")
        self.slider_n_iter = Slider(
            start=1, end=10, value=1, step=1, title="n_iter")
        self.slider_W = Slider(
            start=0, end=1024, value=512, step=32, title="W")
        self.slider_H = Slider(
            start=0, end=1024, value=512, step=32, title="H")
        self.slider_strength = Slider(start=0.0, end=1.0, value=0.5,
                                      step=0.01, title="strength")
        
        self.layout_slider = column(self.slider_ddim_eta, self.slider_ddim_steps, self.slider_scale,
                                    self.slider_n_samples, self.slider_n_iter, self.slider_W, self.slider_H, self.slider_strength)

        # Gallery
        self.gallery = figure(title='Gallery',
                              x_range=(0, self.dim), y_range=(0, self.dim),
                              tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save')
         # Select widgets
        self.select_active_image = Select(
            title="Active image:", value='Active image', options=['Active image'])
        self.select_active_image.on_change(
            'value', self.update_select_active_image_on_value_change)
        self.select_active_image.on_change(
            'options', self.update_select_active_image_on_options_change)

        self.gallery_options = glob.glob(
            '/home/os/gits/stable-diffusion-playground/output/*')
        self.select_gallery = Select(
            title="Gallery:", value=self.gallery_options[0], options=self.gallery_options)
        self.select_gallery.on_change(
            'value', self.update_select_gallery_on_new_value)


        # Layout
        # txt2img
        self.txt2img_layout = row(column(self.fig1, self.select_active_image), column(
            self.prompt_input, self.txt2img_button, self.layout_slider), column(self.gallery, self.select_gallery))
        self.txt2img_tab = Panel(
            child=self.txt2img_layout, title='Text to Image')

        # img2img
        self.img2img_layout = row(column(self.fig1, self.select_active_image, self.file_input), column(
            self.prompt_input, self.img2img_button, self.layout_slider), column(self.fig2))
        self.img2img_tab = Panel(
            child=self.img2img_layout, title='Image to Image')

        # tab it
        self.tabs = Tabs(tabs=[self.txt2img_tab, self.img2img_tab])

        self.doc = curdoc()
        self.doc.add_root(self.tabs)

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

    def image_array(self, image):
        xdim, ydim = image.size
        img = np.empty((ydim, xdim), dtype=np.uint32)
        view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
        view[:, :, :] = np.flipud(np.asarray(image))
        return img, view, xdim, ydim

    def img2img_button_handler(self):
        self.parameter_dict = self.get_parameter_values()
        self.images_list = img2img_helper(prompt=self.parameter_dict['prompt'], ddim_eta=self.parameter_dict['ddim_eta'],
                                          ddim_steps=self.parameter_dict['ddim_steps'], scale=self.parameter_dict['scale'],
                                          n_samples=self.parameter_dict['n_samples'], n_iter=self.parameter_dict['n_iter'],
                                          W=self.parameter_dict['W'], H=self.parameter_dict['H'], strength=self.parameter_dict['strength'], init_img=self.active_image)

        self.update_image()

    def txt2img_button_handler(self):
        self.parameter_dict = self.get_parameter_values()
        self.images_list = txt2img_helper(prompt=self.parameter_dict['prompt'], ddim_eta=self.parameter_dict['ddim_eta'],
                                          ddim_steps=self.parameter_dict['ddim_steps'], scale=self.parameter_dict['scale'],
                                          n_samples=self.parameter_dict['n_samples'], n_iter=self.parameter_dict['n_iter'],
                                          W=self.parameter_dict['W'], H=self.parameter_dict['H'])
        self.select_active_image.value = self.images_list[0]
        self.update_image()

    def update_image(self):
        image = Image.open(self.active_image).convert('RGBA')
        img, view, xdim, ydim = self.image_array(image)
        self.source.data = dict(image=[img])

    def update_select_active_image_on_options_change(self, attr, old, new):
        # self.select.options = self.images_list
        # self.populate_gallery_plot()
        # self.update_select_active_image_on_options_change()
        pass

    def update_select_active_image_on_value_change(self, attr, old, new):
        self.active_image = self.select_active_image.value
        self.select_active_image.options = self.images_list
        self.update_image()

    def update_select_gallery_on_new_value(self, attr, old, new):
        image_directory = self.select_gallery.value
        self.images_list = glob.glob(f'{image_directory}/*.png')

        self.select_active_image.options = self.images_list
        self.select_active_image.value = self.images_list[0]

        self.populate_gallery_plot()

    def populate_gallery_plot(self):
        for i, image_ in enumerate(self.images_list):
            img, view, xdim, ydim = self.image_array(
                Image.open(image_).convert('RGBA'))

            source = ColumnDataSource(data=dict(image=[img]))
            self.gallery.image_rgba(
                image='image', x=xdim*i, y=0, dw=xdim, dh=ydim, source=source)

            callback = CustomJS(
                args={'image': image_, 'select': self.select_active_image}, code="select.value = image")
            self.gallery.js_on_event('tap', callback)

            self.gallery.x_range.end = self.xdim * len(self.images_list)
            self.gallery.plot_height = ydim
            self.gallery.plot_width = self.xdim * len(self.images_list)

    def import_file(self, attr, old, new):
        pass
        # # fuck this, needed to change file_input to change on filename instead of value
        # filename = self.file_input.filename
        # file = io.BytesIO(base64.b64decode(self.file_input.value))

        # image = Image.open(file).convert('RGBA')
        # image.save(f'inputs/{filename}', 'png')

        # self.images_list = [f'inputs/{filename}']
        # self.update_image()
