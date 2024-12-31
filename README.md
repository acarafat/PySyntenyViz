# PySyntenyViz
A CLI to create and annotate synteny plots for microbial genomes or plasmids. It uses GenBank files as input and creates alignment on the fly. It provides additional tools to edit the GenBank files to customize the synteny plot.


# Requirement
`MUMmer` and/or `MMSeqs` should be installed to run the aligner.

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
Available commands: `synteny`, `revcomp`, `reorder`, `change_origin`

## Commands
- `synteny`: Generate synten plot
- `change_origin`: Change origin of a GenBank file
- `revcomp`: Reverse-complement particular contig or whole GenBank file sequence
- `reorder`: Reorder contigs of GenBakn file

## Getting help
Use `-h` or `--h` flag to get details of the command, i.e.: `synviz <command> --help` 


## Annotation options
There are two options for annotating the synteny plot. One option is by providing GenBank features, which will annotate the particular feature of interest based on its presence in the GenBank file. Another option is to provide exact coordinates, so that those coordinates will be annotated specifically.

## Examples
Read GenBank files as input from directory, plot Agrobacterium synteny with MMSeqs2 alignment and annotate by GenBank feature:
```
synviz synteny --input_dir agrobacterium --output agro_original.png --annotate annotate_synteny.tsv --alignment mmseqs
```

Use MUMmer alignment instead:
```
synviz synteny --input_dir agrobacterium --output agro_original.mummer.png --annotate annotate_synteny.tsv
```

Reverse-complement a contig and plot synteny, take input from a list:
```
synviz revcomp -i agrobacterium/47_2_polished_final_renamed.gbk -o agrobacterium/47_2_polished_final_renamed.rc.gbk -c chromosome
synviz synteny --input_list agrolist.txt --output agro_rc.mmseqs.png --alignment mmseqs --annotate annotate_synteny.tsv
```

Reorder contigs by custom-order and plot synteny:
```
grep "LOCUS" agrobacterium/47_2_polished_final_renamed.rc.gbk
synviz reorder --input agrobacterium/47_2_polished_final_renamed.rc.gbk --output agrobacterium/47_2_polished_final_renamed.rc.order.gbk --order chromosome chromid pTi plasmid1 plasmid2
grep "LOCUS" agrobacterium/47_2_polished_final_renamed.rc.order.gbk
```

Reorder contigs by size and plot synteny:
```
grep "LOCUS" agrobacterium/47_2_polished_final_renamed.rc.gbk
synviz reorder --input agrobacterium/47_2_polished_final_renamed.rc.gbk --output agrobacterium/47_2_polished_final_renamed.rc.order.gbk --by_size
grep "LOCUS" agrobacterium/47_2_polished_final_renamed.rc.order.gbk
```

Change contig origin in GenBank file and plot synteny:
```
synviz change_origin -i agrobacterium/47_2_polished_final_renamed.rc.order.gbk -o agrobacterium/47_2_polished_final_renamed.rc.order.origin.gbk --origin 346694 --contig chromosome_rc
synviz synteny --input_list agrolist.txt --output agro_rc.mmseqs.png --alignment mmseqs --annotate annotate_synteny.tsv
```

Annotate synteny with specific feature coordinates:
```
synviz synteny --input_list bradylist.txt --output brady_original.mmseqs.png --alignment mmseqs --coordinate coordinates.tsv
```
