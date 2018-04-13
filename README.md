# genbank-parser

## getting GenBank data from FTP server
### wget -r 'ftp://ftp.ncbi.nlm.nih.gov/genbank/gbmam1.seq.gz'


## Importing GenBank objects into BioPython

### from Bio import SeqIO
### f = SeqIO.parse("gbmam7.seq", 'gb')   # creates a generator
### s = next(f)                           # work on find another way to go through generator

## accession number
The accession number is stored in the SeqIO object (s):
### s.annotations['accessions']

## definition field
Then genbank definition field is actually stored in:
### s.description

## date field from locus
The date field from the locus is store in:
### s.date
