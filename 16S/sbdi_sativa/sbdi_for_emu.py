import sys
import os
import re
import csv
from Bio import SeqIO
import pandas as pd

# User input variables
sbdi_seq_path = sys.argv[2]
sbdi_taxonomy_path = sys.argv[4]
output_dir_path = sys.argv[6]

tax_headers = ['root', 'superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'] 

sbdi_output_records, sbdi_seqid_list, taxid_list = [], [], []
sbdi_seq_counter, tax_counter  = 1,1
tax_dict = {}

def update_seq_id_info(database_name, seq_counter):
    """Update sequence id with database name and taxid"""
    seq_id = f"{database_name}:{seq_counter}"
    return seq_id


##### SBDI database #####
for record in SeqIO.parse(sbdi_seq_path, "fasta"):

    if record.id.startswith("Bacteria"):
        # update information for new fasta file
        tax_lineage = record.description
        record.id = update_seq_id_info("sbdi", sbdi_seq_counter)
        sbdi_seqid_list.append(record.id)

        if tax_lineage not in tax_dict:
            tax_dict[tax_lineage] = tax_counter # append dummy taxid
            tax_counter += 1

        taxid_list.append(tax_dict[tax_lineage])
        sbdi_output_records.append(record)
        sbdi_seq_counter += 1

# Write fasta file
SeqIO.write(sbdi_output_records, os.path.join(output_dir_path, "emu_input.fa"), "fasta")
# example: >sbdi:1 Bacteria;Bacteria;Pseudomonadota;Gammaproteobacteria;Enterobacterales;Enterobacteriaceae;Escherichia;Escherichia coli

# Write seq2tax map
with open(os.path.join(output_dir_path, "seq2tax.map"), "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(zip(sbdi_seqid_list, taxid_list))
# example: sbdi:1	1

# Write taxonomy lineage .tsv
taxonomy_df = pd.DataFrame({'tax_id':tax_dict.values(),
                            'lineage':tax_dict.keys()})
# tax_id  lineage
# 1   Bacteria;Bacteria;Pseudomonadota;Gammaproteobacteria;Enterobacterales;Enterobacteriaceae;Escherichia;Escherichia coli

tax_temp_df = taxonomy_df['lineage'].str.split(pat=';',n=8, expand=True)

tax_temp_df = tax_temp_df.rename(columns={0:'root', 1:'kingdom', 2:'phylum',
                                            3:'class', 4:'order',
                                            5:'family', 6:'genus',
                                            7:'species'})
taxonomy_df[tax_headers] = tax_temp_df
taxonomy_df["clade"] = ""
taxonomy_df["subspecies"] = ""
taxonomy_df["species subgroup"] = ""
taxonomy_df["species group"] = ""
taxonomy_df = taxonomy_df.drop(columns='lineage')
taxonomy_df = taxonomy_df.drop(columns='root')

taxonomy_df.to_csv(f"{output_dir_path}/taxonomy.tsv", sep='\t', index=False)
# tax_id  superkingdom    phylum  class   order   family  genus   species clade   subspecies      species subgroup        species group
# 1       Bacteria        Pseudomonadota  Gammaproteobacteria     Enterobacterales        Enterobacteriaceae      Escherichia     Escherichia coli  
