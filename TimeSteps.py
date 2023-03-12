'''
!/usr/bin/env python3
Script name: TimeSteps.py

Description:
This script reads data from an Excel file, filters the data based on year ranges, 
and saves each subset to a separate text file. The script uses the Pandas library to manipulate the data.

User-defined function: None
Non-standard modules: Pandas

Procedure:
1.Read data from an Excel file
2.Remove spaces from the "ID" column of the DataFrame
3.Define start and end years, and step size for year ranges
4.Generate a list of year ranges
5.Loop through the year ranges and extract subsets of the data that fall within each range
6.Save each subset to a separate text file

usage: python TimeSteps.py Data.xlsx

Input:
- Data.xlsx: An Excel file containing data to be filtered

Output:
- Multiple text files, each containing a subset of the filtered data

Date: 2023-03-08
Name: Saghar Toresson
'''

import pandas as pd

# Read in the Excel file
df = pd.read_excel("Data.xlsx")

# Remove spaces from country names
df["ID"] = df["ID"].str.replace(" ", "")

# Define the start and end years
start_year = 1
end_year = 10000
step = 2000

# Generate a list of year ranges
year_ranges = list(range(start_year, end_year + step, step))

# Loop through the year ranges and save each subset to a file
for i, year_range in enumerate(year_ranges[:-1]):
    subset = df[(df["Yearsbefore1950CE"] >= year_range) and
                (df["Yearsbefore1950CE"] < year_ranges[i+1])]
    subset[["ID", "MasterID"]].to_csv(
        f"{year_range}-{year_ranges[i+1]-1}_years.txt", sep="\t", index=False)
