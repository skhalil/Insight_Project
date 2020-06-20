#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:18:34 2020
script to hide the identity of clients professional network
@author: skhalil
"""
#import unicodecsv as csv
import pandas as pd
import numpy as np
import re
import csv
from faker import Factory
from collections import defaultdict


def faker(df):
    faker  = Factory.create()
    names  = defaultdict(faker.name)
    companies = defaultdict(faker.company)
    jobs    = defaultdict(faker.job)
    emails  = defaultdict(faker.email)
    
    df['FakeName'] = df['FullName'].apply(lambda x: names[x] if x != 'Jared Heyman' else x)
    df['FakeCompany'] = df['Company'].apply(lambda x: companies[x])
    df['FakePosition'] = df['Position'].apply(lambda x: jobs[x])
    df['FakeEmail'] = df['Email_Address'].apply(lambda x: emails[x])
    
    return df
    
    
def main():
    rebel_nodes = pd.read_csv("rebel_valuable_nodes.csv")
    rebel_nodes_up = faker(rebel_nodes)
    # save the identity map for future reference
    df_map = rebel_nodes.loc[:,['FullName','FakeName']]
    df_map.to_csv (r'secret_identity_map.csv', index = False)
    
    rebel_edges = pd.read_csv("rebel_edges.csv")
    full2fake = dict(zip(df_map.FullName, df_map.FakeName))
    rebel_edges['SourceFake'] = rebel_edges.Source.map(full2fake)
    rebel_edges['TargetFake'] = rebel_edges.Target.map(full2fake)
    
    # keep only the relevant columns
    df_fake_nodes = rebel_nodes_up.loc[:,['FakeName', 'FakeCompany', 'FakePosition', 'FakeEmail', 'Size', 'w1', 'w2', 'penalty']]    
    df_fake_edges = rebel_edges.loc[:,['SourceFake', 'TargetFake', 'Weight']]
    
    # save them
    df_fake_nodes.to_csv (r'../demo/anonymous_nodes.csv', index = False)
    df_fake_edges.to_csv (r'../demo/anonymous_edges.csv', index = False)
    
if __name__ == '__main__':
    main()
