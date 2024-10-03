from setuptools import setup, find_packages

setup(
    name='mtopy',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mtopy=mtopy:mtopy',
        ],
    },
)
