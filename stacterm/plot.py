import plotext as plt

from .utils import DATE_FIELDS, items_to_dataframe


def print_plot(items, x, y=None, sort=None, marker=None, fillx=False):
    df = items_to_dataframe(items, sort=sort)
    x_list = df[x].tolist()
    y_list = df[y].tolist() if y else None
    _x = df['timestamp'].tolist() if x in DATE_FIELDS else df[x]

    if y is None:
        plt.scatter(_x, marker=marker, fillx=fillx)
    else:
        plt.plot(_x, y_list, marker=marker, fillx=fillx)
        plt.xticks(_x, x_list)

    plt.show()
