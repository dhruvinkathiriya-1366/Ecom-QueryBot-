import os
from setuptools import find_packages, setup

current_directory = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(current_directory, "requirements.txt")

with open(requirements_path) as f:
    required_packages = f.read().splitlines()

setup(
    name="Ecom-QueryBot",
    version="0.1.0",
    author="Dhruvin Kathiriya",
    description="Ecom QueryBot Multi-Module Project",
    packages=find_packages(include=["src", "src.*"]),
    install_requires=required_packages,
)