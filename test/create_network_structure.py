#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 01:50:34 2020

@author: skhalil
"""

import pandas as pd
import numpy as np
import re
import string
import os, sys

from functions import *

# ===============
# options
# ===============
#from optparse import OptionParser
#parser = OptionParser()

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--inDir', metavar='T', type=str, action='store',
                  default='input', 
                  dest='inDir', 
                  help='input data directory name')

parser.add_argument('--JOnly', action='store_true',
                  default=True,
                  dest='JOnly',
                  help='create network graph for J, else J+R')

parser.add_argument('--outFile1', metavar='P', type=str, action='store',
                  default='edges.csv', 
                  dest='outFile1',
                  help='output file')

parser.add_argument('--outFile2', metavar='P', type=str, action='store',
                  default='nodes.csv', 
                  dest='outFile2',
                  help='output file')

args = parser.parse_args()
# ===================================================
print(args)
inDir = args.inDir
JOnly = args.JOnly

bare_nodes = pd.read_csv(inDir+"/csv/Jared_nodelist.csv")
intel      = pd.read_csv(inDir+"/csv/SecondDegreeConnections.csv")
df_dnc     = pd.read_csv(inDir+"/csv/DNCRebel.csv")
df_fb_j    = pd.read_csv(inDir+"/csv/JFaceBook.csv") 
df_fb_r    = pd.read_csv(inDir+"/csv/RFaceBook.csv")
df_mb_j    = pd.read_csv(inDir+"/csv/JInbox.csv")
df_mb_r    = pd.read_csv(inDir+"/csv/RInbox.csv")
df_unblkd  = pd.read_csv(inDir+"/csv/UnblockedProduction.csv")


#======================================================
# create the base node df from J's LinkedIn list
#======================================================
bare_nodes['FullName'] = bare_nodes['First Name'].astype(str)+' '+bare_nodes['Last Name'].astype(str)
bare_nodes = drop_NAN_rows(bare_nodes, "First Name")
bare_nodes['FullName'] = bare_nodes['FullName'].apply(clean_parentheses) 
bare_nodes['FullName'] = bare_nodes['FullName'].apply(clean_names) 
bare_nodes["FullName"] = bare_nodes["FullName"].str.strip() #remove white spaces
bare_nodes.replace("", float('NaN'), inplace=True)  
bare_nodes.dropna(subset=["FullName"], inplace=True) 
bare_nodes.drop_duplicates(subset ="FullName", keep = 'first', inplace = True)
bare_nodes.reset_index(drop=True,inplace=True) 
bare_nodes = bare_nodes.sort_values('FullName')
nrows_nodes = bare_nodes.shape[0]
cols = bare_nodes.columns.tolist()
cols = cols[-1:] + cols[:-1]
bare_nodes = bare_nodes[cols]


#====================================================
# filter J's nodes to w.r.t the intel df, and add  
# clients to the nodes. R's linkedIn contacts are not
# available
#====================================================

j_df = drop_NAN_rows(intel, "ConnectionsJH")
r_df = drop_NAN_rows(intel, "ConnectionsRS")
nrows_j_intel = j_df.shape[0]
nrows_r_intel = r_df.shape[0]

# input the column of connections from intel and verify if they are still in J's LinkedIn connection

list_matched =[]
j_conn_df = j_df.loc[:, ['Target', 'Title', 'Company', 'Industry','ConnectionsJH', 'email']]
r_conn_df = r_df.loc[:, ['Target', 'Title', 'Company', 'Industry','ConnectionsRS', 'email']]

list_matched, list_linkedIn = get_conn_checked_list(bare_nodes['FullName'], j_conn_df['ConnectionsJH'], nrows_j_intel)   
list_r_conn                 = get_R_conn_list(bare_nodes['FullName'], r_conn_df['ConnectionsRS'], nrows_r_intel)
list_all_first_conn         = set(list_matched) | set(list_r_conn) # mutual


#keep only J's matched connections to the base nodes df
df_filter_nodes = bare_nodes[bare_nodes['FullName'].isin(list_matched)] 
df_filter_nodes.drop(columns=['First Name', 'Last Name'], inplace=True)

#add R's connections to the base nodes df
xtra = {'FullName': list_r_conn}
df_filter_nodes = df_filter_nodes.append(pd.DataFrame(xtra)) #add R's nodes

# add clients in nodes list
new_row1 = {'FullName':'Jared Heyman', 'Company':'Rebel Fund', 'Position':'Managing Partner', 'Connected On':'10 Feb 2004'}
new_row2 = {'FullName':'Richard Sussman', 'Company':'Rebel Fund', 'Position':'General Partner', 'Connected On':'10 Feb 2004'}
df_filter_nodes = df_filter_nodes.append(new_row1,ignore_index=True, sort=True)
df_filter_nodes = df_filter_nodes.append(new_row2, ignore_index=True, sort=True)

# check for duplicates
df_filter_nodes.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
df_filter_nodes.reset_index(drop=True,inplace=True)#drop=True,inplace=True) 
df_filter_nodes = df_filter_nodes.rename({'Email Address': 'Email_Address'}, axis=1)

#====================================================
#Lets fill in the missing attributes from the
#Unblocked Production file
#====================================================
df_unblkd = df_unblkd.fillna('')
df_unblkd.drop(columns=['LinkedIn'], inplace=True)
df_unblkd = df_unblkd.rename({'Email': 'Email_Address', 'TeamSize': 'Size', 'Title':'Position'}, axis=1)
df_unblkd = df_unblkd[df_unblkd['FullName'].isin(list_all_first_conn)] # generated warning: FIXME
df_unblkd.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
df_unblkd.reset_index(drop=True,inplace=True) # reindex

# merge with the filtered base node df
df_filter_nodes_up1 = df_filter_nodes.merge(df_unblkd, on='FullName', how='left')
cond1 = df_filter_nodes_up1.Company_x==""
cond2 = df_filter_nodes_up1.Position_x==""
cond3 = df_filter_nodes_up1.Email_Address_x==""
df_filter_nodes_up1.Company_x.loc[cond1]  = df_filter_nodes_up1.Company_y.loc[cond1] #generated warning: FIXME
df_filter_nodes_up1.Position_x.loc[cond2] = df_filter_nodes_up1.Position_y.loc[cond2]
df_filter_nodes_up1.Email_Address_x.loc[cond3] = df_filter_nodes_up1.Email_Address_y.loc[cond3]
df_filter_nodes_up1.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
df_filter_nodes_up2 = df_filter_nodes_up1.drop(['Company_y', 'Position_y', 'Email_Address_y'], axis=1)
df_filter_nodes_up2 = df_filter_nodes_up2.rename({'Company_x':'Company','Position_x':'Position','Email_Address_x': 'Email_Address'}, axis=1)

#===================================================
# After the baseline nodes are created, and missing
# attributes are filled, add the target nodes to it 
# ==================================================
df_j_target_node = get_target_nodes(j_df, 'Jared Heyman')
df_j_target_node = df_j_target_node.rename({'Email Address': 'Email_Address'}, axis=1)
list_j_target = sorted(list(df_j_target_node['FullName'])) 

df_r_target_node = get_target_nodes(r_df, 'Richard Sussman')
df_r_target_node = df_r_target_node.rename({'Email Address': 'Email_Address'}, axis=1)
list_r_target = sorted(list(df_r_target_node['FullName'])) 

#total targets
list_target = list_j_target + list_r_target

df_valuable_nodes = df_filter_nodes_up2.append(df_j_target_node)
df_valuable_nodes = df_valuable_nodes.append(df_r_target_node)
df_valuable_nodes = df_valuable_nodes.fillna('')
df_valuable_nodes.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
df_valuable_nodes.reset_index(drop=True,inplace=True) 

#===================================================
# check if connection are in DNC list, if yes then
# assign them a penalty weight
#===================================================
df_dnc = df_dnc.fillna('')
df_dnc = df_dnc[~df_dnc['DNCReason'].str.contains('Positive')]
df_dnc.reset_index(drop=True,inplace=True)

df_filter_dnc = df_dnc[df_dnc['FullName'].isin(list_all_first_conn)] 
df_filter_dnc = df_filter_dnc.rename({'size': 'Size'})
df_filter_dnc = df_filter_dnc.loc[:, ['FullName', 'Industry', 'Size']]
df_filter_dnc.insert(loc=2, column='w1', value=1)
df_filter_dnc.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
df_filter_dnc.reset_index(drop=True,inplace=True) # reindex
list_dnc = sorted(list(df_filter_dnc['FullName']))

#now add this penalty to those matched in df_valuable_nodes
df_node_up1  = df_valuable_nodes.merge(df_filter_dnc, on='FullName', how='left')
cond4 = df_node_up1.Industry_x==""
cond5 = df_node_up1.Size_x==""
df_node_up1.Industry_x.loc[cond4] = df_node_up1.Industry_y.loc[cond4]
df_node_up1.Size_x.loc[cond5] = df_node_up1.Size_y.loc[cond5]
df_node_up2 = df_node_up1.drop(['Industry_y', 'Size_y'], axis=1)
df_node_up2 = df_node_up2.rename({'Industry_x': 'Industry', 'Email Address': 'Email_Address', 'Size_x': 'Size', 'Connected On':'ConnectDate'}, axis=1)
df_node_up2 = df_node_up2[['FullName', 'Company', 'Position', 'Industry', 'Size', 'Email_Address', 'KeywordSearch', 'ConnectDate', 'w1']]
df_node_up2.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
df_node_up2.reset_index(drop=True,inplace=True)


#=====================================================
# lets open fb and email contact data. If a person
# will not be found in either, raise the penalty to +1
#=====================================================
df_filter_fb_j, list_fb_j = fb_contact(df_fb_j, list_matched)
df_filter_fb_r, list_fb_r = fb_contact(df_fb_r, list_r_conn)

df_filter_mb_j, list_mb_j = mb_contact(df_mb_j, list_matched, 'Jared Heyman')
df_filter_mb_r, list_mb_r = mb_contact(df_mb_r, list_r_conn, 'Richard Sussman')

list_social = set(list_fb_j) | set(list_mb_j) | set(list_fb_r) | set(list_mb_r)
#list_social = sorted(list(df_node_up3['FullName'])) 
print('social list:', len(list_social)) #lucky ~200 connectors out of 3363

#Sanity Check: if any target is already clients friend?
list_target_friend = set(list_social) & set(list_target)
#Sanity Check: if any target is dnc?
list_target_dnc = set(list_dnc) & set(list_target)

try:
    if len(list_target_friend)+len(list_target_dnc)==0:
        pass
except ValueError:
    print("Oops!  Some of targets are either already friends with clients or \
    belong to DNC list ...")

# give the unsocial connectors a penalty
print('all nodes', df_node_up2.shape)
df_node_unsocial = df_node_up2[~df_node_up2['FullName'].isin(list_social)]
df_node_unsocial.reset_index(drop=True,inplace=True) 
df_node_unsocial.insert(loc=2, column='w2', value=1)
##drop all columns but w2 and FullName, and merge with df_node_up2
df_node_up4 =  df_node_unsocial.drop(['Email_Address','Industry','KeywordSearch','Position', 'w1', 'Company', 'ConnectDate', 'Size'], axis=1)
df_node_up4 =  df_node_up4.fillna(0)

#merge with the base node df
df_node_up5= df_node_up2.merge(df_node_up4, on='FullName', how='left')
df_node_up5 = df_node_up5.fillna(0)
df_node_up5.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
df_node_up5.reset_index(drop=True,inplace=True) # reindex
print('df_node_up5:', df_node_up5.shape)

#=====================================
# Save the penalty weights in a dict
#=====================================
df_node_up5['penalty'] = df_node_up5['w1']+df_node_up5['w2']
df_node_penalty = df_node_up5.drop(['Email_Address','Industry','KeywordSearch','Position', 'w1', 'Company', 'ConnectDate', 'w2'], axis=1)
df_node_penalty.set_index('FullName', inplace=True)
penalty_dict = df_node_penalty.to_dict('index')

my_quick_dict = {}

for k1, v1 in penalty_dict.items():
    for k2 in v1.values():
        my_quick_dict[k1] = k2
print(len(my_quick_dict))       

##=============
## create edges
## ============
df_edge = pd.DataFrame()
source_grand = np.array([]);
target_grand = np.array([]); 
weight_grand = np.array([]);


if JOnly:
    w_j, s_j, t_j = create_edges('Jared Heyman', list_matched, list_linkedIn, my_quick_dict, nrows_j_intel, j_conn_df)
    source_grand = np.append(source_grand, s_j);
    target_grand = np.append(target_grand, t_j);
    weight_grand = np.append(weight_grand, w_j); 
else:
    w_j, s_j, t_j = create_edges('Jared Heyman', list_matched, list_linkedIn, my_quick_dict, nrows_j_intel, j_conn_df)
    w_r, s_r, t_r = create_edges('Richard Sussman', list_r_conn,  list_linkedIn, my_quick_dict, nrows_r_intel, r_conn_df)

    source_grand = np.append(source_grand, s_j); 
    source_grand = np.append(source_grand, s_r);
    source_grand = np.append(source_grand, np.array(['Jared Heyman']))

    target_grand = np.append(target_grand, t_j); 
    target_grand = np.append(target_grand, t_r);
    target_grand = np.append(target_grand, np.array(['Richard Sussman']))

    weight_grand = np.append(weight_grand, w_j); 
    weight_grand = np.append(weight_grand, w_r)
    weight_grand = np.append(weight_grand, np.array(['1']))

#switch the roles of target and source, it doesn't matter anyway as it non-directional data      
df_edge = pd.DataFrame({'Source':target_grand, 'Target':source_grand, 'Weight': weight_grand})#, weight
df_edge = df_edge.sort_values('Source')
df_edge = drop_NAN_rows(df_edge, 'Source')
df_edge.reset_index(drop=True,inplace=True)

print('edges:', df_edge.shape)
    

# Save to csv format
df_node_up5.to_csv (r'rebel_valuable_nodes.csv', index = False, header=False)
df_edge.to_csv (r'rebel_edges.csv', index = False, header=False)
