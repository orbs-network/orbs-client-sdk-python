#!/bin/env python3

from subprocess import run
from os import path
from setuptools import setup, Command


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


class DevelopmentCommand(Command):
    """Support setup.py dev command to retrieve the contract test files"""

    description = 'retrieves the codec contract test files from the https://github.com/orbs-network/orbs-client-sdk-go.git repo'
    user_options = []

    # This method must be implemented
    def initialize_options(self):
        pass

    # This method must be implemented
    def finalize_options(self):
        pass

    def run(self):
        run(['rm', '-rf', './contract'])
        run(['git', 'clone', 'https://github.com/orbs-network/orbs-client-sdk-go.git', './contract'])


setup(
    cmdclass={
        'dev': DevelopmentCommand,
    },
    include_package_data=True,
    name='orbs-client-sdk',
    version='0.0.1',
    description='Orbs Client SDK',
    long_description=read('README.md'),
    author='Orbs Team',
    packages=['orbs_client'],
    install_requires=[
        'securesystemslib',
        'base58',
        'requests'
    ],
    url='https://github.com/orbs-network/orbs-client-sdk-python',
    python_requires='>=3.6.0',
    license='MIT'
)
