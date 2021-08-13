# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.2.0-rc.1] - 2021-08-13

### Added
- Date fields (`datetime`, `created`, `updated`) can now be used in histograms and plots (on x-axis)
- Derived date fields added to Item fields (`date`, `year`, `year-month`) for use in histograms and plots
- marker keyword added to plot for changing plot symbol
- `color`, `background_color`, `axes_color` options added to control color of histograms and plots
- `grid` option added to add x/y grid to histograms and plots
- fillx keyword added to plot to fill in region between data and x-axis

### Changed
- Updated plotext version
- Separated out CLI functionality into new modules: `histogram`, `plot`, `table`. (`calendar` was already a module)

## [v0.1.0] - 2021-04-16

Initial release.

[Unreleased]: <https://github.com/stac-utils/stac-terminal/compare/v0.2.0-rc.1...main>
[v0.2.0-rc.1]: <https://github.com/stac-utils/stac-terminal/compare/v0.1.0...v0.2.0-rc.1>
[v0.1.0]: <https://github.com/stac-utils/stac-terminal/tree/v0.1.0>
