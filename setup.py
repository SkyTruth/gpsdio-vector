#!/usr/bin/env python


"""
Setup script for gpsdio-vector-driver
"""


import os
from setuptools import setup
from setuptools import find_packages


with open('README.rst') as f:
    readme = f.read().strip()


with open('LICENSE.txt') as f:
    license = f.read().strip()


version = None
author = None
email = None
source = None
with open(os.path.join('gpsdio_vector_driver', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__author__'):
            author = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__email__'):
            email = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__source__'):
            source = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif None not in (version, author, email, source):
            break


setup(
    author=author,
    author_email=email,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
    ],
    description="A driver plugin for gpsdio that enable writing to a Fiona supported OGR layer.",
    entry_points='''
        [gpsdio.drivers]
        Vector=gpsdio_vector_driver.driver:Vector
    ''',
    extras_require={
        'test': ['pytest', 'pytest-cov']
    },
    include_package_data=True,
    install_requires=[
        'fiona>=1.2',
        'gpsdio>=0.0.4'
    ],
    keywords='AIS GIS remote sensing vector',
    license=license,
    long_description=readme,
    name='gpsdio-density',
    packages=find_packages(),
    url=source,
    version=version,
    zip_safe=True
)
