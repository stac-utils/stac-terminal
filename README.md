# termstac

This library is for displaying information (calendars, plots, histograms) about STAC Items in the terminal. It takes as input a STAC ItemCollection (a GeoJSON FeatureCollection of STAC Items), either by specifying a filename or by piping output from another program (such as [pystac-api-client](https://github.com/stac-utils/pystac-api-client)).

## Installation

Install from PyPi:

```
$ pip install termstac
```

PySTAC and Pandas are required, along with a couple small dependencies for rendering tables and plots in the terminal,

## Usage

Use `termstac` to display info from a saved file.

```
$ termstac table items.json
```

