from setuptools import setup

with open(".../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='SMHM',
    version='0.1.0',
    description='Swiss Municipalities Historical Mapper',
    author='sondale-git',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url='https://github.com/sondale-git/SMHM',
    packages=['SMHM'],  #same as name
    package_dir={'':'src'},
    install_requires = ["pandas", "requests"], #external packages as dependencies
)
