#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='h5cluster',
    version='0.2.3',
    author="Steven Varga",
    author_email='steven@vargaconsulting.ca',
    description="AWS EC2 cluster controller for HPC solutions with HDF5 middleware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/steven-varga/h5cluster',
    license='MIT',
    scripts=['bin/h5cluster'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.4',
    include_package_data=True,
    keywords='cluster',
    packages=setuptools.find_packages(),
    project_urls={
        "Documentation": "http://h5cluster.ca/docs",
    }
)
