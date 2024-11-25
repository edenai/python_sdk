# my_sdk/setup.py

from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        requirements = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("--hash"):
                requirements.append(line.split(" ")[0])  # Take only the package name and version
    return requirements


setup(
    name="edenai_sdk",
    version="0.1.0a3",
    packages=find_packages(),
    author="Eden AI",
    author_email="contact@edenai.co",
    description="EdenAI SDK for python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/edenai/python_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=parse_requirements("./requirements.txt"),
)
