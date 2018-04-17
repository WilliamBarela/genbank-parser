from Bio import SeqIO
import os
import csv
import re

def seq_to_dict(filename):
    file = SeqIO.parse(filename, 'gb')
    return [record for record in file]

def array_checker(input):
    return [input] if type(input)==str else input

def reg_row_parser(regex, filename):
    """An example of regex here is r'TK\d+' """
    file = seq_to_dict(filename)
    regex = array_checker(regex)

    rows = []
    for record in file:
        for pattern in regex:
            if re.search(pattern, record.description, re.IGNORECASE):
                # fields to be included in output file.
                fields = [
                          filename,                                             # filename
                          record.annotations['accessions'][0],                  # accession number
                          re.search(pattern, record.description, re.IGNORECASE).group(0)       # TK/TM/TTU Number
                         ]
                rows.append(fields)
                continue
    return rows

def save_to_csv(regex, input_filename, output_filename):
    data = reg_row_parser(regex, input_filename)
    file = open(output_filename, 'a')
    try:
        # csv_file = csv.writer(file, delimiter=',')                            # for windows style endings
        csv_file = csv.writer(file, delimiter=',', lineterminator="\n")         # for unix style endings
        csv_file.writerows(data)
        print("CSV with filename " + output_filename + ", had " + str(len(data)) + " rows saved from " + input_filename)
    finally:
        file.close()
    return None 

def reaper(regex=[r'TK \d+', r'TK\d+', r'TTU \d+', r'TTU\d+', r'TTUM \d+', r'TTUM\d+', r'TTU M \d+', r'TTU M\d+', r'TTU-M \d+', r'TTU-M\d+'],output_file="TK_definition.csv"):
    """usage: reaper([r'TK\d+', r'TM\d+', r'TK \d+'])"""
    input_dir = "../ftp.ncbi.nlm.nih.gov/genbank/"
    input_files = [input_dir + file for file in os.listdir(input_dir)] 

    for file in input_files:
        save_to_csv(regex, file, output_file)
    return "done." 
