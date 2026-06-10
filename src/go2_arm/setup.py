import os
from glob import glob

from setuptools import find_packages, setup

package_name = "go2_arm"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "scripts"), glob(os.path.join("scripts", "*"))),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="brimo",
    maintainer_email="jcass358@gmail.com",
    description="CubeMars AK45 arm record/replay nodes for the Go2 (gs_usb CAN).",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "arm_replay_node = go2_arm.arm_replay_node:main",
            "arm_record = go2_arm.arm_record_node:main",
        ],
    },
)
