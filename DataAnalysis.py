import csv
import sys
import pandas as pd
import json

# Set the field size limit to a larger value
csv.field_size_limit(sys.maxsize)
# Read in the bim and ped files
bim = pd.read_csv('DataS1.bim', sep='\t', header=None)
# Calculate the starting and ending columns for the ped file
filelist = ["1-2000_years.txt", "2001-4000_years.txt", "4001-6000_years.txt", 
            "6001-8000_years.txt", "8001-10000_years.txt"]

# TODO: Rename sample_dict to something more descriptive
sample_dict = {}
# make a set of countries
countries = set()
for file in filelist:
    with open(f"Data/{file}", "r") as sample:
        # skip the first line
        sample.readline()
        for line in sample:
            a = line.strip()
            b = a.split("\t")
            countries.add(b[0])
            key = tuple(b)
            sample_dict[key] = file

# convert set to a list
countries = list(countries)
# Get the fifth column of the bim file
# TODO: what do they mean?
bim_col5 = bim.iloc[:, 4]
bim_col2 = bim.iloc[:, 1]

# TODO: What does this do?
year_country_dicts = [{} for _ in range(len(filelist))]
#Make a set of all the SNPs that exist in my json files
available_snps = set()
# Open the CSV file
with open('DataS1.ped', newline='') as csvfile:
    # Create a CSV reader object, delimited by spaces
    reader = csv.reader(csvfile, delimiter=' ')
    # TODO: i is unnecessary
    i = 0
    for row in reader:
        # TODO: What is this key?
        key = tuple(row[0:2])
        if key in sample_dict:
            # If the key is found, increment the frequency counter for each occurrence of the value
            # TODO: update this comment
            file = sample_dict[key]
            file_index = filelist.index(file)
            country = row[0]
            # TODO: country_index and countries is not needed
            country_index = countries.index(country)
            # TODO: Explain what this does
            if 'individual_num' not in year_country_dicts[file_index]:
                year_country_dicts[file_index]['individual_num'] = {}
            if country in year_country_dicts[file_index]['individual_num']:
                year_country_dicts[file_index]['individual_num'][country] += 1
            else:
                year_country_dicts[file_index]['individual_num'][country] = 1
            # TODO: Explain this
            for start_col, end_col in zip(range(6, len(row), 2), range(7, len(row), 2)):
                snp_index = (start_col-6)//2
                snp = bim_col2.iloc[snp_index]
                value = str(bim_col5.iloc[snp_index])

                if row[start_col] == value:
                    available_snps.add(snp)
                    if snp not in year_country_dicts[file_index]:
                        year_country_dicts[file_index][snp] = {}
                    if country in year_country_dicts[file_index][snp]:
                        year_country_dicts[file_index][snp][country] += 1
                    else:
                        year_country_dicts[file_index][snp][country] = 1
                if row[end_col] == value:
                    available_snps.add(snp)
                    if snp not in year_country_dicts[file_index]:
                        year_country_dicts[file_index][snp] = {}
                    if country in year_country_dicts[file_index][snp]:
                        year_country_dicts[file_index][snp][country] += 1
                    else:
                        year_country_dicts[file_index][snp][country] = 1
            # TODO: Remove
            i += 1
for year, file in zip(year_country_dicts, filelist):
    with open("Data/{}.json".format(file), "w") as year_file:
        json.dump(year, year_file)
#conver the set to a list
available_snps = list(available_snps)
with open("Data/available_snps.json", "w") as snp_file:
    json.dump(available_snps, snp_file)

