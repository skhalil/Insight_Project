#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 20:14:46 2020

@author: skhalil
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import time
from operator import itemgetter
import networkx as nx
import glob
from cache_functions import *


st.title('Welcome to Your Professional Network')


def file_selector(folder_path='*.csv'):
    #filenames = os.listdir(folder_path)
    filenames = glob.glob(folder_path)
    #print(filenames)
    node_filename = st.selectbox('Select the node file', filenames)
    edge_filename = st.selectbox('Select the edge file', filenames)
    #node_file_path = os.path.join(folder_path, node_filename)
    #edge_file_path = os.path.join(folder_path, edge_filename)
    #print(node_filename)
    #print(edge_filename)
    return node_filename, edge_filename

file_node, file_edge = file_selector()
st.write('Files selected:`%s`' % file_node)
st.write('Edge file selected: `%s`' % file_edge)


#with st.file_input() as input:
#    if input == None:
#      st.warning('No file found')
#      
#    else: 
#      file_node = input.read()

#print(file_node)      

#========
    
G_Big = get_data(file_node,file_edge)
G = G_Big.copy()

#G.remove_nodes_from(list(nx.isolates(G)))
#print(nx.info(G)) 
if st.sidebar.button('View network graph'):
    fig = plt.figure()
    plt.rcParams['figure.figsize'] = (4, 4)
    plt.style.use('fivethirtyeight')
    pos = nx.spring_layout(G, k=0.1)
    # drawing nodes
    nx.draw_networkx_nodes(G, pos, node_size = 10, node_color = 'orange')
    nx.draw_networkx_edges(G, pos, width = 1, alpha = 0.5, edge_color = 'black')
    #nx.draw_networkx_labels(G, pos, font_size = 4, font_family = 'sans-serif')
    plt.title('Network Graph', fontsize = 20)
    plt.axis('off')
    #plt.show()
    st.pyplot(fig)


c_pagerank_dict = nx.pagerank(G, alpha=0.9)# current node’s importance from its links and their neighbors
nx.set_node_attributes(G, c_pagerank_dict, 'pagerank')
sorted_pagerank = sorted(c_pagerank_dict.items(), key=itemgetter(1), reverse=True)

c_eigenvector_dict = nx.eigenvector_centrality_numpy(G) #find the hub, considering how many other hubs you are connected to
nx.set_node_attributes(G, c_eigenvector_dict, 'eigenvector')
sorted_eigenvector = sorted(c_eigenvector_dict.items(), key=itemgetter(1), reverse=True)
  
c_degree_dict = nx.degree_centrality(G) # shortest paths that pass through a particular node
nx.set_node_attributes(G, c_degree_dict, 'degreeness')
sorted_degree = sorted(c_degree_dict.items(), key=itemgetter(1), reverse=True)

c_closeness_dict = nx.closeness_centrality(G)
nx.set_node_attributes(G, c_closeness_dict, 'closeness')
sorted_closeness = sorted(c_closeness_dict.items(), key=itemgetter(1), reverse=True)

c_betweenness_dict = nx.betweenness_centrality(G) # shortest paths that pass through a particular node
nx.set_node_attributes(G, c_betweenness_dict, 'betweenness')
sorted_betweenness = sorted(c_betweenness_dict.items(), key=itemgetter(1), reverse=True)

## Connectors
df_connector = get_top10_sorted_by_algo(sorted_betweenness, 
                                    c_pagerank_dict, 
                                    c_degree_dict, 
                                    c_eigenvector_dict, 
                                    c_betweenness_dict, 
                                    c_closeness_dict, 
                                    20, 'Connector')
df_connector = df_connector.loc[:, ['Name','B-Centrality']]

if st.sidebar.button('View your top 15 hub list'):
    st.subheader('Top 15 connectors ranked by Brokerage Strength')
    st.write(df_connector.iloc[1:21].style.background_gradient(cmap='Blues').format({}))

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

## Targets
df_target = get_top10_sorted_by_algo(sorted_degree, 
                                    c_pagerank_dict, 
                                    c_degree_dict, 
                                    c_eigenvector_dict, 
                                    c_betweenness_dict, 
                                    c_closeness_dict, 
                                    20, 'Target')
df_target = df_target.loc[:, ['Name','D-Centrality']]


st.subheader('Top 15 targets ranked by Prominance')
st.write(df_target.iloc[0:19].style.background_gradient(cmap='Blues').format({}))


top_target_list = [t.strip() for t in df_target['Name']]
s = 'Jared Heyman'

target_conn_dict = {}


for i, t in enumerate(top_target_list):
    all_p=nx.all_shortest_paths(G,source=s, target=t, weight='weight')
    top_three = list(all_p)[0:3]  
    top_intro = [t[1] for t in top_three]
    #print('\n',top_three)
    #print('\n',t,':', top_intro)
    target_conn_dict[t] = top_intro
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

    
t_0 = st.selectbox("Select the target investor to see the best pathway introducers", list(target_conn_dict.keys()))
#print(t_0)
#print(target_conn_dict[t_0])
st.write('Best pathway introductions')
#st.write(target_conn_dict[t_0])


#name_intro   = np.array([]); 
#name_intro   = np.append(name_intro, target_conn_dict[t_0])
#df_into = pd.DataFrame({'Name':name_intro})

#print(df_into)

st.write(df_into.iloc[:].style.background_gradient(cmap='Oranges').format({}))

nodes_df = pd.read_csv('anonymous_nodes.csv')
#nodes.['FakeName'] 

#for n in name_intro:
#    node_row = nodes_df[nodes_df['FakeName']==n]
#    print(node_row)
    
#f = Image.open(t_0+"_subnet.png").show()
#st.image(t_0+"_subnet.png")
#fig1  =  show_subnet(G, t_0, s)
#st.pyplot(fig1)

