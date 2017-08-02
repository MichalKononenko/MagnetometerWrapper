# -*- coding: utf-8
"""
Contains python package metadata, allowing mr_freeze to be installed with pip
"""
from setuptools import setup, find_packages

setup(
    name="magnetometer_wrapper",
    version="1.0",
    description="Wraps serial communication to the Lakeshore 475 magnetometer",
    author="Michal Kononenko",
    author_email="mkononen@edu.uwaterloo.ca",
    url='https://github.com/MichalKononenko/MagnetometerWrapper',
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "pyserial==3.4"
    ]
)
