This project is writing a software that shows the minor allele frequency for a chosen SNP in populations for a selected period on worldwide 
map. The software will be written in python and will be used in a web application. 
The web application will be written in python using streamlit and is available at
https://saghart-population-genetic-project-webaplication-7e56el.streamlit.app/

# Software and Data
install plink via conda version 1.9
```bash
conda install -c bioconda plink
mkdir Project
cd Project
```
Download data from this repository:  
https://github.com/sarabehnamian/Origins-of-Ancient-Eurasian-Genomes/tree/main/steps/Step%200  
DataS1.bed  
DataS1.bim  
DataS1.fam  
Eurasian - Dataset_tims.xlsx

```bash 
# convert data to ped format
plink --bfile DataS1 --recode --out DataS1
```


# Time Period
The time period is from 0 to 10000 years ago. Data older than 10000 years ago is removed.

With python scipt, TimeSteps.py, years are divided into 5 time periods. 1 time period is 2000 years. 

Input:
- Data.xlsx: The Excel file containing data to be filtered

Output:
- Multiple text files, each containing a subset of the filtered data


# Find Minor allele frequency of each SNP for different population in diffeent time period
With python scipt, DataAnalysis.py, minor allele frequency of each SNP for different population in diffeent time period is calculated.
Modules to be download:
pandas

input: DataS1.ped
- DataS1.bim
- Text files which were prodused by TimeSteps.py

output: 
- Json files which contains the minor allele frequency of each SNP for different population in diffeent time period


# Longtitude and Latitude
Cluster populations due to their longtitude and latitude.
```bash
#find tha name of all countries
cat DataS1.ped | cut -d' ' -f1 | sort | uniq
```
A text file countrynames.txt is created and includes the name of all countries, capital of each country and its longtitude and latitude. The file is space separated.
I got information from this website:
https://www.latlong.net/

# Web application
The web application is written in python using streamlit, WebApplication.py.
In this script, the user can choose a SNP and a time period and the web application shows the minor allele frequency of the SNP in different populations in the selected time period on a world map.

Modules to be download:
numpy
scikit-learn
plotly
streamlit

input:
- Json files which were prodused by DataAnalysis.py
_ countrynames.txt

output:
- Web application

# Run the web application
On your local machine
```bash
streamlit run WebApplication.py
```
Or you can run the web application on the following link:
https://saghart-population-genetic-project-webaplication-7e56el.streamlit.app/

A screenshot of the web application is shown below:
![fig1](https://user-images.githubusercontent.com/112621611/226444339-d85fe7d7-d342-4716-b92c-cf8e482ff0f7.jpeg)

