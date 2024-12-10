#!/bin/python3

import os
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
    face_colors = []
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            face_colors.append(row)
    return face_colors

#
def parse_feature_fc(feature, face_color_dict):
    '''
    INPUT: A feature and path to a tab-separated file with feature_type, qualifier, value, and face_color.
    OUTPUT: Based on SeqFeature type, returns a specific color to be used as face-color
    '''
    # Set default
    fc = "ivory"
    f_lab = ''

    # Load face color data from file
    #face_colors = load_face_colors(file_path)

    for entry in face_color_dict:
        if feature.type == entry['feature_type']:
            qualifier = entry['qualifier']
            if qualifier in feature.qualifiers:
                if feature.qualifiers[qualifier][0] == entry['value']:
                    fc = entry['face_color']
                    f_lab = entry['label']
                    break
    return fc, f_lab


def plot_synteny(gbk_list, output_png, annotate_file=None):
    '''
    INPUT: A list contianing parsed Genbank objects and A list of pairwise coordinates of Mummer alignment
    OUTPUT: It plots the synteny plot. Nothing returns in output.
    '''
    # Set GenomeViz object
    gv = GenomeViz(fig_track_height=0.7,
                   feature_track_ratio=0.2,
                   #tick_track_ratio=0.4,
                   #tick_style="bar",
                   #align_type="center",
                   )

    if annotate_file != None:
            fc_dict = load_face_colors(annotate_file)

    for gbk in gbk_list:
        track = gv.add_feature_track(gbk.name, gbk.get_seqid2size())

        #Plot individual contigs.
        for seqid, features in gbk.get_seqid2features(feature_type = 'source').items():
            segment = track.get_segment(seqid)
            segment.add_features(features, fc="skyblue", lw=0.5, label_handler=lambda s: str(seqid))

        # Plot target genes
        for seqid, features in gbk.get_seqid2features(feature_type = ['rRNA', 'CDs',  'mobile_element', 'gene']).items
():
        #for seqid, features in gbk.get_seqid2features().items():
             for f in features:
                if annotate_file != None:
                    face_color, f_lab = parse_feature_fc(f, fc_dict)

                    if f_lab != '':
                        segment = track.get_segment(seqid)
                        # Add features to the segment with dynamic face color
                        segment.add_features(f, fc=face_color, lw=0.5, plotstyle='rbox', label_handler = lambda s: f_l
ab)
                else:
                    face_color = 'ivory'
                    f_lab = ''

    #Run MMseqs RBH search
    print('Creating MUMmer/MMseqs alignment ...')
    align_coords = MMseqs(gbk_list).run()
    #align_coords = MUMmer(gbk_list).run()

    #Plot MUMmer/MMseqs RBH search links
    print('Plotting synteny ...')
    if len(align_coords) > 0:
        min_ident = int(min([ac.identity for ac in align_coords if ac.identity]))
        color, inverted_color = "chocolate", "limegreen"
        for ac in align_coords:
            gv.add_link(ac.query_link, ac.ref_link, color=color, inverted_color=inverted_color, v=ac.identity, vmin=mi
n_ident, curve=True, alpha=0.1)
        gv.set_colorbar([color, inverted_color], vmin=min_ident)

    fig = gv.plotfig()
    fig.savefig(f"{output_png}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_dir', '-i', type=str, required=False, help="Poth to directory containing GenBank file
s")
    parser.add_argument('--input_list', type=str, required=False, help="Textfile containing paths of GenBank files")
    parser.add_argument('--output', '-o', type=str, required=True, help="Output image file")
    parser.add_argument('--annotate', '-a', type=str, required=False, help="Sequence features from GenBank file and co
lor to annotate them")
    #parser.add_argument('--legend', '-l', type=str, required=False, help="Show or hide legends")
    parser.add_argument('--alignment', '-t', type=str, required=False, help="Alignment algorithm to use. Default MMSeq
s. Options: `mummer` and `mmseqs` (mummer for fast genome level alignment, mmseqs for fast protein level alignment)")

    args = parser.parse_args()

    print('Getting all the GenBank files ...')
    if args.input_dir != None:
        gbk_list = get_gbk_path(args.input_dir)
    else:
        gbk_list = get_gbk_path(args.input_list)

    plot_synteny(gbk_list, args.output, args.annotate)

if __name__ == "__main__":
    main()
