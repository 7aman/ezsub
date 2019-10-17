#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

# package information (is filling from ezsub/const.py)
__version__ = ''
__author__ = ''
__contact__ = ''
__url__ = ''
__license__ = ''


# Get the information from ezsub/const.py without importing the package
exec(compile(open('ezsub/const.py').read(),
             'ezsub/const.py', 'exec'))

with open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ezsub',
    version=__version__,
    description='Download subtitle from subscene',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=__url__,
    author=__author__,
    author_email=__contact__,
    license=__license__,
    packages=['ezsub', 'ezsub.cli', 'ezsub.cli.commands'],
    entry_points={
        'console_scripts': ['ezsub = ezsub.cli:main'],
    },
    install_requires=[
        'bs4',
        'requests-futures',
        'rarfile'
    ],
    python_requires='>=3.7',
    zip_safe=False,
    keywords='subtitle movie subscene',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    project_urls={
        'source': __url__
    }
)
