from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, FeatureLocation
import argparse


# Function to reverse complement a specific locus in a GenBank file
def reverse_complement_genbank(input_file, contig):
    reversed_records = []

    # Parse the GenBank file
    records = SeqIO.parse(input_file, "genbank")

    # Iterate through each record in the GenBank file
    for record in records:
        if record.id == contig:
            # Reverse complement the sequence for the specified contig
            reversed_sequence = record.seq.reverse_complement()

            # Reverse complement features
            new_features = []
            for feature in record.features:
                # Reverse complement the location of the features
                new_location = FeatureLocation(
                    len(record.seq) - feature.location.end,
                    len(record.seq) - feature.location.start,
                    strand=-feature.location.strand,
                )
                new_feature = SeqFeature(
                    location=new_location,
                    type=feature.type,
                    qualifiers=feature.qualifiers,
                )
                new_features.append(new_feature)

            # Create a new record with the reversed sequence and features
            reversed_record = record.__class__(
                id=record.id + "_rc",
                name=record.name,
                description="Reversed complement of " + record.description,
                seq=reversed_sequence,
                features=new_features,
            )

            # Copy annotations and update molecule_type
            reversed_record.annotations = record.annotations.copy()
            reversed_record.annotations["molecule_type"] = record.annotations.get("molecule_type", "DNA")

            # Add the reversed record to the list
            reversed_records.append(reversed_record)
        else:
            # Keep the record unchanged if it doesn't match the specified contig
            reversed_records.append(record)

    return reversed_records

def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', type=str, required=True)
    parser.add_argument('--output', '-o', type=str, required=True)
    parser.add_argument('--contig', '-c', type=str, required=True)

    args = parser.parse_args(args)

    revcomp_records = reverse_complement_genbank(args.input, args.contig)

    SeqIO.write(revcomp_records, args.output, "genbank")


if __name__ == "__main__":
    main()