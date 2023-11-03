"""
File containing the required information to successfully build a python package
"""

import setuptools

with open("README.md", "r", encoding="utf-8", newline="\n") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tty_ov',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=[
        "colorama==0.4.6",
        "prettytable==3.9.0",
        "ask_question==1.2.4",
        "colourise-output==1.1.3",
        "prompt-toolkit==3.0.39"
    ],
    author="Henry Letellier",
    author_email="henrysoftwarehouse@protonmail.com",
    description="A module that emulates a few core functionalities of a tty (see the inner help for a list of functions).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hanra-s-work/tty_ov",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
