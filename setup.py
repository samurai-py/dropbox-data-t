from setuptools import setup, find_packages

setup(
    name='dropbox-data-merger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'dropbox>=11.36.0',
        'python-decouple>=3.8',
    ],
)