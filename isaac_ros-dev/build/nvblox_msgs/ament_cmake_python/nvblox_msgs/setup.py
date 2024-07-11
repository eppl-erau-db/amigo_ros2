from setuptools import find_packages
from setuptools import setup

setup(
    name='nvblox_msgs',
    version='3.0.1',
    packages=find_packages(
        include=('nvblox_msgs', 'nvblox_msgs.*')),
)
