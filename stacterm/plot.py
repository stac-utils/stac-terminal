import plotext as plt

from .utils import DATE_FIELDS, items_to_dataframe


def print_plot(items, x, y=None, sort=None, fillx=False, 
               marker=None, color=None, background_color=None, text_color=None):
    df = items_to_dataframe(items, sort=sort)
    x_list = df[x].tolist()
    y_list = df[y].tolist() if y else None
    _x = df['timestamp'].tolist() if x in DATE_FIELDS else df[x]

    if y is None:
        plt.scatter(_x, marker=marker, color=color, fillx=fillx)
    else:
        plt.plot(_x, y_list, marker=marker, color=color, fillx=fillx)
        plt.xticks(_x, x_list)

    if background_color is not None:
        plt.canvas_color(background_color)
        plt.axes_color(background_color)
    if text_color is not None:
        plt.ticks_color(text_color)

    plt.show()
