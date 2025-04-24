# 16S databases for emu

Updated database for [emu](https://github.com/treangenlab/emu): `ncbi-2025-04-22_rrnddb-5.9.tar.gz`.
The database consists of rrnDB v5.9 and NCBI 16S RefSeq from 2025-04-22. Taxonomy is from NCBI from 2025-04-23. 
The database contains 85 197 sequences from 25 528 bacterial and archaeal species.

## Build updated database

### Dependencies
- [biopython](https://biopython.org)
- [taxopy](https://github.com/apcamargo/taxopy) - can be installed with pip or conda
- emu

### Prepare input files for `emu build-database`

1. Download input files

    To run the script the following files are required:
    - NCBI 16S RefSeq: `bacteria.16SrRNA.gbff.gz` from  https://ftp.ncbi.nlm.nih.gov/refseq/TargetedLoci/Bacteria/
    - NCBI `taxdump` from https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/
    - rrnDB fasta file `rrnDB-x.x_16S_rRNA.fasta` and metadata `rrnDB-x.x.tsv` from https://rrndb.umms.med.umich.edu/downloads/

2. Run python script

Example:

```
python ncbi_rrndb_for_emu.py -n <path/to/bacteria.16SrRNA.gbff> \
 -r <path/to/rrnDB-5.9_16S_rRNA.fasta> \
 -m <path/to/rrnDB-5.9.tsv> \
 -t <path/to/taxdump/> \
 -o <path/to/output_folder>
```
This will generate two input files for building the database with the NCBI taxonomy.

### Build database

`emu build-database <database name> --sequences emu_input.fa --seq2tax seq2tax.map --ncbi-taxonomy <path/to/taxdump>`

## Acknowledgements
This work builds on example code from the [emu developers](https://osf.io/rgu9p).