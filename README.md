# Project
Write software that shows the minor allele frequency for a chosen SNP in worldwide 
populations for a selected period (Saghar Toresson):
Example of output:
https://popgen.uchicago.edu/ggv/?data=%221000genomes%22&chr=14&pos=31573859
You can use the modern DNA dataset (PLINK files for Projects.zip).
# Software and Data
install plink via conda version 1.9
```bash
conda install -c bioconda plink
mkdir Project
cd Project
```
Download plink files:
MARITIME_ROUTE.bed
MARITIME_ROUTE.bim
MARITIME_ROUTE.fam

plink --bfile MARITIME_ROUTE --recode --out MARITIME_ROUTE
MARITIME_ROUTE.map    MARITIME_ROUTE.ped 
MARITIME_ROUTE.log  MARITIME_ROUTE.nosex  plink.log


# Time Period

# Find Minor allele frequency of each SNP for different population in diffeent time period

# Longtitude and Latitude
Cluster populations due to their long. and lat. to some points in the map
cat DataS1.ped | cut -d' ' -f1 | sort | uniq

Data: Data.xlsx
note: some population had missing data for long. and lat..
pip install xlsx2csv
xlsx2csv Data.xlsx | awk -F',' '$5 ~ /\.\./ || $6 ~ /\.\./ {print $4}' | sort | uniq
Cuba
France
Jordan
Kazakhstan
Morocco
Nepal
Peru
Puerto Rico
Russia
Spain
Uzbekistan

I wrote it manualy due to the information of the position of the capital of a country.
I got information from this website:
https://www.latlong.net/

Modules to be download:
pip install scikit-learn
pip install geopy
pip install folium

# Web application 