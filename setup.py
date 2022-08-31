import pathlib

from setuptools import find_packages, setup

with open(pathlib.Path(__file__).parent / "requirements/base.txt") as i:
    requirements = i.read().strip().splitlines()


setup(
    name="normalise-email",
    version="0.1.1",
    author="PsypherPunk",
    author_email="psypherpunk+github@gmail.com",
    packages=find_packages(include=("normalise.*",)),
    url="https://github.com/PsypherPunk/py-normalise-email",
    description="Python port of normalizeEmail.js.",
    long_description=open("README.md").read(),
    install_requires=[r.split("==")[0] for r in requirements],
    include_package_data=True,
)
