"""termstac module."""

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

# Dev Requirements
extra_reqs = {
    "test": ["pytest", "pytest-cov"],
    "dev": ["pytest", "pytest-cov", "pre-commit"],
}


setup(
    name="termstac",
    version="0.1.0",
    description=u"An Awesome python module",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="An Awesome python module",
    author=u"",
    author_email="",
    url="",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pystac~=0.5.6',
        'termtables~=0.2.3',
        'pandas~=1.2.3',
        'plotext~=2.3.1'
    ],
    extras_require=extra_reqs,
    entry_points={"console_scripts": ["termstac = termstac.cli:cli"]},
)
