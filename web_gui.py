# display images from file system with bokeh

import os
import sys
import time
import glob
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Button, Div, DataTable, TableColumn, NumberFormatter
from bokeh.plotting import figure, show, output_file
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.widgets import TextInput, Select, CheckboxGroup, RadioGroup, Toggle, Paragraph, Div, Button, DataTable, TableColumn, NumberFormatter
from bokeh.models.widgets import CheckboxButtonGroup, RadioButtonGroup, MultiSelect, Select, AutocompleteInput, MultiChoice, CheckboxGroup, Toggle, Dropdown
from bokeh.models.widgets import Button, DataTable, TableColumn, NumberFormatter, Paragraph, Div, PreText, Select, MultiSelect, CheckboxGroup, CheckboxButtonGroup, RadioButtonGroup, Toggle, Dropdown, AutocompleteInput, MultiChoice, TextInput

from PIL import Image

# get list of images
image_list = glob.glob('imgs/*.png')
images = [Image.open(x).convert('RGBA') for x in image_list]

image =images[0]
xdim, ydim = image.size
print("Dimensions: ({xdim}, {ydim})".format(**locals()))

# Create an array representation for the image `img`, and an 8-bit "4
# layer/RGBA" version of it `view`.
img = np.empty((ydim, xdim), dtype=np.uint32)
view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))

# Copy the RGBA image into view, flipping it so it comes right-side up
# with a lower-left origin
view[:,:,:] = np.flipud(np.asarray(image))

# Display the 32-bit RGBA image
dim = max(xdim, ydim)
fig = figure(title="Lena",
             x_range=(0,dim), y_range=(0,dim),
             # Specifying xdim/ydim isn't quire right :-(
             # width=xdim, height=ydim,
             )

source = ColumnDataSource(data=dict(image=[img]))
fig.image_rgba(image='image', x=0, y=0, dw=xdim, dh=ydim, source=source)

select = Select(title="Image:", value=image_list[0], options=image_list)

def update_image(attrname, old, new):
    image = Image.open(select.value).convert('RGBA')
    xdim, ydim = image.size
    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
    view[:,:,:] = np.flipud(np.asarray(image))
    source.data = dict(image=[img])
select.on_change('value', update_image)

curdoc().add_root(column(select, fig))
