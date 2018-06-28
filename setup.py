#!/usr/bin/env python3
from setuptools import setup
version = '0.0.1'
setup(
    install_requires = ['aquachain.py'],
    name='aquachain-tk',
    url='https://github.com/aquachain/aquachain-tk',
    packages = ['aquachaintk'],
    version=version,
    scripts = ['AquaTK'],
    data_files = [('aquachaintk', ['aquachaintk/aquachain.png'])],
    include_package_data=True,
    description='Aquachain TK wallet for Python 3.6.5',
    long_description='Aquachain TK wallet for Python 3.6.5 -- See https://github.com/aquachain/aquachain.py or https://aquachain.github.io for more information.',
    author='Aquachain Authors',
    author_email='aquachain@riseup.net',
    license = 'GPL',
    test_suite='tests',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: Free for non-commercial use',
        'License :: OSI Approved :: GNU General Public License (GPL)',
	],
)
