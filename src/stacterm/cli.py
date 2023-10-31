import argparse
import json
import sys

from .calendar import print_calendar
from .histogram import print_histogram
from .plot import print_plot
from .table import print_table
from .version import __version__


def parse_args(args):
    desc = "Terminal STAC"
    dhf = argparse.ArgumentDefaultsHelpFormatter
    parser0 = argparse.ArgumentParser(description=desc, formatter_class=dhf)

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument(
        "--version",
        help="Print version and exit",
        action="version",
        version=__version__,
    )

    subparsers = parser0.add_subparsers(dest="command")

    # table command
    parser = subparsers.add_parser(
        "table", help="Output a table", parents=[parent], formatter_class=dhf
    )
    parser.add_argument(
        "--fields", help="Fields to include in table", nargs="*", default=["id", "date"]
    )
    parser.add_argument("--sort", help="Field to sort by", default=None)
    parser.add_argument("--style", help="Output style", default="markdown")

    # calendar command
    parser = subparsers.add_parser(
        "cal", help="Output a calendar", parents=[parent], formatter_class=dhf
    )
    parser.add_argument(
        "--date-field", dest="date_field", help="Date field to use", default="date"
    )
    parser.add_argument(
        "--label-field",
        dest="label_field",
        help="Label field to use",
        default="collection",
    )

    # common plotting arguments
    plot_parser = argparse.ArgumentParser(add_help=False)
    plot_parser.add_argument("--title", help="Add plot title")
    plot_parser.add_argument("--marker", help="Use this character as a plot marker")
    plot_parser.add_argument("--color", help="Use this color for the plot markers")
    plot_parser.add_argument(
        "--background-color",
        dest="background_color",
        help="Use this color for background",
    )
    plot_parser.add_argument(
        "--axes-color", dest="axes_color", help="Use this color for axes text"
    )
    plot_parser.add_argument(
        "--grid", help="Add x/y grid to plot", default=False, action="store_true"
    )

    # histogram command
    parser = subparsers.add_parser(
        "hist",
        help="Output a histogram",
        parents=[parent, plot_parser],
        formatter_class=dhf,
    )
    parser.add_argument("field", help="Plot histogram of this quantity", default=None)

    # plot command
    parser = subparsers.add_parser(
        "plot", help="Output a plot", parents=[parent, plot_parser], formatter_class=dhf
    )
    parser.add_argument("x", help="Field for x value")
    parser.add_argument("y", help="Field for y value", nargs="?", default=None)
    parser.add_argument("--sort", help="Field to sort by", default=None)
    parser.add_argument(
        "--fillx",
        help="Fills the area between data and x axis",
        default=False,
        action="store_true",
    )

    parsed_args = {
        k: v for k, v in vars(parser0.parse_args(args)).items() if v is not None
    }
    parsed_args["items"] = json.load(sys.stdin)
    return parsed_args


def cli():
    args = parse_args(sys.argv[1:])

    cmd = args.pop("command")
    if cmd == "table":
        print_table(**args)
    elif cmd == "cal":
        print_calendar(**args)
    elif cmd == "hist":
        print_histogram(**args)
    elif cmd == "plot":
        print_plot(**args)


if __name__ == "__main__":
    cli()
