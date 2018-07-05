# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

from setuptools import setup, find_packages
import ricohcloudsdk

setup(
    name='ricoh-cloud-sdk',
    version=ricohcloudsdk.__version__,
    description='RICOH Cloud SDK for Python',
    long_description="""RICOH Cloud SDK for Python""",
    author='Ricoh Co., Ltd.',
    url='https://github.com/ricohapi/ricoh-cloud-sdk-python',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pillow',
        'requests'
    ],
    setup_requires=[
        'pytest-runner',
        'pytest-html'
    ],
    tests_require=[
        'pytest-cov',
        'mock',
        'pytest'
    ]
)
