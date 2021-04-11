import argparse
import json
import os
import sys

import pandas as pd
import plotext as plt
from pystac import ItemCollection
import termtables as tt
import termplotlib as tpl

from . import __version__
from .calendar import print_labeled_calendar


API_URL = os.getenv('STAC_API_URL', None)


def items_to_dataframe(item_collection, sort=None):
    _items = []
    for item in item_collection:
        _items.append({
            "id": item.id,
            "collection": item.collection_id,
            "date": item.datetime.date(),
            **item.to_dict()['properties']
        })
    df = pd.DataFrame(_items)
    if sort is not None:
        df.sort_values(sort, inplace=True)
    return df


def table(items, fields=['date', 'id'], sort=None, style='markdown'):
    _sort = fields[0] if sort is None else sort
    df = items_to_dataframe(items, sort=_sort)
    data = df[fields].values
    tt.print(data, header=fields, style=eval(f"tt.styles.{style}"))


def plot(items, x, y, sort=None, line=False):
    df = items_to_dataframe(items, sort=sort)
    #df.sort_values(x, inplace=True)
    if line:
        plt.plot(df[x])
    else:
        plt.scatter(df[x])
    plt.show()
    #fig = tpl.figure(padding=1)
    #fig.plot(df[x], df[y], title=y, plot_command="plot '-' w points")
    #fig.show()


def histogram(items, field, bins=100):
    df = items_to_dataframe(items)
    plt.clp()
    plt.hist(df[field].values, bins, label=field)
    plt.show()
    #counts = df[field].value_counts()

    #fig = tpl.figure(padding=1)
    #fig.hist(counts.values, counts.index.tolist(), force_ascii=False, bins=100)
    #fig.show()


def calendar(items, date_field='date', label_field='collection'):
    df = items_to_dataframe(items)
    # get dictionary of dates and values containing the group names
    df1 = df[[date_field, label_field]]
    df1[date_field] = pd.to_datetime(df1[date_field]).dt.date
    events = df1.groupby(date_field)[label_field].unique()
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
    parser.add_argument('y', help='Field for y value')
    parser.add_argument('--sort', help='Field to sort by', default=None)
    parser.add_argument('--line', help='Plot as line', default=False, action='store_true')

    parsed_args = {k: v for k, v in vars(parser0.parse_args(args)).items() if v is not None}
    if not sys.stdin.isatty():
        parsed_args['items'] = ItemCollection.from_dict(json.load(parsed_args['items']))        
    elif os.path.exists(parsed_args['items']):
        parsed_args['items'] = ItemCollection.from_file(parsed_args['items'])
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
