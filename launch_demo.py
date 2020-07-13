#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 20:14:46 2020

@author: skhalil
"""

import streamlit as st
import numpy as np
import pandas as pd
from operator import itemgetter
import networkx as nx
import csv
import os
import time
import matplotlib.pyplot as plt
from cache_functions import *

from enum import Enum
from io import BytesIO, StringIO
from typing import Union

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""
FILE_TYPES = ["csv", "py", "png", "jpg"]

@st.cache
class FileType(Enum):
    """Used to distinguish between file types"""

    IMAGE = "Image"
    CSV = "csv"
    PYTHON = "Python"


def get_file_type(file: Union[BytesIO, StringIO]) -> FileType:
    """The file uploader widget does not provide information on the type of file uploaded so we have
    to guess using rules, in order to make sure user doesn't upload wrong file extensions 

    Arguments:
        file {Union[BytesIO, StringIO]} -- The file uploaded

    Returns:
        FileType -- A best guess of the file type
    """

    if isinstance(file, BytesIO):
        return FileType.IMAGE
    
    content = file.getvalue()
    if (
        content.startswith('"""')
        or "import" in content
        or "from " in content
        or "def " in content
        or "class " in content
        or "print(" in content
    ):
        return FileType.PYTHON

    return FileType.CSV

def main():
    """Run this function to display the Streamlit app"""
    #st.info(__doc__)
    #st.markdown(STYLE, unsafe_allow_html=True)

    st.title('Welcome to Your Professional Network')
    page = st.sidebar.selectbox('Choose a page', ['Targets', 'View_Network', 'Best_Connections'])
    
    file_upload_options = st.selectbox('Select the input files', ['Default', 'Custom'])
    
    if file_upload_options == 'Default':
        file_node = 'anonymous_nodes.csv'
        nodecsv= open(file_node, 'r', encoding="ISO-8859-1")
        nodereader = csv.reader(nodecsv)
        
        file_edge = 'anonymous_edges.csv'
        edgecsv = open(file_edge, 'r', encoding="ISO-8859-1")
        edgereader = csv.reader(edgecsv)
        
    else:  #file_upload_options == 'Custom':  
        file_node = st.file_uploader("Please upload node file", type=FILE_TYPES[0])
        file_edge = st.file_uploader("Please upload edge file", type=FILE_TYPES[0])
        show_file = st.empty()
        if not file_node or not file_edge:
            show_file.info("Please upload a files of type: " + "".join(FILE_TYPES[0]))
            return
        
        file1_type = get_file_type(file_node)
        file2_type = get_file_type(file_edge)
        
        if file1_type == FileType.CSV and file2_type == FileType.CSV:
             nodereader = csv.reader(file_node)
             edgereader = csv.reader(file_edge)
        else: 
            st.print('Please upload the right file extensions')
            return
 
    nodes = [n for n in nodereader][1:]
    node_names = [n[0] for n in nodes]
   
    G = nx.Graph()
    G.add_nodes_from(node_names)
    next(edgereader)
    for e in edgereader:
        G.add_edge(e[0], e[1], weight = float(e[2]))
    G.remove_nodes_from(list(nx.isolates(G)))


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
    
    
    
    if page  == 'View_Network': 
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
        
    elif page == 'Best_Connections':
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
        
        st.write(df_into.iloc[:].style.background_gradient(cmap='Browns').format({}))
        
        #data = pd.read_csv(file)
        #st.dataframe(data.head(10))

    if file_upload_options != 'Default':    
        file_node.close()
        file_edge.close()

if __name__ == '__main__':
    main()
