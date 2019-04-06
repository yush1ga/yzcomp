import json
from setuptools import setup, find_packages

from yzcomp import __version__

with open('./Pipfile.lock') as f:
    install_requires = []
    for k, v in json.load(f).items():
        if k == 'default':
            for l, d in v.items():
                install_requires.append(l+d['version'])

setup(
    name='yzcomp',
    version=__version__,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        yzcomp=yzcomp:main
    ''',
)