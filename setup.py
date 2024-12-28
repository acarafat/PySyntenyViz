from setuptools import setup, find_packages

setup(
    name='PySyntenyViz',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'synviz=PySyntenyViz.cli:main',
        ],
    },
    install_requires=[
        'Bio', 'argparse', 'pandas', 'pygenomeviz'
    ]

)