import argparse
import json
import os
import sys

import pandas as pd
import plotext as plt
import termtables as tt

from . import __version__
from .calendar import print_labeled_calendar
from .utils import items_to_dataframe


API_URL = os.getenv('STAC_API_URL', None)


def table(items, fields=['date', 'id'], sort=None, style='markdown'):
    _sort = fields[0] if sort is None else sort
    df = items_to_dataframe(items, sort=_sort)
    data = df[fields].values
    tt.print(data, header=fields, style=eval(f"tt.styles.{style}"))


def plot(items, x, y=None, sort=None, line=False):
    df = items_to_dataframe(items, sort=sort)
    if line:
        if y is None:
            plt.plot(df[x])
        else:
            plt.plot(df[x], df[y])
    else:
        if y is None:
            plt.scatter(df[x])
        else:
            plt.plot(df[x], df[y])
    plt.show()


def histogram(items, field, bins=100):
    df = items_to_dataframe(items)
    plt.clp()
    plt.hist(df[field].values, bins, label=field)
    plt.show()


def calendar(items, date_field='date', label_field='collection'):
    df = items_to_dataframe(items)
    df.loc[date_field] = pd.to_datetime(df[date_field]).dt.date

    events = df.groupby(date_field)[label_field].unique()
    events = events.map(lambda x: x[0] if len(x) == 1 else "Multiple")
    print_labeled_calendar(events.to_dict(), label_field=label_field)


def parse_args(args):
    desc = 'Terminal STAC'
    dhf = argparse.ArgumentDefaultsHelpFormatter
    parser0 = argparse.ArgumentParser(description=desc, formatter_class=dhf)

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--version', help='Print version and exit', action='version', version=__version__)
    parent.add_argument('items', nargs='?', default=sys.stdin)

    subparsers = parser0.add_subparsers(dest='command')

    # table command
    parser = subparsers.add_parser('table', help='Output a table', parents=[parent], formatter_class=dhf)
    parser.add_argument('--fields', help='Fields to include in table', nargs='*', default=['id', 'date'])
    parser.add_argument('--sort', help='Field to sort by', default=None)
    parser.add_argument('--style', help='Output style', default='markdown')

    # calendar command
    parser = subparsers.add_parser('cal', help='Output a calendar', parents=[parent], formatter_class=dhf)
    parser.add_argument('--date-field', dest='date_field', help='Date field to use', default='date')
    parser.add_argument('--label-field', dest='label_field', help='Label field to use', default='collection')

    # histogram command
    parser = subparsers.add_parser('hist', help='Output a histogram', parents=[parent], formatter_class=dhf)
    parser.add_argument('field', help='Plot histogram of this quantity', default=None)

    # plot command
    parser = subparsers.add_parser('plot', help='Output a plot', parents=[parent], formatter_class=dhf)
    parser.add_argument('x', help='Field for x value')
    parser.add_argument('y', help='Field for y value', nargs='?', default=None)
    parser.add_argument('--sort', help='Field to sort by', default=None)
    parser.add_argument('--line', help='Plot as line', default=False, action='store_true')

    parsed_args = {k: v for k, v in vars(parser0.parse_args(args)).items() if v is not None}
    if not sys.stdin.isatty():
        parsed_args['items'] = json.load(parsed_args['items'])
    elif os.path.exists(parsed_args['items']):
        with open(parsed_args['items']) as f:
            parsed_args['items'] = json.loads(f.read())
    return parsed_args


def cli():
    args = parse_args(sys.argv[1:])

    cmd = args.pop('command')
    if cmd == 'table':
        table(**args)
    elif cmd == 'cal':
        calendar(**args)
    elif cmd == 'hist':
        histogram(**args)
    elif cmd == 'plot':
        plot(**args)


if __name__ == "__main__":
    cli()
