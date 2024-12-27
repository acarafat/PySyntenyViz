#!/bin/python3

import os, sys
import csv

import argparse

from pygenomeviz import  GenomeViz
from pygenomeviz.parser import Genbank
from pygenomeviz.align import MUMmer, MMseqs


# Get absulate paths of GBK files in a directory
def get_gbk_path(path_to_gbk):
    '''
    INPUT: A directory containing genbank as input for synteny plotting
    OUTPUT: List of parsed genback file as Genbank object, sorted alphabetically.
    '''
    root, _, files = next(os.walk(path_to_gbk, topdown=True))

    gbk_files = [ os.path.abspath(os.path.join(root, f)) for f in files ]

    gbk_list = [Genbank(f) for f in gbk_files]
    gbk_list.sort(key=lambda x: x.full_genome_length)

    return gbk_list


# Given a text file containing gbk paths
def get_gbk_file(gbk_path_file):
    '''
    INPUT: A textfile containing genbank as input for synteny plotting
    OUTPUT: List of parsed genback file as Genbank object.
    '''
    with open(gbk_path_file) as handle:
        gbk_files = handle.read().splitlines()

    gbk_list = [Genbank(f) for f in gbk_files]

    return gbk_list


# Parse annotation meta file
def load_face_colors(file_path):
    '''
    INPUT: Annotation tsv file which should have `feature_type`, `qualifier`, `value`, `label`, and `face_color`.
    OUTPUT: Parse the file as dictionary
    '''
    face_colors = []
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            face_colors.append(row)

    return face_colors

# Given a paritcular feature, define it's face color and label based on face_color_dict
def parse_feature_fc(feature, face_color_dict):
    '''
    INPUT: A feature and face_color_dict with feature_type, qualifier, value, label, and face_color.
    OUTPUT: Based on SeqFeature type, returns a specific color to be used as face-color
    '''
    # Set default
    fc = "ivory"
    f_lab = ''

    for entry in face_color_dict:
        if feature.type == entry['feature_type']:
            qualifier = entry['qualifier']
            if qualifier in feature.qualifiers:
                if feature.qualifiers[qualifier][0] == entry['value']:
                    fc = entry['face_color']
                    f_lab = entry['label']
                    break
    return fc, f_lab


# Plot synteny
def plot_synteny(gbk_list, output_png, annotate_file=None, coordinate_file=None, alignment=None):
    '''
    INPUT: A list contianing parsed Genbank objects and A list of pairwise coordinates of Mummer alignment
    OUTPUT: It plots the synteny plot. Nothing returns in output.
    '''
    ########################
    # Set GenomeViz object #
    ########################
    gv = GenomeViz(fig_track_height=1,
                   feature_track_ratio=0.2,
                   #tick_track_ratio=0.4,
                   #tick_style="bar",
                   #align_type="center",
                   )

    if annotate_file != None:
        fc_dict = load_face_colors(annotate_file)
    if coordinate_file != None:
        coord_dict = load_face_colors(coordinate_file)

    #############################
    # Plot contigs and features #
    ############################# 
    for gbk in gbk_list:
        track = gv.add_feature_track(gbk.name, gbk.get_seqid2size())

        # Make sure all GenBank locus has `source` feature
        gbk_f_types = set()
        for rec in gbk.records:
            gbk_f_types.update(set(f.type for f in rec.features))
            if "source" not in gbk_f_types:
                sys.exit(f"Error: Make sure {rec.id} in {gbk.name} has `source` feature!")

        # Plot individual contigs.
        for seqid, features in gbk.get_seqid2features(feature_type = 'source').items():
            segment = track.get_segment(seqid)
            segment.add_features(features, fc="skyblue", lw=0.5, label_handler=lambda s: str(seqid))

            # Plot target features based on the coordinate tsv file, if provided
            if annotate_file == None and coordinate_file != None:
                for entry in coord_dict:
                    if entry['gbk'] == gbk.name and entry['locus'] == str(seqid):
                        segment.add_feature(int(entry['start']), int(entry['end']), int(entry['strand']), 
                                            fc = entry['color'], label = entry['label'], plotstyle=entry['plotstyle'])
        
        # Remove `source`
        gbk_f_types.remove("source")

        ########################
        # Plot target features #
        ########################
        # Plot based on the feature annotation tsv file
        for seqid, features in gbk.get_seqid2features(feature_type = gbk_f_types).items():
             for f in features:
                if annotate_file != None and coordinate_file == None:
                    face_color, f_lab = parse_feature_fc(f, fc_dict)
                    if f_lab != '':
                        segment = track.get_segment(seqid)
                        # Add features to the segment with dynamic face color
                        segment.add_features(f, fc=face_color, lw=0.5, plotstyle='rbox', label_handler = lambda s: f_lab)
                else:
                    face_color = 'ivory'
                    f_lab = ''

    #############
    # Alignment #
    #############
    if alignment in ["mummer", None]:
        print('Creating MUMmer alignment ...')
        align_coords = MUMmer(gbk_list).run()
        
    elif alignment == "mmseqs":
        print('Creating MMseqs alignment ...')
        align_coords = MMseqs(gbk_list).run()

    #######################################
    # Plot MUMmer/MMseqs RBH search links #
    #######################################
    print('Plotting synteny ...')
    if len(align_coords) > 0:
        min_ident = int(min([ac.identity for ac in align_coords if ac.identity]))
        color, inverted_color = "chocolate", "limegreen"
        for ac in align_coords:
            gv.add_link(ac.query_link, ac.ref_link, color=color, inverted_color=inverted_color, v=ac.identity, vmin=min_ident, curve=True)
        gv.set_colorbar([color, inverted_color], vmin=min_ident)

    fig = gv.plotfig()
    fig.savefig(f"{output_png}")


# Parse input, program logic-flow
def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_dir', '-i', type=str, required=False, help="Path to directory containing GenBank files")
    parser.add_argument('--input_list', type=str, required=False, help="Textfile containing paths of GenBank files seperated by lines. The order of GenBank files will be used to plot.")
    parser.add_argument('--output', '-o', type=str, required=True, help="Output image file. Use .png/.pdf etc. extensions for desiarable format.")
    parser.add_argument('--annotate', '-a', type=str, required=False, help="Sequence features from GenBank file to annotate.")
    parser.add_argument('--coordinate', '-c', type=str, required=False, help="Coordinate position from GenBank file to annotate.")
    parser.add_argument('--alignment', '-t', type=str, required=False, help="Alignment algorithm to use. Default MMSeqs. Options: `mummer` and `mmseqs` (mummer for fast genome level alignment, mmseqs for fast protein level alignment).")

    args = parser.parse_args(args)

    print('Getting all the GenBank files ...')
    if args.input_dir != None:
        gbk_list = get_gbk_path(args.input_dir)
    else:
        gbk_list = get_gbk_file(args.input_list)

    plot_synteny(gbk_list, args.output, args.annotate, args.coordinate, args.alignment)

# Main
if __name__ == "__main__":
    main()
