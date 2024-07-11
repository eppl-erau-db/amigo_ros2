from setuptools import find_packages
from setuptools import setup

setup(
    name='unitree_go',
    version='0.0.0',
    packages=find_packages(
        include=('unitree_go', 'unitree_go.*')),
)
