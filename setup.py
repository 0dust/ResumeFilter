import os
import ast
import pathlib
from io import open
import importlib.util
from setuptools import find_packages, setup

with open("README.md", "r") as f:
    README = f.read()



setup(
    name="ResumeFilter",
    description="Extract information from resume using Deep Learning",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Himanshu Tripathi",
    author_email="himanshutripathi366@gmail.com",
    maintainer="Himanshu Tripathi",
    maintainer_email="himanshutripathi366@gmail.com",
    url="https://github.com/0dust/ResumeFilter",
    license="MIT",
    keywords=[""],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires = ["tensorflow>=2.0.0", "python-docx>=0.8.10", "pdfminer>=20191125", "nltk>=3.5", "inflect>=4.1"],  
)