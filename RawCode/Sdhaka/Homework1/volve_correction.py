import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#correction and proper tabulation of data
df=pd.read_csv('volvedata.las', skiprows=56, names ='abcde', sep='\s+')
for index, row in df.iterrows():
    mod=index%6
    
    if mod==0:
        df.at[index,'depth_m'] = df.at[index,'a']
        
        df.at[index,'bs_in'] = df.at[index+1,'a']
        df.at[index,'bvw_in'] = df.at[index+1,'b']
        df.at[index,'carb_flag'] = df.at[index+1,'c']
        df.at[index,'coal_flag'] = df.at[index+1,'d']
        df.at[index,'delta'] = df.at[index+1,'e']
        
        df.at[index,'grmax_gapi'] = df.at[index+2,'a']
        df.at[index,'grmin_gapi'] = df.at[index+2,'b']
        df.at[index,'j'] = df.at[index+2,'c']
        df.at[index,'klhc_int_md'] = df.at[index+2,'d']
        df.at[index,'klogh_md'] = df.at[index+2,'e']
        
        df.at[index,'m'] = df.at[index+3,'a']
        df.at[index,'n'] = df.at[index+3,'b']
        df.at[index,'perf_flag'] = df.at[index+3,'c']
        df.at[index,'phif'] = df.at[index+3,'d']
        df.at[index,'density_porosity'] = df.at[index+3,'e']
        
        df.at[index,'rho_fl'] = df.at[index+4,'a']
        df.at[index,'rho_ma'] = df.at[index+4,'b']
        df.at[index,'r_w_ohm'] = df.at[index+4,'c']
        df.at[index,'sand_flag'] = df.at[index+4,'d']
        df.at[index,'s_w'] = df.at[index+4,'e']
        
        df.at[index,'s_wirr'] = df.at[index+5,'a']
        df.at[index,'temp_degc'] = df.at[index+5,'b']
        df.at[index,'v_sh'] = df.at[index+5,'c']
        
        
        
    else:
        df.at[index,'depth_m']='NaN'

df.to_csv('volve_corrected.txt', sep='\t', columns=['depth_m', 'bs_in', 'bvw_in', 'carb_flag', 'coal_flag', 'delta', 'grmax_gapi',
                                                 'j', 'klhc_int_md', 'klogh_md', 'm', 'n', 'perf_flag', 'phif', 
                                                 'density_porosity', 'rho_fl', 'rho_ma', 'r_w_ohm', 'sand_flag', 's_w', 
                                                 's_wirr', 'temp_degc', 'v_sh' ], index =False )
df=pd.read_csv('volve_corrected.txt', sep='\t')

df=df.dropna()

df.to_csv('volve_corrected.txt', sep='\t', index = False)
