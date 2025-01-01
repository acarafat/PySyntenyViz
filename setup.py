from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='PySyntenyViz',
    version='0.1.0',
    packages=find_packages(),
    author = "Arafat Rahman",
    author_email = "ac.arafat@gmail.com",
    description = "A CLI to create and annotate synteny plots for microbial genomes or plasmids. It uses GenBank files as input and creates alignment on the fly. It provides additional tools to edit the GenBank files to customize the synteny plot.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/acarafat/PySyntenyViz",
    entry_points={
        'console_scripts': [
            'synviz=PySyntenyViz.cli:main',
        ],
    },
    install_requires=[
        'biopython', 'argparse', 'pandas', 'pygenomeviz'
    ]

)