from setuptools import setup

setup(
    name='telegraph',
    version='0.0.1',
    packages=['telegraph'],
    include_package_data=True,
    install_requires=[
        'requests==2.12.4'
    ],
)