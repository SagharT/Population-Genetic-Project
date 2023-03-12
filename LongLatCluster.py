#!/usr/bin/env python3
'''
Script name: LongLatCluster.py

Description:
This script reads country names and their corresponding latitude and longitude values from a text file, 
normalizes the values, and performs K-Means clustering with 8 clusters. 
The script uses the NumPy and scikit-learn libraries for data manipulation and clustering.

User-defined function: None
Non-standard modules: NumPy, scikit-learn

Procedure:
1.Load country names and corresponding latitude and longitude values from a text file
2.Normalize latitude and longitude values to range [-1, 1] and [0, 1], respectively
3.Perform K-Means clustering with 8 clusters on the normalized values
4.Print the countries in each cluster and the coordinates of the center of each cluster

usage: python Clustering.py countrynames.txt

Input:
- countrynames.txt: A text file containing the names of countries and their corresponding latitude and longitude
values, separated by spaces

Output:
- Print statements displaying the countries in each cluster and the coordinates of the center of each cluster

Date: 2023-03-09
Name: Saghar Toresson 

'''

import numpy as np
from sklearn.cluster import KMeans

#Load data from file
data = np.genfromtxt('countrynames.txt', delimiter=' ', dtype='str')
#Load latitude and longitude values of each capital city and normalize them
lat_long = data[:,2:].astype(float) 
lat_long[:,0] /= 90  # Normalize latitude values to [-1, 1]
lat_long[:,1] /= 180  # Normalize longitude values to [-1, 1]
#Normalize longitude values to [0, 1]
lat_long[:,:] += 1
lat_long[:,:] /= 2
#Fit K-Means model with 8 clusters
kmeans = KMeans(n_clusters=8, random_state=0).fit(lat_long)
# Print the clusters and coordinates of each center
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