from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pysmartlogger",
    version="1.3.0",
    author="Mohammad Rasol Esfandiari",
    author_email="mrasolesfandiari@gmail.com",
    description="A cross-platform Python library that adds colorful logging capabilities to the standard logging module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeepPythonist/smartlogger",
    project_urls={
        "Bug Tracker": "https://github.com/DeepPythonist/smartlogger/issues",
        "Documentation": "https://github.com/DeepPythonist/smartlogger/blob/master/README.md",
        "Source Code": "https://github.com/DeepPythonist/smartlogger",
        "Changelog": "https://github.com/DeepPythonist/smartlogger/blob/master/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",

        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Terminals",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    keywords="logging colors terminal cross-platform python ansi console",
    license="MIT",
) 