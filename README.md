# stacterm

This library is for displaying information (tables, calendars, plots,
histograms) about [STAC](https://stacspec.org/) Items in the terminal. It takes
as input a STAC ItemCollection (a GeoJSON FeatureCollection of STAC Items),
either by specifying a filename or by piping output from another program.

## Installation

Install from PyPi:

```cmdline
❯ pip install stacterm
```

PySTAC and Pandas are required, along with two dependencies for rendering
tables ([termtables](https://pypi.org/project/termtables/)) and plots
([plotext](https://pypi.org/project/plotext/)) in the terminal.

## Usage

stacterm main usage is as a CLI progam `stacterm`. Use help to see options
available:

```cmdline
❯ stacterm -h
usage: stacterm [-h] {table,cal,hist,plot} ...

Terminal STAC

positional arguments:
  {table,cal,hist,plot}
    table               Output a table
    cal                 Output a calendar
    hist                Output a histogram
    plot                Output a plot

optional arguments:
  -h, --help            show this help message and exit
```

All of the sub-commands in `stacterm` can take optional field names. A field
name is:

- `id`: The ID of the Item
- `collection`: The collection of the Item
- Dates
  - `date`: The date portion of the Item's `datetime` field
  - `year-month`: The year and month of the Item's `datetime` field
  - `year`: The year of the Item's `datetime` field
- Any property

`stacterm` reads from in stdin allowing other programs to pipe output to it,
such as [pystac-client](https://github.com/stac-utils/pystac-client).

```cmdline
❯ export STAC_API_URL=https://earth-search.aws.element84.com/v0
❯ stac-client search --intersects aoi.json \
    --datetime 2020-07-01/2020-12-31 \
    -c sentinel-s2-l2a-cogs landsat-8-l1-c1 | stacterm cal --label platform
```

The detailed usage examples below are all shown using the item collection from
a search saved to a file and redirected to stdin.

![](images/cal.png)

### Tables

Use `stacterm` to display tabularized data from a saved ItemCollection.

```cmdline
❯ <input.json stacterm table

| id                                       | date       |
|------------------------------------------|------------|
| LC08_L1TP_026079_20201014_20201104_01_T1 | 2020-10-14 |
| LC08_L1TP_026079_20201115_20201210_01_T1 | 2020-11-15 |
| S2A_12JXQ_20201008_0_L1C                 | 2020-10-08 |
```

By default this is a markdown table (note the terminal will not render Markdown)

| id                                       | date       |
|------------------------------------------|------------|
| LC08_L1TP_026079_20201014_20201104_01_T1 | 2020-10-14 |
| LC08_L1TP_026079_20201115_20201210_01_T1 | 2020-11-15 |
| S2A_12JXQ_20201008_0_L1C                 | 2020-10-08 |

The fields displayed can be changed via the `--fields` keyword, and sorted via
the `--sort` keyword.

```cmdline
❯ <input.json stacterm table \
    --fields date eo:cloud_cover collection \
    --sort eo:cloud_cover

| date       | eo:cloud_cover | collection           |
|------------|----------------|----------------------|
| 2020-10-13 | 0.0            | sentinel-s2-l1c      |
| 2020-10-13 | 0.0            | sentinel-s2-l2a      |
| 2020-10-13 | 0.0            | sentinel-s2-l2a-cogs |
| 2020-10-13 | 0.0            | sentinel-s2-l1c      |
```

The style of the table can also be changed via the `--style` keyword, although
it will no longer be usable in a Markdown renderer. See [termtables
styles](https://github.com/nschloe/termtables/blob/master/termtables/styles.py)
for list of styles.

```cmdline
❯ <input.json stacterm table \
    --fields id date platform sentinel:grid_square\
    --sort date \
    --style thick

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ id                        ┃ date       ┃ platform    ┃ sentinel:grid_square ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━┫
┃ S2B_12JXR_20201003_0_L2A  ┃ 2020-10-03 ┃ sentinel-2b ┃ XR                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━┫
┃ S2B_12JXQ_20201003_0_L1C  ┃ 2020-10-03 ┃ sentinel-2b ┃ XQ                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━┫
┃ S2B_12JXQ_20201003_0_L2A  ┃ 2020-10-03 ┃ sentinel-2b ┃ XQ                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━┻━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━┛
```

### Calendars

A UNIX-like calendar (see [`cal`](https://en.wikipedia.org/wiki/Cal_(Unix))) is
available to show dates of individual items. By default `cal` will use the
field `datetime` (the collection datetime) and group Items by their Collection.
These can be overridden by the `--date_field` and `--label_field` keywords.
Note that the specified `--date_field` needs to be a date field, such as
`created` or `updated`.  `--label_field` will group and label items by the
provided field.

```cmdline
❯ <input.json stacterm cal --date_field created --label_field gsd
```

![](images/cal2.png)

### Histograms

Histograms can be created for any numeric field and `datetime` and `date` (just
the date portion of `datetime`). `created` and `updated` may also be specified
if available in all Items.

```cmdline
❯ <items.json stacterm hist eo:cloud_cover
```

![](images/hist.png)

### Plots

Plots can be created with a single numeric fields, a date field (`datetime`,
`date`, `created`, or `updated`) and a numeric field, or two numeric fields. If
a single field it will be plotted against the scene number. The `--sort`
keyword can control how to sort the data if plotting a single field.

```cmdline
❯ <input.json stacterm plot eo:cloud_cover --sort eo:cloud_cover
```

![](images/plot.png)

## Markers and Colors

For histograms and plots there are options for changing the marker (symbol) and
color of the plot, background, and text. These options all come directly from
[plotext](https://github.com/piccolomo/plotext).

In addition to a marker being able to be any single character, the following
names can also be provided for these symbols:

![](https://raw.githubusercontent.com/piccolomo/plotext/master/images/markers.png)

Color names can be provided as follows:

![](https://raw.githubusercontent.com/piccolomo/plotext/master/images/colors.png)

## Limitations

Currently any provided field must exist in all STAC Items.

## Development

There are a lot more options in the [plotext
library](https://github.com/piccolomo/plotext) that could be surfaced here.
Additionally, if [support for
datetimes](https://github.com/piccolomo/plotext/issues/7) in histograms and
plots is added, `stacterm` could create temporal histograms, or plot quantities
vs date.
