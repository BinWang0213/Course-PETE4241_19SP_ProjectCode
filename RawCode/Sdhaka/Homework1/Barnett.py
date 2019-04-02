# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:11:36 2019

@author: Sulav
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read and ignore erroneous data
field='BarnettShale'
df=pd.read_table('%sData.txt' % field,sep='\t')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('/', '')
df = df[df.density_gcc != 999.25]

#Calculation of vertical stress at each depth.
density_conv=1000
depth_conv=0.3048
ob_density=density_conv*1.9
ob_depth= depth_conv*(df.at[0,'depthft']-0)
g=9.8
sv_ob=ob_density*ob_depth*g/1000000
df['dz'] =df['depthft'].diff().fillna(0)
df['s_v'] = df['dz']*depth_conv*df['density_gcc']*density_conv*g/1000000
df.at[0,'s_v']=sv_ob
df['s_v'] = df['s_v'].cumsum()

#Calculation of hydrostatic pressure at each depth.
water_density=1000
df['hydrostatic_pres']=df['depthft']*depth_conv*water_density*g/1000000

#Calculation of porosity at each depth
matrix_density=2.7
water_density_gcc=1
df['porosity'] = (matrix_density-df['density_gcc'])/(matrix_density-water_density_gcc)
#Calculation of vertical stress gradient (MPa/km)
df['gradient'] = df['s_v'].diff().fillna(0)/df['depthft'].diff().fillna(1)*3280.84
df=df.round(decimals=3)
print(df)

#writing the results to a text file
header=["depthft","density_gcc", "s_v","hydrostatic_pres","porosity","gradient"]
df.to_csv('Data (%s).txt' % field, sep='\t',columns=header,index=False)



#Dividing into blocks
block1=450
block2=700
block3=797
block4=5000
block5=6193.5
for index, row in df.iterrows():
    if df.at[index,'depthft']<=block1:
        df.at[index,'code']='b1'
    elif df.at[index,'depthft']<=block2 and df.at[index,'depthft']>=block1:
        df.at[index,'code']='b2'
    elif df.at[index,'depthft']<=block3 and df.at[index,'depthft']>=block2:
        df.at[index,'code']='b3'
    elif df.at[index,'depthft']<=block4 and df.at[index,'depthft']>=block3:
        df.at[index,'code']='b4'
    elif df.at[index,'depthft']<=block5 and df.at[index,'depthft']>=block4:
        df.at[index,'code']='b5' 


df['block_mean'] = df.code.map(df.groupby(['code']).density_gcc.mean())


#Plotting data

fig=plt.figure(figsize=(36,20),dpi=300)

fig.tight_layout(pad=1, w_pad=4, h_pad=2)

plt.subplot(1, 6, 1)
plt.grid(axis='both')
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('Density (g/cc)',fontsize=14)
plt.plot(df['density_gcc'],df['depthft'],linewidth=2,c='brown')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 2)
plt.grid(axis='both')
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('Vertical Stress (MPa)',fontsize=14)
plt.plot(df['s_v'],df['depthft'],linewidth=2,c='black')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 3)
plt.grid(axis='both')
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('Hydrostatic Pressure (MPa)',fontsize=14)
plt.plot(df['hydrostatic_pres'],df['depthft'],linewidth=2,c='g')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 4)
plt.grid(axis='both')
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('Sv Gradient (MPa/km)',fontsize=14)
plt.plot(df['gradient'],df['depthft'],linewidth=2,c='r')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 5)
plt.grid(axis='both')
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('Porosity',fontsize=14)
plt.plot(df['porosity'],df['depthft'],linewidth=2,c='b')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 6)
plt.grid(axis='both')
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('Mean Density (g/cc)',fontsize=14)
plt.plot(df['block_mean'],df['depthft'],linewidth=2,c='m')
plt.gca().invert_yaxis()

plt.savefig('plot(%s).png' % field)
plt.show()


#Querries (Q.4)
for index, row in df.iterrows():
    if df.at[index,'depthft']==5000:
        ans1=df.at[index,'s_v']
        ans2=df.at[index,'hydrostatic_pres']
        ans3=df.at[index,'gradient']
        ans4=df.at[index,'density_gcc']
        print("Vertical stress at 5000 ft: %10.3f" %ans1)
        print("Hydrostatic pressure at 5000 ft: %10.3f" %ans2)
        print("Vertical stress gradient at 5000 ft : %10.3f" %ans3)
        print("Bulk density at 5000 ft: %10.3f" %ans4)
    if df.at[index,'depthft']==2500:
        ans5=df.at[index,'porosity']
        print("Porosity at 2500 ft: %10.3f" %ans5)
    
        
