import base64
import io
import os
import sys
import time
import glob
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Button, Div, DataTable, TableColumn, NumberFormatter, FileInput, RangeSlider, Select
from bokeh.plotting import figure, show, output_file
from bokeh.models.widgets import Tabs, Panel

from PIL import Image


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


# get list of images
image_list = glob.glob('imgs/*.png')
image_list.sort()
images = [Image.open(x).convert('RGBA') for x in image_list]
image = images[0]

img, view, xdim, ydim = image_array(image)
source = ColumnDataSource(data=dict(image=[img]))

# Figure
dim = max(xdim, ydim)
fig = figure(title='Stable Diffusion',
             x_range=(0, dim), y_range=(0, dim),
             tools='pan,wheel_zoom,box_zoom,poly_draw,reset,save'
             )
fig.image_rgba(image='image', x=0, y=0, dw=xdim, dh=ydim, source=source)

# Select tool
select = Select(title="Image:", value=image_list[0], options=image_list)
select.on_change('value', update_image)

# File input
file_input = FileInput(accept=".png")
file_input.on_change('value', import_file)

curdoc().add_root(column(file_input, select, fig))
