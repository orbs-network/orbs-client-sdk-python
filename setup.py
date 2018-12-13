#!/bin/env python3

from subprocess import run
from os import path
from setuptools import setup, Command


def read(file_name):
    return open(path.join(path.dirname(__file__), file_name)).read()


class TestCommand(Command):
    """Support 'setup.py test' command to retrieve the contract test files and run tests"""

    description = 'retrieves the codec contract test files from ' \
                  'https://github.com/orbs-network/orbs-client-sdk-go.git and run all tests including contract test'
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
        run(['./test.sh'])


class E2ECommand(Command):
    """Support 'setup.py test_e2e' command to run end to end tests"""

    description = 'run end to end tests'
    user_options = []

    # This method must be implemented
    def initialize_options(self):
        pass

    # This method must be implemented
    def finalize_options(self):
        pass

    def run(self):
        run(['./test_e2e.sh'])


setup(
    cmdclass={
        'test': TestCommand,
        'test_e2e': E2ECommand,
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
        'requests',
        'PyNaCl'
    ],
    url='https://github.com/orbs-network/orbs-client-sdk-python',
    python_requires='>=3.7.0',
    license='MIT'
)
