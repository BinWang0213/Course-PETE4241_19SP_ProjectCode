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

#Calculation of bulk density
df['density_gcc']=df['rho_ma']*(1-df['density_porosity'])+df['rho_fl']*df['density_porosity']

#Calculation of vertical stress at each depth.
density_conv=1000
depth_conv=0.3048
water_density=1000
ob_density=density_conv*1.8            #assuming the average overburden rock density = 1.80
water_depth=1000             #assuming water depth 1000 m
df['depthft']=df['depth_m']/depth_conv
ob_depth= depth_conv*(df.at[0,'depthft']-0)-water_depth
g=9.8
sv_ob= (ob_density*ob_depth*g+water_depth*g*water_density)/1000000
df['dz'] =df['depthft'].diff().fillna(0)
df['s_v'] = df['dz']*depth_conv*df['density_gcc']*density_conv*g/1000000
df.at[0,'s_v']=sv_ob
df['s_v'] = df['s_v'].cumsum()

#Calculation of hydrostatic pressure at each depth.
df['hydrostatic_pres']=df['depthft']*depth_conv*water_density*g/1000000



#Calculation of vertical stress gradient (MPa/km)
df['gradient'] = df['s_v'].diff()/df['depthft'].diff().fillna(1)*3280.84
df=df.round(decimals=3)


#writing the results to a text file
header=["depth_m","density_gcc", "s_v","hydrostatic_pres","porosity","gradient"]
df.to_csv('Data (%s).txt' % field, sep='\t',columns=header,index=False)



#Dividing into blocks
block1=3703.015
block2=3769.462
block3=3821.43
block4=3920.185
block5=3950
block5=3966.21
for index, row in df.iterrows():
    if df.at[index,'depth_m']<=block1:
        df.at[index,'code']='b1'
    elif df.at[index,'depth_m']<=block2 and df.at[index,'depth_m']>=block1:
        df.at[index,'code']='b2'
    elif df.at[index,'depth_m']<=block3 and df.at[index,'depthft']>=block2:
        df.at[index,'code']='b3'
    elif df.at[index,'depth_m']<=block4 and df.at[index,'depthft']>=block3:
        df.at[index,'code']='b4'
    elif df.at[index,'depth_m']<=block5 and df.at[index,'depthft']>=block4:
        df.at[index,'code']='b5' 
    elif df.at[index,'depth_m']<=block6 and df.at[index,'depthft']>=block5:
        df.at[index,'code']='b6'

df['block_mean'] = df.code.map(df.groupby(['code']).density_gcc.mean())
print(df)    
fig=plt.figure(figsize=(5,15))    
plt.plot(df['block_mean'],df['depth_m'])
plt.gca().invert_yaxis()
plt.show()
 

#Plotting data

fig=plt.figure(figsize=(36,20),dpi=300)

fig.tight_layout(pad=1, w_pad=4, h_pad=2)

plt.subplot(1, 6, 1)
plt.grid(axis='both')
plt.ylabel('Depth (m)',fontsize=14)
plt.xlabel('Density (g/cc)',fontsize=14)
plt.plot(df['density_gcc'],df['depth_m'],linewidth=2,c='brown')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 2)
plt.grid(axis='both')
plt.ylabel('Depth (m)',fontsize=14)
plt.xlabel('Vertical Stress (MPa)',fontsize=14)
plt.plot(df['s_v'],df['depth_m'],linewidth=2,c='black')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 3)
plt.grid(axis='both')
plt.ylabel('Depth (m)',fontsize=14)
plt.xlabel('Hydrostatic Pressure (MPa)',fontsize=14)
plt.plot(df['hydrostatic_pres'],df['depth_m'],linewidth=2,c='g')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 4)
plt.grid(axis='both')
plt.ylabel('Depth (m)',fontsize=14)
plt.xlabel('Sv Gradient (MPa/km)',fontsize=14)
plt.plot(df['gradient'],df['depth_m'],linewidth=2,c='r')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 5)
plt.grid(axis='both')
plt.ylabel('Depth (m)',fontsize=14)
plt.xlabel('Porosity',fontsize=14)
plt.plot(df['density_porosity'],df['depth_m'],linewidth=2,c='b')
plt.gca().invert_yaxis()

plt.subplot(1, 6, 6)
plt.grid(axis='both')
plt.ylabel('Depth (m)',fontsize=14)
plt.xlabel('Mean Density (g/cc)',fontsize=14)
plt.plot(df['block_mean'],df['depth_m'],linewidth=2,c='m')
plt.gca().invert_yaxis()

plt.savefig('plot(%s).png' % field)
plt.show()   