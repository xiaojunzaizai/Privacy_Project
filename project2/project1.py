#!/usr/bin/env python
# coding: utf-8

# In[2]:


import networkx as nx
import math
import numpy as np


# In[2]:


# READ:
def get_seed(seed1,seed2,seed_pair):
    G1 = nx.read_edgelist(seed1)
    G2 = nx.read_edgelist(seed2)
    with open(seed_pair,'r') as sp:
        lines = sp.readlines()
    return G1,G2,lines


# In[3]:


# Get G1,G2 paired nodes and stored in Dictionary
def get_pair(lines):
    g1p = []
    g1pdir = {}
    g2p =[]
    for line in lines:
        line = line.strip('\n')
        line = line.split(' ')
        g1p.append(line[0])
        g2p.append(line[1])
        g1pdir[line[0]] = line[1]
    return g1p,g2p,g1pdir


# In[4]:


#Get G1, G2 unpaired nodes
def get_unpair(G1,G2,g1p,g2p):
    g1np = []
    g2np = []
    for i in G1.nodes:
        if i not in g1p:
            g1np.append(i)
    for j in G2.nodes:
        if j not in g2p:
            g2np.append(j)
    return g1np,g2np


# In[5]:


# Get nodes' degrees
def get_degree(node_list,G):
    degree_dir = {}
    for i in node_list:
        degree_dir[i] = G.degree(i)
    return degree_dir


# In[6]:


# get node's neighbors which are in the pair list
def check_in_pairs(node,G,pair_list):
    in_pair_list =[]
    for neighbor in G.neighbors(node):
        if neighbor in pair_list:
            in_pair_list.append(neighbor)
    return in_pair_list      


# In[7]:


# Count how many paired neighbors are in another Graph (G2).
def check_in_other_neighbor(neighbor_pair_list,other_G,pair_dir,other_node):
    other_pair_list = []
    for i in neighbor_pair_list:
        other_pair_list.append(pair_dir[i])
    count = 0
    for j in other_pair_list:
        if j in other_G.neighbors(other_node):
            count +=1
    return count


# In[8]:


# Calculate the score
def get_score(node1_degree,node2_degree,count):
    score = count/((math.sqrt(node1_degree))*(node2_degree))
    return score


# In[19]:


# Calculate ECCE 
def get_ECCE (score_list):
    std = np.std(score_list)
    max1 = max(score_list)
    score_list.remove(max1)
    max2 = max(score_list)
    if std == 0:
        result = 0
    else:
        result = (max1-max2)/std
    return result


# In[10]:


# Based on dictionary's value, get the key.
def get_key (dict, value):
    for k, v in dict.items():
         if v == value:
             a = k 
    return a


# In[11]:


# Calculate G1's one node and All G2 unpaired nodes  ECCE and find the Maximun score's G2 node.
def G1_node_compare_G2(node,G1,G1_pair,G2,G1_pair_dir,G1_unpair_degree_dir,G2_unpair_degree_dir,G2_unpair):
    node_pair_list = check_in_pairs(node,G1,G1_pair)
    G2_node_and_score = {}
    for j in G2_unpair:
        count = check_in_other_neighbor(node_pair_list,G2,G1_pair_dir,j)
        score = get_score(G1_unpair_degree_dir[node],G2_unpair_degree_dir[j],count)
        G2_node_and_score[j] = score

    score_list = list(G2_node_and_score.values())
    max_score_G2_node = get_key(G2_node_and_score,max(score_list))
    ECCE_score = get_ECCE(score_list)
    return ECCE_score, max_score_G2_node


# In[12]:


# If ECCE larger than my setting value. Update G1 pair list, G2 pair list, G1 pair dictionary, and G1, & G2 unpaired list
def update_pair(ecce,node1,node2,v,G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair):
    if ecce > v:
        G1_pair.append(node1)
        G2_pair.append(node2)
        G1_pair_dir[node1] = node2
        G1_unpair.remove(node1)
        G2_unpair.remove(node2)
        

    return G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair
        


# In[13]:


# Read all G1's nodes to do the calculation and update the lists. 
def get_result(v,G1,G2,G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair,G1_unpair_degree_dir,G2_unpair_degree_dir):
    for node in G1_unpair:
        ecce,max_node = G1_node_compare_G2(node,G1,G1_pair,G2,G1_pair_dir,G1_unpair_degree_dir,G2_unpair_degree_dir,G2_unpair)
        G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair = update_pair(ecce,node,max_node,v,G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair)

    return G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair

        


# In[14]:


# Passing two seeds' location and pair list location to get two graph and get final result lists.
def running (seed1,seed2,seed_pair,v):
    G1,G2,node_pairs = get_seed(seed1,seed2,seed_pair)
    G1_pair,G2_pair,G1_pair_dir = get_pair(node_pairs)
    G1_unpair,G2_unpair = get_unpair(G1,G2,G1_pair,G2_pair)
    G1_unpair_degree_dir = get_degree(G1_unpair,G1)
    G2_unpair_degree_dir = get_degree(G2_unpair,G2)

    G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair = get_result(v,G1,G2,G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair,G1_unpair_degree_dir,G2_unpair_degree_dir)
    return G1_pair,G2_pair,G1_pair_dir,G1_unpair,G2_unpair

