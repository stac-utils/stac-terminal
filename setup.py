"""stacterm module."""

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()


setup(
    name="stacterm",
    version="0.2.0-rc.1",
    description="STAC Items in the terminal",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="An Awesome python module",
    author=u"Matthew Hanson",
    author_email="matt.a.hanson@gmail.com",
    url="https://github.com/stac-utils/stac-terminal",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pandas~=1.2",
        "termtables~=0.2",
        "plotext~=3.1"
    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "dev": ["pytest", "pytest-cov", "pre-commit"],
    },
    entry_points={"console_scripts": ["stacterm = stacterm.cli:cli"]},
)
