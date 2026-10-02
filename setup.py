"""setup.py: setuptools control."""

from setuptools import setup, find_packages

__version__ = '2.4.0'

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
        'requests>=2.34.2'
    ],
    url='https://github.com/mine-your-business/myb-nicehash-api',
    python_requires='>=3.11',
    zip_safe=False,
    license_expression='GPL-3.0-only',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
