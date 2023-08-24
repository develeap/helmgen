from __future__ import absolute_import


__project__      = 'helmgen'
__version__      = '0.0.1'
__keywords__     = ['helmgen', 'helm gen tools', 'tools']
__author__       = 'develeap'
__author_email__ = 'kfir.bekhavod@develeap.com'
__url__          = 'https://develeap.com'
__platforms__    = 'ALL'

__classifiers__ = [
    "Development Status :: Production",
    "Topic :: Utilities",
    "Programming Language :: Python :: 3",
    "License :: NA :: NA",
]

__entry_points__ = {
    'console_scripts': [
        'helmgen = helmgen.helmgen:main',
    ],
}

__requires__ = [
    'click',
    'pyyaml',
    'requests',
    'GitPython'
]

__extra_requires__ = {
    'doc':   ['mkdocs'],
    'test':  ['pytest', 'coverage', 'tox'],
}
