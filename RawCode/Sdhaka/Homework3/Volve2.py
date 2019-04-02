# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 11:23:28 2019

@author: admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read and ignore erroneous data
field='volve'
df=pd.read_table('%s_corrected.txt' % field,sep='\t')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('/', '')
df = df[df.rho_ma != -999.25]

density_conv=1000
depth_conv=0.3048
vel_conv = 0.3048/1e-6 
water_density=1000
g=9.8


#Calculation of hydrostatic pressure at each depth.
df['hydrostatic_pres']=df['depth_m']*water_density*g/1000000


#Calculation of UCS
for index,row in df.iterrows():
    if df.at[index,'depth_m'] <3780:
        
        df.at[index,'ucs_d'] = 135.9*np.exp(-4.8*df.at[index,'density_porosity'])
    elif df.at[index,'depth_m'] >= 3780:
        
        df.at[index,'ucs_d'] = 1.001*df.at[index,'density_porosity']**(-1.143)
print(df)

#Plotting data
fig=plt.figure(figsize=(4,10))

fig.tight_layout(pad=1, w_pad=4, h_pad=2)
plt.grid(axis='both')
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('UCS from Density(MPa)', fontsize=14)
plt.xlim(0,200)
plt.plot(df['ucs_d'],df['depth_m'],linewidth=2,c='blue')
plt.gca().invert_yaxis()

plt.savefig('plot(volve).png')
plt.show()


 

