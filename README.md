# PySyntenyViz
A CLI to create and annotate synteny plots for microbial genomes or plasmids. It uses GenBank files as input and creates alignment on the fly. It provides additional tools to edit the GenBank files to customize the synteny plot.


# Requirement
`MUMmer` and/or `MMSeqs` should be installed to run the aligner.

# Installation
Install from PyPI
```
pip install PySyntenyViz
``` 

Install from source:
```
git clone https://github.com/acarafat/PySyntenyViz/
cd PySyntenyViz
pip install .
```

Alternatively to build and install from source using `pip wheel`:

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

## Generating Synteny with two different annotation options

![alt text](synteny_coords.png "Synteny with annotation by custom coordinates")

Input file `strainlist.txt`:
```
/path/to/Strain_1.gbk
/path/to/Strain_2.gbk
/path/to/Strain_3.gbk
```

Coordinate file for annotation using `--coordinate` flag: `coordinates.tsv`
| gbk       | locus     | label          | start  | end       | color   | strand | plotstyle |
|-----------|-----------|----------------|--------|-----------|---------|--------|-----------|
| Strain_1  | Contig_1  | nod            | 5413   | 14992     | blue    | 1      | box       |
| Strain_1  | Contig_1  | nif/fix        | 19407  | 42752     | magenta | 1      | box       |
| Strain_1  | Contig_1  | nif/fix        | 175637 | 187210    | magenta | 1      | box       |
| Strain_1  | Contig_1  | T4SS           | 357052 | 370816    | brown   | 1      | box       |
| Strain_1  | Contig_1  | bio            | 377557 | 381609    | black   | 1      | box       |
| Strain_1  | Contig_1  | pan            | 386274 | 387991    | black   | 1      | box       |
| Strain_1  | Contig_1  | nod            | 391054 | 393012    | blue    | 1      | box       |
| Strain_1  | Contig_1  | nif/fix        | 421473 | 429473    | magenta | 1      | box       |
| Strain_1  | Contig_1  | T4SS           | 557560 | 569180    | brown   | 1      | box       |
| Strain_2  | Contig_1  | nod            | 3972   | 9259      | blue    | 1      | box       |
| Strain_2  | Contig_1  | nif/fix        | 30871  | 44544     | magenta | 1      | box       |
| Strain_2  | Contig_1  | nif/fix        | 68132  | 84403     | magenta | 1      | box       |
| Strain_2  | Contig_1  | bio            | 297983 | 302023    | black   | 1      | box       |
| Strain_2  | Contig_1  | pan            | 306814 | 308405    | black   | 1      | box       |
| Strain_2  | Contig_1  | nif/fix        | 330400 | 338787    | magenta | 1      | box       |
| Strain_2  | Contig_1  | T4SS           | 392045 | 403669    | brown   | 1      | box       |
| Strain_3  | Contig_1  | nif/fix        | 479987 | 488559    | magenta | 1      | box       |
| Strain_3  | Contig_1  | T4SS           | 467546 | 479162    | brown   | 1      | box       |
| Strain_3  | Contig_1  | T4SS           | 429923 | 451808    | brown   | 1      | box       |
| Strain_3  | Contig_1  | nod            | 369759 | 373679    | blue    | 1      | box       |
| Strain_3  | Contig_1  | nod            | 357170 | 357766    | blue    | 1      | box       |
| Strain_3  | Contig_1  | nif/fix        | 157877 | 164992    | magenta | 1      | box       |
| Strain_3  | Contig_1  | nif/fix        | 108463 | 122788    | magenta | 1      | box       |
| Strain_3  | Contig_1  | bio            | 78637  | 84154     | black   | 1      | box       |
| Strain_3  | Contig_1  | nod            | 74067  | 77670     | blue    | 1      | box       |

Command for synteny plot:
```
synviz synteny --input_list strainlist.txt --output synteny_output.pdf --alignment mmseqs --coordinate coordinates.tsv
```


If you want to use feature types for generic annotation, use the `--annotate` flag and provide `annotation.tsv` file instead:
| feature_type   | qualifier           | value | face_color | label |
|----------------|---------------------|-------|------------|-------|
| CDS            | product             | bio   | black      | bio   |
| gene           | gene                | nif   | magenta    | nif   |
| gene           | gene                | nod   | magenta    | nod   |
| gene           | gene                | fix   | magenta    | fix   |
| mobile_element | mobile_element_type | T4SS  | brown      | ICE   |

Command:
```
synviz synteny --input_list strainlist.txt --output synteny_output.pdf --alignment mmseqs --annotate annotate.tsv
```

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
