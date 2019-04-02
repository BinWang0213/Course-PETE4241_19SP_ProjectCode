# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:11:36 2019

@author: Sulav
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read and ignore erroneous data
field='GOM'
df=pd.read_table('%sData.txt' % field,sep='\t')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('/', '')
df = df[df.density_gcc != 999.25]

#Calculation of vertical stress at each depth.
density_conv=1000
depth_conv=0.3048
water_density=1000
ob_density=density_conv*1.75
water_depth=depth_conv*1000
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
beta = 0.0313
phi_initial =  0.386
water_density_gcc=1
df['porosity1'] = phi_initial*np.exp(-1*beta*df['eff_v_stress']) 
matrix_density=2.7
water_density_gcc=1
df['porosity2'] = (matrix_density-df['density_gcc'])/(matrix_density-water_density_gcc)
 
df[df < 0] = np.nan
df=df.round(decimals=3)


#writing the results to a text file
header=["depthft","density_gcc","s_v","hydrostatic_pres","porosity1","porosity2","eff_v_stress"]
df.to_csv('Data (%s).txt' % field, sep='\t',columns=header,index=False)



#Plotting data
fig=plt.figure()

fig.tight_layout(pad=1, w_pad=4, h_pad=2)

plt.plot(df['porosity1'],df['depthft'],linewidth=1,c='brown')
plt.plot(df['porosity2'],df['depthft'],linewidth=1,c='blue')
plt.gca().legend(("Porosity(Athy's equation)",'Porosity (Density log)'))
plt.grid(axis='both')
plt.ylabel('Depth (ft)')
plt.gca().invert_yaxis()


plt.savefig('plot1(%s).png' % field)
plt.show()


#Porepressure
df['pp'] = df['s_v']- 1/beta*np.log(phi_initial/df['porosity2']) 
for index, row in df.iterrows():
    if df.at[index,'pp'] < 0:
        df.at[index,'pp'] = 0

fig=plt.figure()

fig.tight_layout(pad=1, w_pad=4, h_pad=2)

plt.plot(df['pp'],df['depthft'],linewidth=1,c='brown')
plt.plot(df['hydrostatic_pres'],df['depthft'],linewidth=1,c='blue')
plt.plot(df['s_v'],df['depthft'],linewidth=1,c='green')


plt.grid(axis='both')
plt.ylabel('Depth (ft)')
plt.gca().legend(('Pore Pressure (MPa)','Hydrostatic Pressure (MPa)', 'Total Vertical Stress (MPa)'))
plt.gca().invert_yaxis()


plt.savefig('plot2(%s).png' % field)
plt.show()