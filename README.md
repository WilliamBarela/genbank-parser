# genbank-parser

## Usage
```
reaper(r'TK\d+')
```

FIXME: Make reaper handle list of regex statements
FIXME: Check other fields than description

## getting GenBank data from FTP server
```
wget -r 'ftp://ftp.ncbi.nlm.nih.gov/genbank/gbmam*'   # by default, wget retries 20 times: --tries=20; max: --tries=inf
cd ftp.ncbi.nlm.nih.gov/genbank
for file in $(ls ./); do gunzip $file; done;
```

## Importing GenBank objects into BioPython
```
from Bio import SeqIO
f = SeqIO.parse("gbmam7.seq", 'gb')   # creates a generator
s = next(f)                           # work on find another way to go through generator
```

## accession number
The accession number is stored in the SeqIO object (s):
```s.annotations['accessions']```

## definition field
Then genbank definition field is actually stored in:
```s.description```

## date field from locus
The date field from the locus is store in:
```s.date```
