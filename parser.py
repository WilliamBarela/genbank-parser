from Bio import SeqIO
import os
import csv
import re

def default_search():
    """all of these searches are case insensitive because of reg_row_parser has re.IGNORECASE"""
    regex=[
            r'TK \d+',      # TK [NUMBER]
            r'TK\d+',       # TK[NUMBER]
            r'TTU \d+',     # TTU [NUMBER]
            r'TTU\d+',      # TTU[NUMBER]
            r'TTUM \d+',    # TTUM [NUMBER]
            r'TTUM\d+',     # TTUM[NUMBER]
            r'TTU M \d+',   # TTU M [NUMBER]
            r'TTU M\d+',    # TTU M[NUMBER]
            r'TTU-M \d+',   # TTU-M [NUMBER]
            r'TTU-M\d+'     # TTU-M[NUMBER]
            ]
    return regex

def seq_to_dict(filename):
    file = SeqIO.parse(filename, 'gb')
    return [record for record in file]

def array_checker(input):
    return [input] if type(input)==str else input

def reference(record, reference_no, field):
    reference_len = len(record.annotations['references'])
    if reference_no <= reference_len:
        reference_no = reference_no - 1
        if hasattr(record.annotations['references'][reference_no], field):
            return getattr(record.annotations['references'][reference_no], field)
    else:
        return "NA"
    

def references(record):
    return [
            reference(record, 1, 'authors'),      # authors of reference 1
            reference(record, 1, 'title'),        # authors of reference 1
            reference(record, 1, 'journal'),      # authors of reference 1
            reference(record, 2, 'authors'),      # authors of reference 2
            reference(record, 2, 'title'),        # authors of reference 2
            reference(record, 2, 'journal')       # authors of reference 2
           ]

def reg_row_parser(regex, filename):
    """An example of regex here is r'TK\d+' """
    file = seq_to_dict(filename)
    regex = array_checker(regex)

    rows = []
    for record in file:
        for pattern in regex:
            # This is where you should add additional fields if you would like them
            fields = [
                      filename,                                         # filename
                      record.annotations["data_file_division"],         # which database
                      record.annotations['date'],                       # date
                      record.description,                               # definition
                      record.annotations['sequence_version'],           # sequence version
                      record.annotations['source'],                     # source
                      record.annotations['accessions'][0]               # accession number
                     ]

            # tk/ttu/etc regex match in description 
            if re.search(pattern, record.description, re.IGNORECASE):
                fields.append( re.search(pattern, record.description, re.IGNORECASE).group(0) )
                fields.extend(references(record))
                rows.append(fields)
                continue
            # tk/ttu/etc regex match in source 
            elif re.search(pattern, record.annotations['source'], re.IGNORECASE):
                fields.append( re.search(pattern, record.annotations['source'], re.IGNORECASE).group(0) )
                fields.extend(references(record))
                rows.append(fields)
                continue
            # tk/ttu/etc regex match in organism 
            elif re.search(pattern, record.annotations['organism'], re.IGNORECASE):
                fields.append( re.search(pattern, record.annotations['organism'], re.IGNORECASE).group(0) )
                fields.extend(references(record))
                rows.append(fields)
                continue
            # tk/ttu/etc regex match in features organsim if it exists
            elif 'organism' in record.features[0].qualifiers and re.search(pattern, record.features[0].qualifiers['organism'][0], re.IGNORECASE):
                fields.append( re.search(pattern, record.features[0].qualifiers['organism'][0], re.IGNORECASE).group(0) )
                fields.extend(references(record))
                rows.append(fields)
                continue
            # tk/ttu/etc regex match in features specimen_voucher if it exists
            elif 'specimen_voucher' in record.features[0].qualifiers and re.search(pattern, record.features[0].qualifiers['specimen_voucher'][0], re.IGNORECASE):
                fields.append( re.search(pattern, record.features[0].qualifiers['specimen_voucher'][0], re.IGNORECASE).group(0) )
                fields.extend(references(record))
                rows.append(fields)
                continue

    return rows

def save_to_csv(regex, input_filename, output_filename):
    try:
        # csv_file = csv.writer(file, delimiter=',')                                            # for windows style endings
        data = reg_row_parser(regex, input_filename)
        file = open(output_filename, 'a')
        csv_file = csv.writer(file, delimiter=',', lineterminator="\n")                         # for unix style endings
        csv_file.writerows(data)
        print("CSV with filename " + output_filename + ", had " + str(len(data)) + " rows saved from " + input_filename)
        file.close()
    except:
        print(input_filename +  "could not be opened because format is incorrect")
    return None 

def reaper(regex=default_search(),output_file="master.csv"):
    """usage: reaper([r'TK\d+', r'TM\d+', r'TK \d+'])"""
    input_dir = "../ftp.ncbi.nlm.nih.gov/genbank/"
    input_files = [input_dir + file for file in os.listdir(input_dir)] 

    for file in input_files:
        save_to_csv(regex, file, output_file)
        #save_to_csv(regex, input_dir + file, output_file)
    return "done." 
