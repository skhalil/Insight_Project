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

def main():
    
    st.title('Welcome to Your Professional Network')
    page = st.sidebar.selectbox('Choose a page', ['Targets', 'Network', 'Connections']) 

    filenames = glob.glob('*.csv')
    #print(filenames)
    file_node = st.selectbox('Please select the node file', filenames)
    file_edge = st.selectbox('Please select the edge file', filenames)   
    G_Big = get_data(file_node,file_edge)
    G = G_Big.copy()


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

    
    if page  == 'Network': 
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
        st.pyplot(fig)
        
    elif page == 'Connections':
        df_connector = get_top10_sorted_by_algo(sorted_betweenness, 
                                                c_pagerank_dict, 
                                                c_degree_dict, 
                                                c_eigenvector_dict, 
                                                c_betweenness_dict, 
                                                c_closeness_dict, 
                                                20, 'Connector')
        df_connector = df_connector.loc[:, ['Name','B-Centrality']]
        st.subheader('Top Connectors Ranked by Brokerage')
        st.write(df_connector.iloc[1:21].style.background_gradient(cmap='Blues').format({}))
        
    else:
        # Add a placeholder to show the progress bar
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

        st.subheader('Top Targets Ranked by Prominance')
        st.write(df_target.iloc[0:19].style.background_gradient(cmap='Blues').format({}))


        top_target_list = [t.strip() for t in df_target['Name']]
        s = 'Jared Heyman'

        target_conn_dict = {}
        for i, t in enumerate(top_target_list):
            all_p=nx.all_shortest_paths(G,source=s, target=t, weight='weight')
            top_three = list(all_p)[0:3]  
            top_intro = [t[1] for t in top_three]
            target_conn_dict[t] = top_intro
            latest_iteration.text(f'Iteration {i+1}')
            bar.progress(i + 1)
            time.sleep(0.1)

        # write them in an array
        t_0 = st.selectbox("Select the target investor to see the best pathway introducers", list(target_conn_dict.keys()))
        st.write('Best pathway introductions')
        name_intro   = np.array([]); 
        name_intro   = np.append(name_intro, target_conn_dict[t_0])
        df_into = pd.DataFrame({'Name':name_intro})
        st.write(df_into.iloc[:].style.background_gradient(cmap='Oranges').format({}))
    
        #nodes_df = pd.read_csv('anonymous_nodes.csv')
        #nodes.['FakeName'] 

        #for n in name_intro:
        #    node_row = nodes_df[nodes_df['FakeName']==n]
        #    print(node_row)
    
        #f = Image.open(t_0+"_subnet.png").show()
        #st.image(t_0+"_subnet.png")
        #fig1  =  show_subnet(G, t_0, s)
        #st.pyplot(fig1)

if __name__ == '__main__':
    main()
