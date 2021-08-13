import plotext as plt

from .utils import DATE_FIELDS, items_to_dataframe


def print_plot(items, x, y=None, sort=None, line=False):
    df = items_to_dataframe(items, sort=sort)
    x_list = df[x].tolist()
    y_list = df[y].tolist() if y else None
    _x = df['timestamp'].tolist() if x in DATE_FIELDS else df[x]

    if line:
        if y is None:
            plt.scatter(_x)
        else:
            plt.plot(_x, y_list)
            plt.xticks(_x, x)
    else:
        if y is None:
            plt.scatter(_x)
        else:
            plt.plot(_x, y_list)
            plt.xticks(_x, x_list)
    plt.show()