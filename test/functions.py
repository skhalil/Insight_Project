#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 01:54:05 2020

@author: skhalil
"""
import pandas as pd
import numpy as np
import re
import string

def drop_NAN_rows(df, column):
    nan_value = float('NaN')
    df1 = df.replace("", nan_value, inplace=False)#inplace=True
    df1.dropna(subset=[column], inplace=True)
    df1.reset_index(drop=True, inplace=True)
    return df1

def clean_parentheses(name): 
    clean_name = ''
    if re.search('\(.*', name):  
        pos = re.search('\(.*', name).start()
        clean_name = name[:pos]  
    elif  re.search('\[.*', name):
        pos = re.search('\[.*', name).start()
        clean_name = name[:pos] 
    elif  re.search('\".*', name):
        pos = re.search('\".*', name).start()
        clean_name = name[:pos]  
    else: 
        clean_name = name
    return clean_name


def clean_names(name):
    #Remove punctuation
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    name = regex.sub(' ', name)
    #Remove non-ascii characters
    name = name.encode('ascii', 'ignore').decode('ascii')
    n0 = name.replace('MD', '')
    n1 = n0.replace('PhD', '')
    n2 = n1.replace('Ph', '')
    n3 = n2.replace('DO','')
    n4 = n3.replace('MHS', '') 
    n5 = n4.replace('CFP', '')
    n6 = n5.replace('CFP', '')
    n7 = n6.replace('CIMA', '')
    n8 = n7.replace('CPWA', '')
    n9 = n8.replace('CFA', '')
    n10 = n9.replace('MBA', '')
    n11 = n10.replace('CPA', '')
    n12 = n11.replace('"Z"','')
    n13 = n12.replace('CAIA','')
    n14 = n13.replace('MHS', '')
    n15 = n14.replace('/PFS', '')
    n16 = n15.replace('MA', '')
    n17 = n16.replace('abc', '')
    n18 = n17.replace('RPA', '')
    n19 = n18.replace('BOMIHP', '')
    n20 = n19.replace('CPA', '')
    n21 = n20.replace('PT', '')
    n22 = n21.replace('DPT', '')
    n23 = n22.replace('OCS', '')
    n24 = n23.replace('CSCS', '')
    n25 = n24.replace('AuD', '')
    n26 = n25.replace('Dr', '')
    n27 = n26.replace('CLU', '')
    n28 = n27.replace('ChFC', '')
    n29 = n28.replace('Jr', '')
    n30 = n29.replace('CIMP', '')
    n31 = n30.replace('PFP', '')
    n32 = n31.replace('LSSGB','')
    n33 = n32.replace('CIPM','')
    #Remove words made of single letters
    n34 = re.sub(r'\b\w{1}\b', ' ', n33)
    #Remove additional whitespaces
    n35 = n34.strip()
    n36 = re.sub(' +',' ',n35)
    n37 = n36.title()
    return n37

def common_names(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set):
        return (a_set & b_set)
    
def uncommon_names(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set):
        return (a_set | b_set)    
    
def get_conn_checked_list(col_name_linkedIn, col_name_intel, nrows):  
    '''
    Match the connection names from the Intel file to clients LinkedIn connections
    '''
    great_list = [] 
    
    for i in range(0, nrows):
        cons_list_per_row = [t.strip() for t in col_name_intel[i].split(",")]
        for n in cons_list_per_row: great_list.append(n) 
        
    list_intel = sorted(list(set(great_list)))
    list_nodes = sorted(list(col_name_linkedIn))
    list_nodes = list(filter(None, list_nodes)) #lets keep the None values
    
    matched = common_names(list_nodes, list_intel)

    return matched, list_nodes   

def get_R_conn_list(col_name_linkedIn, col_name_intel, nrows):  
    '''
    List the connection names from the Intel file 
    '''
    great_list_2 = [] 
    for i in range(0, nrows):
        cons_list_per_row = [t.strip() for t in col_name_intel[i].split(",")]
        for n in cons_list_per_row: great_list_2.append(n.title()) 
        
    list_intel_2 = sorted(list(set(great_list_2)))   
    return list_intel_2   

def get_target_nodes(df_client,clientName):
    df_target = df_client[df_client.Source == clientName]
    df_target = df_client.drop(columns=['Source', 'First', 'Last', 'ConnectionsJH', 'ConnectionsRS'])
    df_target = df_target.rename({'email': 'Email Address', 'Title': 'Position', 'Target':'FullName'}, axis=1)
    df_target.columns = ['FullName', 'Position', 'Company', 'Industry', 'Email Address', 'KeywordSearch']
    df_target = df_target[['FullName', 'Email Address','Company', 'Position', 'Industry', 'KeywordSearch']]
    return df_target

def fb_contact(df_fb, contact_list):
    df_filter_fb =  df_fb[df_fb['FullName'].isin(contact_list)] 
    df_filter_fb =  df_filter_fb.rename({'Email': 'Email_Address'}, axis=1)
    df_filter_fb =  df_filter_fb.loc[:, ['FullName', 'Email_Address']]
    df_filter_fb.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
    df_filter_fb.reset_index(drop=True,inplace=True) # reindex
    list_fb = sorted(list(df_filter_fb['FullName']))
    return df_filter_fb, list_fb

def mb_contact(df_mb, contact_list, client_name):
    if client_name == 'Jared Heyman':
        df_mb = df_mb.drop(['Gmail', 'OutLookCC'], axis=1)
        df_filter_mb =  df_mb[df_mb['ContactName'].isin(contact_list)]
    else: 
        df_filter_mb =  df_mb[df_mb['FullName'].isin(contact_list)]
    df_filter_mb =  df_filter_mb.rename({'ContactName': 'FullName'}, axis=1)
    df_filter_mb.drop_duplicates(subset ="FullName", keep = "first", inplace = True) 
    df_filter_mb.reset_index(drop=True,inplace=True) 
    list_mb = sorted(list(df_filter_mb['FullName']))
    return df_filter_mb, list_mb 
    
def create_edges(clientName, conn_list_in, list_linkedIn, penalty_dict, nrows_intel, conn_df):
    '''
    create arrays to be used in df of source, target investors 
    and connections links. Also store the relevant penalty weight
    for each edge
    '''
    
    source = np.array([])
    target = np.array([])
    weight = np.array([])

    client = np.array([clientName]*len(conn_list_in))
    investor = np.array(sorted(conn_list_in))
    w = [1+ penalty_dict.get(x, 0) for x in investor]
    
    source = np.append(source, client)
    target = np.append(target, investor)
    weight = np.append(weight, w)
    
    matched_list = []
    for i in range(0, nrows_intel):
        investor_n = conn_df['Target'][i] 
        
        if clientName == 'Jared Heyman':
            conn_list_per_row = [t.title().strip() for t in conn_df['ConnectionsJH'][i].split(",")]
            conn_list = list(filter(lambda x: x != "", conn_list_per_row))
            matched_list = common_names(conn_list, list_linkedIn) 
        else: 
            conn_list_per_row = [t.title().strip() for t in conn_df['ConnectionsRS'][i].split(",")]
            conn_list = list(filter(lambda x: x != "", conn_list_per_row))
            matched_list = conn_list 
            
        if matched_list is None: continue
        #print('i=',i, '', investor_n, '-->', sorted(matched_list))     
        investor_f   = np.array([investor_n]*len(matched_list))
        connection_f = np.array(sorted(matched_list))    
        w_f          = np.array([1]*len(matched_list))
    
        weight = np.append(weight, w_f)
        source = np.append(source, investor_f)
        target = np.append(target, connection_f)
        
    return weight, source, target
