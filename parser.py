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

# example of re usage
x = ['This is a TK1000356.', 'TK1000345', 'adjf adjfd TK1003845 ajdlfjad.']
print (re.search(r'TK\d+', x[0]).string)
