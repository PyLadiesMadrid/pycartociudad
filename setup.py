#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="PyLadies Madrid",
    author_email='madrid@pyladies.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="PyCartociudad contains Python functions to access the CartoCiudad REST and WPS API (REST y WPS) from IGN with spanish cartography services.",
    install_requires=['requests'],
    license='GPLv3+',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pycartociudad',
    name='pycartociudad',
    packages=find_packages(include=['pycartociudad', 'pycartociudad.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pyladiesmadrid/pycartociudad',
    version='0.1.0',
    zip_safe=False,
)
