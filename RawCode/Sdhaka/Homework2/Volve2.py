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

df['eff_v_stress'] = df['s_v']-df['hydrostatic_pres']

#Calculation of porosity at each depth
beta = 0.03
phi_initial =  0.2
water_density_gcc=1
df['porosity1'] = phi_initial*np.exp(-1*beta*df['eff_v_stress']) 
df['porosity2'] = df['density_porosity']


df[df <= 0] = np.nan
df=df.round(decimals=3)



# Porepressure
df['pp'] = df['s_v']- np.log(phi_initial/df['porosity2'])/beta
for index, row in df.iterrows():
    if df.at[index,'pp'] < 0:
        df.at[index,'pp'] = 0

# Plotting the figure
fig=plt.figure()

fig.tight_layout(pad=1, w_pad=4, h_pad=2)

plt.plot(df['pp'],df['depth_m'],linewidth=1,c='brown')
plt.plot(df['hydrostatic_pres'],df['depth_m'],linewidth=1,c='blue')
plt.plot(df['s_v'],df['depth_m'],linewidth=1,c='green')


plt.grid(axis='both')
plt.ylabel('Depth (m)')
plt.gca().legend(('Pore Pressure (MPa)','Hydrostatic Pressure (MPa)', 'Total Vertical Stress (MPa)'))
plt.gca().invert_yaxis()


plt.savefig('plot2(%s).png' % field)
plt.show()


 

