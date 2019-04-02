import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read and ignore erroneous data
df=pd.read_table("hw3_data.txt",sep='\t')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('/', '')
df = df[df.density_gcc != 999.25]


density_conv=1000
depth_conv=0.3048
vel_conv = 0.3048/1e-6 
water_density=1000
g=9.8

#Calculation of hydrostatic pressure at each depth.
df['hydrostatic_pres']=df['depth_ft']*depth_conv*water_density*g/1000000

#Calculation of porosity at each depth
matrix_density=2.7
water_density_gcc=1
df['porosity'] = (matrix_density-df['density_gcc'])/(matrix_density-water_density_gcc)

df = df[df.porosity != 0]

#Calculation of velocity
df['vel_c'] = 1/df['t_compressional_microsft']*vel_conv
df['vel_s'] = 1/df['t_shear_microsft']*vel_conv


#Calculation of modulii
df['poisson'] = (df['vel_c']**2 - 2*df['vel_s']**2) / (2*(df['vel_c']**2-df['vel_s']**2))
df['G'] = df['density_gcc']*density_conv*df['vel_s']**2/1e6
df['E'] = 2*df['G']*(1+df['poisson'])



#Calculation of UCS
for index,row in df.iterrows():
    if df.at[index,'depth_ft'] <5167:
        df.at[index,'ucs_s'] = 0.4067*df.at[index,'E']**0.51
        df.at[index,'ucs_d'] = 135.9*np.exp(-4.8*df.at[index,'porosity'])
    elif df.at[index,'depth_ft'] >= 5167 and df.at[index,'depth_ft'] < 5514:
        df.at[index,'ucs_s'] = 2.4*df.at[index,'E']**0.34
        df.at[index,'ucs_d'] = 135.9*np.exp(-4.8*df.at[index,'porosity'])
    elif df.at[index,'depth_ft'] >= 5514:
        df.at[index,'ucs_s'] = 0.0528*df.at[index,'E']**0.712
        df.at[index,'ucs_d'] = 1.001*df.at[index,'porosity']**(-1.143)
print(df)

#Plotting data
fig=plt.figure(figsize=(10,20))

fig.tight_layout(pad=1, w_pad=4, h_pad=2)

plt.subplot(1, 2, 1)
plt.grid(axis='both')
plt.xlim(0,500)
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('UCS from Sonic(MPa)', fontsize=14)
plt.plot(df['ucs_s'],df['depth_ft'],linewidth=2,c='red')
plt.gca().invert_yaxis()

plt.subplot(1, 2, 2)
plt.grid(axis='both')
plt.xlim(0,500)
plt.ylabel('Depth (ft)',fontsize=14)
plt.xlabel('UCS from Density(MPa)', fontsize=14)
plt.plot(df['ucs_d'],df['depth_ft'],linewidth=2,c='blue')
plt.gca().invert_yaxis()

plt.savefig('plot.png')
plt.show()


#Querries 
for index, row in df.iterrows():
    if df.at[index,'depth_ft']==5100:
        ans1=abs(df.at[index,'ucs_s']-df.at[index,'ucs_d'])
        ans2 = df.at[index,'ucs_s']
        print("absolute difference at 5100 ft: %10.3f" %ans1)
        print("UCS from sonic at 5100 ft: %10.3f" %ans2)
    if df.at[index,'depth_ft']==5300:
        ans3=abs(df.at[index,'ucs_s']-df.at[index,'ucs_d'])
        ans4 = df.at[index,'ucs_s']
        print("absolute difference at 5300 ft: %10.3f" %ans3)
        print("UCS from sonic at 5300 ft: %10.3f" %ans4)
    if df.at[index,'depth_ft']==5800:
        ans5=abs(df.at[index,'ucs_s']-df.at[index,'ucs_d'])
        ans6 = df.at[index,'ucs_s']
        print("absolute difference at 5800 ft: %10.3f" %ans5)
        print("UCS from sonic at 5800 ft: %10.3f" %ans6)
        
        