import plotext as plt

from .utils import DATE_FIELDS, items_to_dataframe


def print_histogram(items, field, bins=100,
                    marker='big', color=None, background_color=None, text_color=None):
    df = items_to_dataframe(items)
    plt.clp()

    data = df['timestamp'] if field in DATE_FIELDS else df[field]

    plt.hist(data.values, bins, label=field, marker=marker, color=color)
    plt.xticks(data.tolist(), df[field].tolist())

    if background_color is not None:
        plt.canvas_color(background_color)
        plt.axes_color(background_color)
    if text_color is not None:
        plt.ticks_color(text_color)

    plt.show()
