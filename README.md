# PySyntenyViz
A CLI to create synteny plots for small genomes or plasmids. 

# Requirement
`MUMmer`, `Blast`, and `MMSeqs`

# Installation
Releasing to PyPi soon.
To build and install from local: use `pip wheel`:

```
pip install wheel
git clone https://github.com/acarafat/PySyntenyViz/
cd PySyntenyViz
python3 setup.py sdist bdist_wheel
pip install dist/bioinfutils-0.1.0-py3-none-any.whl --force-reinstall
```

## Usage
```
synviz <command> [<args>]
```
Available commands: synteny, revcomp, reorder, change_origin

## Tools:
- `synteny`: Generate synten plot
- `change_origin`: Change origin of a GenBank file
- `revcomp`: Reverse-complement particular contig or whole GenBank file sequence
- `reorder`: Reorder contigs of GenBakn file

## Getting help
Use `-h` or `--h` flag to get details of the command, i.e.: `synviz <command> --help` 

