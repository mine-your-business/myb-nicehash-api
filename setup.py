"""setup.py: setuptools control."""

from setuptools import setup, find_packages

__version__ = '1.1.0'

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='myb-nicehash-api',
    author='Mine Your Business',
    author_email='mine.your.business.crypto@gmail.com',
    packages=find_packages(exclude=("tests",)),
    version=__version__,
    description='Python library for communicating with the NiceHash API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.25.1'
    ],
    url='https://github.com/mine-your-business/myb-nicehash-api',
    python_requires='>=3.7',
    zip_safe=False,
    license='GPL-3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
