from bokeh import events
from bokeh.io import curdoc,show
from bokeh.layouts import column
from bokeh.models import Button as Button

def button_handler():
    print("Button was clicked!")


css = """
.btn-custom > .bk-btn-group > .bk-btn {
    background-image: url(https://previews.123rf.com/images/hemantraval/hemantraval1206/hemantraval120600022/13975128-glassy-aqua-blue-next-icon-button.jpg);
    background-repeat: no-repeat;
    background-size: contain;
    background-position: center;
}
"""
# button = Button(label="Click me", button_type="success", css_classes=["btn-custom"])
button = Button(name='', css_classes=['btn-custom'], width=50, height=50)
button.extension(raw_css=[css])

show(button)
