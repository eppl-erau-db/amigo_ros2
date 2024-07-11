from setuptools import find_packages
from setuptools import setup

setup(
    name='isaac_ros_apriltag_interfaces',
    version='3.0.1',
    packages=find_packages(
        include=('isaac_ros_apriltag_interfaces', 'isaac_ros_apriltag_interfaces.*')),
)
