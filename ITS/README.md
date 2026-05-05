# ITS databases for emu

[unite-fungi-19.02.2025_dev_SH](unite-fungi-19.02.2025_dev_SH.tar.gz): this database is built from UNITE 19.02.2025 (sh_general_release_dynamic_all_19.02.2025_dev.fasta) and includes the species hypotheses accessions from UNITE in the species names.

## Python script to generate the database above

### Dependencies
- [emu](https://github.com/treangenlab/emu)
- [biopython](https://biopython.org)
- [pandas](https://pandas.pydata.org) (1.5.3 was used)

### UNITE with species hypotheses (SH)

1. Download input fasta file from https://unite.ut.ee/repository.php
    
    To run the script the following files are required:
    - Fasta file: `sh_general_release_dynamic_all_xx.xx.xxxx_dev.fasta`

2. Run python script

Check/edit `input_fa_path`, `output_dir_path`, `database_name`

```
python prep_Unite_for_Emu_SH.py 
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

Abarenkov K, Nilsson RH, Larsson K-H, Taylor AFS, May TW, Frøslev TG, Pawlowska J, Lindahl B, Põldmaa K, Truong C, Vu D, Hosoya T, Niskanen T, Piirmann T, Ivanov F, Zirk A, Peterson M, Cheeke TE, Ishigami Y, Jansson AT, Jeppesen TS, Kristiansson E, Mikryukov V, Miller JT, Oono R, Ossandon FJ, Paupério J, Saar I, Schigel D, Suija A, Tedersoo L, Kõljalg U. 2024. The UNITE database for molecular identification and taxonomic communication of fungi and other eukaryotes: sequences, taxa and classifications reconsidered. Nucleic Acids Research, https://doi.org/10.1093/nar/gkad1039