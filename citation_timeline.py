# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 18:58:43 2018

@author: maria
"""

import time
import pandas as pd
import numpy as np
import pdb

#measure time elapsed
start_time = time.time()

# create dataframe to store initial data
df = pd.DataFrame([], columns=['Year', 'Ref made'])

# read our file
filename = "C:\\Users\\maria\\Desktop\\glob\\data.txt"
fh = open(filename, "r", encoding='utf-8')

# Search our data and store the values we need!

# initial position in file
start_pos = fh.tell()

# initialize reference counter
ref_counter = 0

# counter for our rows
title_counter = 0

# Run through the entire file
line = fh.readline()
line = line.strip('\ufeff\n') #remove starting special characters
while line:

    # Every title
    if line.find("#t") != -1:
        line = line.strip('#t')

        # increase rows counter
        title_counter += 1
        
        # print progress
        if title_counter % 50000 == 0:
            print('50k done...')
        
        # Don't finish the file
        #if title_counter == 500:
           # break

        # create new entry to 'df' (add year to 'df')
        df = df.append({'Year': line}, ignore_index=True)

        # initialize the reference made column
        df.iloc[title_counter - 1, 1] = ''

       # print('Year:', line)  # debug

    elif line.find("#%") != -1:
        line = line.strip('#%')

        # increase reference counter
        ref_counter += 1

        # add reference to 'df'
        df.iloc[title_counter - 1, 1] += line
        df.iloc[title_counter - 1, 1] += ','

        #print('Reference:', line)  # debug

    # Move to next line
    line = fh.readline()

# close file
fh.close()

#measure time
elapsed_time = time.time() - start_time
elapsed_time

# Remove '\n' from columns
cols_to_check = ['Year', 'Ref made']
df[cols_to_check] = df[cols_to_check].replace({'\n': ''}, regex=True)
df.index.name = 'ID'

# save as csv file
df.to_csv('results_hopefully_final.csv', sep=',', index=True, header=True)

#pdb.set_trace()  # breakpoint

#df_ = pd.read_csv("D:\\Desktop\\glob\\results_part_final.csv", sep=',')

#pdb.set_trace()  # breakpoint

# prepare for creation of 'timeline' dataframe

# store unique years that appear in dataframe df

time = np.unique(time)
#time = list(time)

# Create our "timeline" dataframe to store Years and references
timeline = pd.DataFrame(0, index=np.arange(df.shape[0]), columns=time)

#cols_to_check = timeline.columns
#timeline[cols_to_check] = timeline[cols_to_check].replace({np.nan: 0}, regex=True)


# search for non-empty cells in Ref made column in df
for i in range(0, 629814):
    if df.iloc[i, 1]:
        # references made
        value = df.iloc[i, 1]

        # number of references made
        number = value.count(',')

        # convert string -> array
        value = value.split(',')
        del (value[number])

        # print (value,number)#debug

        # increase references taken counter in 'timeline' based on the references made in 'df'
        for j in range(0, number):
            # increase year counter
            year = df.iloc[i, 0]
            timeline.loc[int(value[j]), year] += 1

            # increase total counter (unnecessary)
            # timeline.iloc[int(value[j]), -1] += 1

timeline.to_csv('timeseries_final_final.csv', sep=',', index=True, header=True)
# 629814 citations