import sys
import os
import re
import csv
from Bio import SeqIO
import taxopy

# User input variables
ncbi_seq_path = sys.argv[2]
rrndb_seq_path = sys.argv[4]
rrndb_meta_path = sys.argv[6]
taxdump_path = sys.argv[8]
output_dir_path = sys.argv[10]

taxdb = taxopy.TaxDb(
    nodes_dmp=os.path.join(taxdump_path, "nodes.dmp"),
    names_dmp=os.path.join(taxdump_path, "names.dmp"),
    merged_dmp=os.path.join(taxdump_path, "merged.dmp"),
)

ncbi_output_records, ncbi_seqid_list, ncbi_taxid_list = [], [], []
ncbi_seq_counter = 1

rrndb_output_records, rrndb_seqid_list, rrndb_taxid_list = [], [], []
rrndb_seq_counter = 1

output_records = []


def get_taxid_from_gbff_update(record, taxdb):
    """
    Get NCBI taxid from record in gbff file
    Check if the taxid has been updated with taxopy
    """
    for feature in record.features:
        if "source" in feature.type:
            tax_id = "".join(
                feature.qualifiers["db_xref"]
            )  # example: /db_xref="taxon:1624"
            tax_id = re.sub(r".*taxon:", "", tax_id)
            new_tax_id = taxdb.oldtaxid2newtaxid.get(int(tax_id), int(tax_id))
        return new_tax_id


def create_tax_dict(meta_data_path):
    """Create dict of record ids and NCBI taxids from rrnDB metadata"""
    tax_dict = {}
    with open(meta_data_path, "r+") as metadata:
        metadata_reader = csv.DictReader(metadata, delimiter="\t")
        for row in metadata_reader:
            tax_dict[row["Data source record id"]] = int(row["NCBI tax id"])
    return tax_dict


def update_seq_id_info(database_name, tax_id, seq_counter):
    """Update sequence id with database name and taxid"""
    seq_id = f"{tax_id}:{database_name}:{seq_counter}"
    return seq_id


def update_record_description(record):
    """Update record description to match emu-prebuilt format"""
    record.description = f"['{record.description}']"
    return record.description


##### NCBI database #####
for record in SeqIO.parse(ncbi_seq_path, "genbank"):
    tax_id = get_taxid_from_gbff_update(record, taxdb)
    ncbi_taxid_list.append(tax_id)

    # update information for new fasta file
    record.id = update_seq_id_info("ncbi", tax_id, ncbi_seq_counter)
    ncbi_seqid_list.append(record.id)
    update_record_description(record)
    ncbi_output_records.append(record)  # f"{identifier} ['{rest_of_string}']"
    ncbi_seq_counter += 1


##### rrnDB database #####
tax_dict = create_tax_dict(rrndb_meta_path)

# Replace missing taxids
new_tax_dict = {
    acc: taxdb.oldtaxid2newtaxid.get(taxid, taxid) for acc, taxid in tax_dict.items()
}
# print("GCF_029225785.1: " + str(new_tax_dict["GCF_029225785.1"]))  # test, should be 2246

# Parse fasta file
for record in SeqIO.parse(rrndb_seq_path, "fasta"):
    rid = record.description
    gcf_acc = rid.split("|")[1]  # GCF_000762265.1

    # update seq_id info for new fasta file
    seq_id = update_seq_id_info("rrn", new_tax_dict[gcf_acc], rrndb_seq_counter)
    record.id = seq_id
    rrndb_seqid_list.append(seq_id)
    rrndb_taxid_list.append(new_tax_dict[gcf_acc])
    update_record_description(record)
    rrndb_output_records.append(record)
    rrndb_seq_counter += 1


##### Concatenate two databases #####
output_records = ncbi_output_records + rrndb_output_records
seq_id_list = ncbi_seqid_list + rrndb_seqid_list
tax_id_list = ncbi_taxid_list + rrndb_taxid_list

# Write fasta file
SeqIO.write(output_records, os.path.join(output_dir_path, "emu_input.fa"), "fasta")
# example: >28903:ncbi:1 ['Mycoplasmopsis bovis strain Donetta 16S ribosomal RNA, complete sequence']

# Write seq2tax map
with open(os.path.join(output_dir_path, "seq2tax.map"), "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(zip(seq_id_list, tax_id_list))
# example: 28903:ncbi:1	28903
