# 16S databases for emu

1. [ncbi-2025-04-22_rrnddb-5.9](ncbi_rrndb/ncbi-2025-04-22_rrnddb-5.9.tar.gz): this database is based on newer versions of the two databases included in the [emu](https://github.com/treangenlab/emu) prebuilt database. The database consists of rrnDB v5.9 and NCBI 16S RefSeq from 2025-04-22. Taxonomy is from NCBI from 2025-04-23. 
The database contains 85 197 sequences from 25 528 bacterial and archaeal species.

2. [sbdi-sativa-2025-11-03](sbdi_sativa/sbdi-sativa-2025-11-03.tar.gz): this database is built from the SBDI Sativa curated 16S GTDB database from the Swedish Biodiversity Infrastructure. Version 2025-11-03 and the `20genomes.assignTaxonomy` file is used. The database is not using the NCBI taxonomy.
The database contains 79 855 sequences from 49 965 bacterial species.

## Python scripts to generate the databases above

### Dependencies
- [emu](https://github.com/treangenlab/emu)
- [biopython](https://biopython.org)
- [taxopy](https://github.com/apcamargo/taxopy) (for ncbi_rrndb)
- [pandas](https://pandas.pydata.org) (for sbdi_sativa)

### NCBI 16S Refseq + rrnDB database

1. Download input files

    To run the script the following files are required:
    - NCBI 16S RefSeq: `bacteria.16SrRNA.gbff.gz` from  https://ftp.ncbi.nlm.nih.gov/refseq/TargetedLoci/Bacteria/
    - NCBI `taxdump` from https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/
    - rrnDB fasta file `rrnDB-x.x_16S_rRNA.fasta` and metadata `rrnDB-x.x.tsv` from https://rrndb.umms.med.umich.edu/downloads/

2. Run python script

Example:
```
python ncbi_rrndb_for_emu.py \
    -n <path/to/bacteria.16SrRNA.gbff> \
    -r <path/to/rrnDB-X.X_16S_rRNA.fasta> \
    -m <path/to/rrnDB-X.X.tsv> \
    -t <path/to/taxdump/> \
    -o <path/to/output_folder>
```

This will generate two input files for building the database with the NCBI taxonomy.

3. Build database
```
emu build-database <database name> \
    --sequences emu_input.fa \
    --seq2tax seq2tax.map \
    --ncbi-taxonomy <path/to/taxdump>
```

### SBDI Sativa 16S GTDB database

1. Download input files from https://doi.org/10.17044/scilifelab.14869077
    
    To run the script the following files are required:
    - Fasta file: `sbdi-gtdb-sativa.rXXrsXXX-X.XXgenomes.assignTaxonomy.fna`
    - Taxonomy: `sbdi-gtdb-sativa.rXXrsXXX-X.bac120.sprep.taxonomy.tsv`

2. Run python script

Example:
```
python sbdi_for_emu.py \
    -s <path/to/sbdi-gtdb-sativa.rXXrsXXX-X.XXgenomes.assignTaxonomy.fna> \
    -t <path/to/sbdi-gtdb-sativa.rXXrsXXX-X.bac120.sprep.taxonomy.tsv> \
    -o <path/to/output_folder>
```

This will generate three input files for building the database **without** the NCBI taxonomy.

3. Build database
```
emu build-database <database name> \
    --sequences emu_input.fa \
    --seq2tax seq2tax.map \
    --taxonomy-list taxonomy.tsv
```

## Acknowledgements
This work builds on example code from the [emu developers](https://osf.io/rgu9p).

Curry, K.D. et al. (2022) ‘Emu: species-level microbial community profiling of full-length 16S rRNA Oxford Nanopore sequencing data’, Nature Methods, 19(7), pp. 845–853. https://doi.org/10.1038/s41592-022-01520-4.

Swedish Biodiversity Infrastructure (SBDI; 2021). SBDI Sativa curated 16S GTDB database. https://doi.org/10.17044/scilifelab.14869077