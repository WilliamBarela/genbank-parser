# getting GenBank data from FTP server
cd ..
rm -rf ./ftp.ncbi.nlm.nih.gov 
wget -r 'ftp://ftp.ncbi.nlm.nih.gov/genbank/gbmam*'   # by default, wget retries 20 times: --tries=20; max: --tries=inf
cd ftp.ncbi.nlm.nih.gov/genbank
for file in $(ls ./); do gunzip $file; done;
