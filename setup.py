"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="atmscitools",
    version="2.000.0",
    description="Atmospheric Science Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ackermannluis/AtmSciTools",
    author="Luis Ackermann",
    author_email="ackermann.luis@gmail.com",  # Optional
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: Apache 2.0",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    package_data={'': ['*.nc','cdsapirc', '*.npy']},
    keywords="weather meteorology instrumentation",
    packages=find_packages(exclude=["contrib", "docs", "tests", "notebooks"]),
    install_requires=["scp", "xlrd", "imageio", "pyproj", "requests", "numpy", "netCDF4", "scipy",
                      "matplotlib", 'Pillow', 'pdf2image', 'pygrib'],
    project_urls={"Source": "https://github.com/ackermannluis/AtmSciTools/",},
)
