#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 22:24:48 2020

@author: skhalil
"""

import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import csv
import os
import matplotlib.pyplot as plt

@st.cache
def get_data(file_node, file_edge):
    #with open('fake_nodes.csv', 'r', encoding="ISO-8859-1") as nodecsv:
    if os.path.isfile(file_node):
        with open(file_node, 'r', encoding="ISO-8859-1") as nodecsv:
            nodereader = csv.reader(nodecsv)
            nodes = [n for n in nodereader][1:]
        node_names = [n[0] for n in nodes]    
        my_G = nx.Graph()
        my_G.add_nodes_from(node_names)
    
    if os.path.isfile(file_edge):
        #with open('fake_edges.csv', 'r', encoding="ISO-8859-1") as edgecsv: 
        with open(file_edge, 'r', encoding="ISO-8859-1") as edgecsv:
            edgereader = csv.reader(edgecsv) 
            next(edgereader)
            for e in edgereader:
                my_G.add_edge(e[0], e[1], weight = float(e[2]))
            
        my_G.remove_nodes_from(list(nx.isolates(my_G)))            
        return my_G

@st.cache
def get_top10_sorted_by_algo(sorted_dict, c_pagerank_dict, 
                             c_degree_dict, c_eigenvector_dict, 
                             c_betweenness_dict, c_closeness_dict, 
                             size, list_name):
    
    name_np = np.array([]); name   = []
    deg_np  = np.array([]); deg  = []
    pr_np   = np.array([]); pr   = []
    bc_np   = np.array([]); bc   = []
    cc_np   = np.array([]); cc   = []
    e_np    = np.array([]); e    = []
    
    # for 1st 10 sorted values
    for tb in sorted_dict[:size]: 
       page_rank   = c_pagerank_dict[tb[0]]
       degree      = c_degree_dict[tb[0]] 
       eigen_value = c_eigenvector_dict[tb[0]]
       betweeness  = c_betweenness_dict[tb[0]] 
       closeness   = c_closeness_dict[tb[0]]
       #print("Name:", tb[0], "| Betweenness Centrality:", round(tb[1],3), "| Degree:", degree, "| Eigenvector:", eigen_value)
       pass_cut = False
       if list_name == 'Target': 
         pass_cut =  closeness <= 0.35#betweeness <=0.01
       elif list_name == 'Connector':
         pass_cut =  closeness > 0.35
       elif list_name == 'None':
         pass_cut = True
        
       if(pass_cut):
         name.append(tb[0]); 
         deg.append(round(degree,3)); 
         pr.append(round(page_rank,3))
         bc.append(round(betweeness,3)); 
         cc.append(round(closeness,3)); 
         e.append(round(eigen_value,3))
    
    name_np   = np.append(name_np, name)
    deg_np    = np.append(deg_np, deg)
    pr_np     = np.append(pr_np, pr)
    bc_np     = np.append(bc_np, bc)
    cc_np     = np.append(cc_np, cc)
    e_np      = np.append(e_np, e)
    df = pd.DataFrame({'Name':name_np, 'D-Centrality':deg_np, 
                         'PageRank':pr_np, 'EigenVector':e_np,
                         'B-Centrality': bc_np,'C-Centrality': cc_np
                    })

    return df
@st.cache  
def show_subnet(G, t_in, s_in):
    H = nx.ego_graph(G, t_in, radius=2)
    pos = nx.kamada_kawai_layout(H)
    nx.draw_networkx(
        H, pos=pos, node_size=20, alpha=1.0, size = 900)
    p=nx.shortest_path(G,source=s_in, target=t_in, weight='weight' )
    path_edges = zip(p,p[1:])
    path_edges = set(path_edges)
    nx.draw_networkx_nodes(H,pos,nodelist=p,node_color='r')
    nx.draw_networkx_edges(H,pos,edgelist=path_edges,edge_color='r',width=4)
    fig = plt.figure()
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.title('Undirected SubGraphs', fontsize = 20)
    plt.axis('off')
    return fig    
