from Bio import SeqIO
import os
import csv
import re

def seq_to_dict(filename):
    file = SeqIO.parse(filename, 'gb')
    return [record for record in file]

def data_parser(filename):
    file = seq_to_dict(filename)
    rows = [[filename, record.annotations['accessions'], record.description] if re.search(r'TK\d+', record.description).string else None for record in file]
    rows.remove(None)
    
def reg_parser(regex, filename):
    """An example of regex here is r'TK\d+' """
    file = seq_to_dict(filename)
    for record in file:
        print (record.annotations['accessions'][0] + ", " + re.search(regex, record.description).group(0)) if re.search(regex, record.description) else None

def reg_row_parser(regex, filename):
    """An example of regex here is r'TK\d+' """
    file = seq_to_dict(filename)

    rows = []
    for record in file:
        if re.search(regex, record.description):
            # fields to be included in output file.
            fields = [
                      filename,                                         # filename
                      record.annotations['accessions'][0],              # accession number
                      re.search(regex, record.description).group(0)     # TK/TM/TTU Number
                     ]
            rows.append(fields)
    return rows

def reaper():
    """ Don't use the reaper, it eats up too much memory """
    files = os.listdir("./")
    records = [records.extend(seq_to_dict(file)) for file in files]
    return records 

def save_to_csv(input_filename, output_filename, data):
    file = open(output_filename, 'ab')
    try:
        csv_file = csv.writer(file, delimiter=',')
        csv_file.writerows(data)
    finally:
        file.close()
    return "CSV with filename " + output_filename + ", saved." 
