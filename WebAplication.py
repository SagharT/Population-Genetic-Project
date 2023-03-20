#Run: streamlit run WebAplication.py or this 
#link: https://saghart-population-genetic-project-webaplication-7e56el.streamlit.app/
import streamlit as st
import plotly.express as px
import numpy as np
from sklearn.cluster import KMeans
import json
import random

#Clustering countries into 8 clusters by latitude and longitude.
#countrynames.txt contains the names of the countries and their latitude and longitude values.
#Load data from file
data = np.genfromtxt('Data/countrynames.txt', delimiter=' ', dtype='str')
#Load latitude and longitude values of each capital city and normalize them
lat_long = data[:,2:].astype(float) 
lat_long[:,0] /= 90  #Normalize latitude values to [-1, 1]
lat_long[:,1] /= 180  #Normalize longitude values to [-1, 1]
#Normalize Latitude and longitude values to [0, 1]
lat_long[:,:] += 1
lat_long[:,:] /= 2
#Fit K-Means model with 8 clusters
kmeans = KMeans(n_clusters=8, random_state=0).fit(lat_long)
#Print the clusters and coordinates of each center
cluster_coords = []
cluster_countries = []
for i in range(8):
    print("Cluster", i+1, ":")
    cluster_countries.append([])
    for j in range(len(data)):
        if kmeans.labels_[j] == i:
            print(data[j,0])
            cluster_countries[-1].append(data[j,0])
    center = kmeans.cluster_centers_[i]
    print("Coordinates:", center[0], center[1])
    print("\n")
    cluster_coords.append(center)



#Make a page that shows the map of the world and the pie chart of the minor allele frequency of a SNP in each cluster.
#Add title, text input box, random button and select year box to the page
#Add title to the page
original_title = '<p style="color:Black; font-size: 30px;">Geography of Minor allele frequency (MAF)</p>'
st.markdown(original_title, unsafe_allow_html=True)

#Divide the page into three columns to show the text input, random box and the select year box
col1, col2, col3 = st.columns(3)

#In column 2 is a button that user can press to choose a random SNP
available_snps = json.load(open("Data/available_snps.json"))
#Define the button
col2.text('')
col2.text('')
btn_select_snp = col2.button('Random')
#Define the action when the button is pressed
if btn_select_snp:
   snp = random.choice(available_snps)
   st.session_state['snp'] = snp

#In column 1, show the text input box for the user to input a SNP
with col1:
 snp = st.text_input(
    'SNP',
    placeholder="rsID", key="snp")

#In column 3 is a select box for the year range that the user wants to see the minor allele frequency of
with col3:
 year_range = st.selectbox(
    'Year range', ('1-2000', '2001-4000', '4001-6000', '6001-8000', '8001-10000'))
#Read json file which prodused in DataMatrix.py
with open ("Data/"+year_range+"_years.txt.json") as user_file:
    json_file = json.load(user_file)

#If snp is empty, ask the user to input a SNP
if snp == "":
    st.write("Please input a SNP or press the random button.")
    st.stop()
#If user input is not in the json file, show an error message and stop the program
if snp not in json_file:
        st.write("SNP not found, please try again with a different SNP or choose another year range.")
        st.stop()



#Divide the page into two columns to show the map and map information.One column is twice as big as the other column
col1,col2 = st.columns([2,1])
#To the right of the map is the information about the frequency scale
information = '<p  </p>'+'<p style="font-size: 13px ; margin-bottom: 2px;">Frequency Scale = Proportion out of 0.1</p>'+\
'<p style="font-size: 9px; margin-bottom: 2px;">The pie below represents a minor allele frequency of <span style="color: green;">0.25</span> </p>'
col2.markdown (information, unsafe_allow_html=True)
#Add the mini pie chart under the information to clarify the frequency scale
fig_info = px.pie(labels=['maf', ' '], values=[0.25, 0.75], width=20, height=20, 
            color_discrete_sequence=['gold', 'green'])
fig_info.update_traces(hoverinfo='none', textinfo='none')
#Add margin to the pie chart
fig_info.update_layout(margin=dict(t=0, b=0, l=0, r=0, pad=4))
#Add this pie chart to the column 2 too
col2.plotly_chart(fig_info, use_container_width=True, align="center")



#Make the world map, add the pie charts to each cluster and show the map
fig = px.choropleth()
#Adjust the map size, show the countries and the ocean
fig.update_layout(height=400, width=1000)
fig.update_geos(showcountries=True, countrycolor="LightGrey", showocean=True, 
                oceancolor="Lightblue")

#Create the mini pie charts on each cluster
for coord, countries in zip(cluster_coords, cluster_countries):
    individual_sum = 0
    maf_sum = 0
    for country in countries:
        #Sum up the number of individuals and the minor allele frequency of the SNP in each country
        if country in json_file['individual_num']:
            individual_sum += json_file['individual_num'][country]
        if country in json_file[snp]:
            maf_sum += json_file[snp][country]
    if individual_sum > 0:
        #round the percentage to 3 decimal places
        percentage = maf_sum/(2*individual_sum)
        percentage = round(percentage, 3)
    else:
        percentage = 0
        #Add the pie chart to the map, label the pie chart with the minor allele frequency of the SNP
    fig.add_pie(values=[percentage, 1-percentage], labels=['maf', ' '],
                domain={'x':[coord[1]-0.025, coord[1]+0.025], 'y':[coord[0]-0.025, coord[0]+0.025]},
                textinfo='none', hovertemplate='maf: '+str(percentage), 
                marker=dict(colors=['green', 'gold']), showlegend=False)

#Display the chart in Streamlit
col1.plotly_chart(fig, use_container_width=True)

