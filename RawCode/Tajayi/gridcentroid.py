import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#correction and proper tabulation of data
df=pd.read_csv('CMG3 Grid Bottom Time 2007-12-31.txt', skiprows=4, names ='abc', sep='\s+')
df2=pd.read_csv('CMG3 Grid Top Time 2007-12-31.txt', skiprows=4, names ='abc', sep='\s+')
df3=pd.read_csv('testtext.txt', names ='a', sep='\s+')
for index, row in df3.iterrows():
    m = index
    n = row
    try:
        df3.at[index,'depth_m'] = float(df3.at[index,'a']) + float(df3.at[index,'a'])
    except ValueError:
        continue
        df3.at[index,'depth_m'] = df3.at[index,'a']
    
for index, row in df.iterrows():
    m = index
    n = row
    try:
        df.at[index,'Grid Centroid Z'] = (float(df.at[index,'c']) + float(df2.at[index,'c']))/2
        df.at[index,'Grid Centroid X'] = df.at[index,'a']
        df.at[index,'Grid Centroid Y'] = df.at[index,'b']
    except ValueError:
        continue
        df.at[index,'Grid Centroid Z'] = df.at[index,'c']
        
df.to_csv('all cells cmg.txt', sep='\t', columns=['Grid Centroid X', 'Grid Centroid Y','Grid Centroid Z' ], index =False )