import plotext as plt

from .utils import DATE_FIELDS, items_to_dataframe


def print_histogram(items, field, bins=100):
    df = items_to_dataframe(items)
    plt.clp()

    data = df['timestamp'] if field in DATE_FIELDS else df[field]

    plt.hist(data.values, bins, label=field)
    plt.xticks(data.tolist(), df[field].tolist())
    plt.show()