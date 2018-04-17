from Bio import SeqIO
import os
import csv
import re

def seq_to_dict(filename):
    file = SeqIO.parse(filename, 'gb')
    return [record for record in file]

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

def save_to_csv(regex, input_filename, output_filename):
    data = reg_row_parser(regex, input_filename)
    file = open(output_filename, 'a')
    try:
        # csv_file = csv.writer(file, delimiter=',')                    # for windows style endings
        csv_file = csv.writer(file, delimiter=',', lineterminator="\n") # for unix style endings
        csv_file.writerows(data)
        print("CSV with filename " + output_filename + ", had " + str(len(data)) + " rows saved.")
    finally:
        file.close()
    return None 
