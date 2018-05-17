#!/usr/bin/env python
"""
Example plugin for MultiQC, showing how to structure code
and plugin hooks to work effectively with the main MultiQC code.

For more information about MultiQC, see http://multiqc.info
"""

from setuptools import setup, find_packages

version = '0.1'

setup(
    name = 'multiqc_example_plugin',
    version = version,
    author = 'Phil Ewels',
    author_email = 'phil.ewels@scilifelab.se',
    description = "Example MultiQC plugin",
    long_description = __doc__,
    keywords = 'bioinformatics',
    url = 'https://github.com/MultiQC/example-plugin',
    download_url = 'https://github.com/MultiQC/example-plugin/releases',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'multiqc'
    ],
    entry_points = {
        'multiqc.modules.v1': [
            'my_example = example_plugin.modules.my_example:MultiqcModule',
        ],
        'multiqc.cli_options.v1': [
            'disable_plugin = example_plugin.cli:disable_plugin'
        ],
        'multiqc.hooks.v1': [
            'execution_start = example_plugin.custom_code:example_plugin_execution_start'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
