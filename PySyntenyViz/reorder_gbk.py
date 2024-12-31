import argparse
from Bio import SeqIO

def reorder_by_custom_order(records, order):
    """
    Reorder records based on a custom order.

    Args:
        records (list): List of SeqRecords.
        order (list): List of record names in the desired order.

    Returns:
        list: Reordered SeqRecords.
    """
    record_dict = {record.name: record for record in records}
    return [record_dict[name] for name in order if name in record_dict]

def reorder_by_size(records):
    """
    Reorder records by contig size in descending order.

    Args:
        records (list): List of SeqRecords.

    Returns:
        list: SeqRecords sorted by sequence length.
    """
    return sorted(records, key=lambda x: len(x.seq), reverse=True)

def main(args=None):
    parser = argparse.ArgumentParser(description="Reorder contigs in a GenBank file.")
    parser.add_argument("--input", "-i", type=str, help="Path to the input GenBank file.")
    parser.add_argument("--output", "-o", type=str, help="Path to save the reordered GenBank file.")
    parser.add_argument(
        "--order",
        type=str,
        nargs="+",
        help="Custom order of contig names (space-separated)."
    )
    parser.add_argument(
        "--by_size",
        action="store_true",
        help="Reorder contigs by size in descending order."
    )

    args = parser.parse_args(args)

    # Read all records from the GenBank file
    records = list(SeqIO.parse(args.input, "genbank"))

    if args.order:
        # Reorder by custom order if provided
        reordered_records = reorder_by_custom_order(records, args.order)
    elif args.by_size:
        # Reorder by size if the option is selected
        reordered_records = reorder_by_size(records)
    else:
        # If no option is provided, maintain the original order
        reordered_records = records

    # Save the reordered records to a new GenBank file
    with open(args.output, "w") as out_handle:
        SeqIO.write(reordered_records, out_handle, "genbank")

if __name__ == "__main__":
    main()
