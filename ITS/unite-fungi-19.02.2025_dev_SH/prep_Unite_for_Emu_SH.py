from Bio import SeqIO
import pandas as pd
import os

## define variables
input_fa_path = "sh_general_release_dynamic_all_19.02.2025_dev.fasta" 
output_dir_path = os.getcwd()
database_name = "unite-fungi-19.02.2025-SH"
tax_headers = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'SH'] 

output_records = []
file_type = "fasta"
seq_counter, tax_counter = 1, 1
seq_id_list, tax_id_list = [], []
tax_dict = {}

# gather dict of unique tax lineages and assign incremented tax_id
for record in SeqIO.parse(input_fa_path, file_type):
    rid = record.id
    tax_lineage = rid.split("|")[4]
    # k__Fungi;p__Ascomycota;c__Sordariomycetes;o__Hypocreales;f__Hypocreaceae;g__Trichoderma;s__Trichoderma_pluripenicillatum
    # >Glomeraceae|AM076560|SH146432.05FU|refs|k__Fungi;p__Glomeromycota;c__Glomeromycetes;o__Glomerales;f__Glomeraceae;g__;s__uncultured_Glomus
    sh = rid.split("|")[2]
    tax_lineage = str(tax_lineage + "_" + sh + ";" + sh)
    # k__Fungi;p__Ascomycota;c__Sordariomycetes;o__Hypocreales;f__Hypocreaceae;g__Trichoderma;s__Trichoderma_pluripenicillatum_SH1958183.10FU

    # if new tax_lineage, add new entry
    if tax_lineage not in tax_dict:
        tax_dict[tax_lineage] = tax_counter
        tax_counter = tax_counter + 1

    # update seq_id info for new fasta file
    seq_id = f"{database_name}_{seq_counter}"
    record.id = seq_id
    seq_counter = seq_counter + 1
    seq_id_list.append(seq_id)
    tax_id_list.append(tax_dict[tax_lineage])
    output_records.append(record)

# write seq2tax map
SeqIO.write(output_records,f"{output_dir_path}/emu_input.fa", "fasta")
seq_tax_df = pd.DataFrame({'seq_id':seq_id_list,
                            'tax_id':tax_id_list})


# write taxonomy lineage .tsv
seq_tax_df.to_csv(f"{output_dir_path}/seq2tax.map", sep='\t', index=False)

taxonomy_df = pd.DataFrame({'tax_id':tax_dict.values(),
                            'lineage':tax_dict.keys()})
tax_temp_df = taxonomy_df['lineage'].str.split(';',7, expand=True)
tax_temp_df = tax_temp_df.rename(columns={0:'kingdom', 1:'phylum',
                                            2:'class', 3:'order',
                                            4:'family', 5:'genus',
                                            6:'species', 7:'SH'})
taxonomy_df[tax_headers] = tax_temp_df
taxonomy_df = taxonomy_df.drop(columns='lineage')

# remove rank labeling in tax rank names
for col in taxonomy_df.columns:
    if col != 'tax_id' and col != 'SH':
        taxonomy_df[col] = taxonomy_df[col].apply(lambda x:x.split("__",1)[1])
taxonomy_df.to_csv(f"{output_dir_path}/taxonomy.tsv", sep='\t', index=False)