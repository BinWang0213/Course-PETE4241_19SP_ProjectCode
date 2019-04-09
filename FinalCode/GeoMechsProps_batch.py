import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

import PyLasMech as plm

#Unit Converter
ft=0.3048 #m
g_cm3=1000 #kg/m3
g=9.8 #m/s2
meter=1
mega=1e6 #Mega
Pa=1 #Pa
us=0.000001 #us, micro seconds
psi=6894.76


#Find all LAS files from a dir
LogFiles=plm.FileFinder("../Data/Petrophysics")

#Read all las data into WellLogs and WellLogParams
NumWells=len(LogFiles)

WellLogs=[]
for log in LogFiles: #We only need INPUT LAS file for each well
    log=plm.ReadLas(log)
    
    WellLogs.append(log)

#Basic paramters for Volve field
rho_w=1.0*g_cm3  #formation fluid density
rho_m=2.65*g_cm3 #rock matrix density
z_w=80*meter # ocean water depth @ https://www.offshore-technology.com/projects/volve-oil-field-north-sea/
RHOB_avg=1.75*g_cm3 # average bulk density above the reservoir, Z<2576 ft
phi0=0.37
beta=0.0266*(1/mega*Pa) #convert it unit back to Pa

#Compute geomechanics properties for each well
OutputFolder="./output/GeoMech/"
os.makedirs(OutputFolder, exist_ok=True)

for i in range(len(WellLogs)):
    print("[Post-proccessing] Processing Geomechanical properties....Well=",WellLogs[i].plm_param.WellName)
    l=WellLogs[i]
    param=l.plm_param
    GeoMechParams={}

    #RHOB DT DTS etc from Log
    NonNanIndex=param.getCommonNonNanIndex(l,["RHOB","DT","DTS"])

    DZ=l[0][NonNanIndex]
    #Auto unit setup
    if(param.Units[0]=="F" or param.Units[0]=="f"): DZ=DZ*ft
    elif(param.Units[0]=="M" or param.Units[0]=="m"): DZ=DZ*meter
    else:print("!!!Unknown Unit!!!!")
    
    if("RHOB" in param.CurveNames): 
        RHOB=l["RHOB"][NonNanIndex]
        #Auto unit
        unit=param.Units[param.getCurveIndex("RHOB")]
        if(unit=="g/cm3"): RHOB=RHOB*g_cm3
        else:print("!!!Unknown Unit!!!!",unit)    
    if("DT" in param.CurveNames): 
        DT=l["DT"][NonNanIndex]
        #Auto unit
        unit=param.Units[param.getCurveIndex("DT")]
        if(unit=="us/ft"): DT=DT*us/ft
        else:print("!!!Unknown Unit!!!!",unit)  
    if("DTS" in param.CurveNames): 
        DTS=l["DTS"][NonNanIndex]
        #Auto unit
        unit=param.Units[param.getCurveIndex("DTS")]
        if(unit=="us/ft"): DTS=DTS*us/ft
        else:print("!!!Unknown Unit!!!!",unit) 

    #Calculate geomechanical properties
    if("RHOB" in param.CurveNames): 
        z_0=DZ[0]

        #1. Overburden stress
        Sv0=rho_w*g*z_w+RHOB_avg*g*(z_0-z_w)
        Sv=[Sv0]+list(Sv0+integrate.cumtrapz(RHOB*g, DZ))
        GeoMechParams["Sv"]=np.array(Sv)
        GeoMechParams["Sv_grad"]=GeoMechParams["Sv"]/DZ

        #2. Pore pressure
        GeoMechParams["P_pore"]=rho_w*g*DZ

        #3. Porosity
        GeoMechParams["PORO"]=(rho_m-RHOB)/(rho_m-rho_w)

        #4. Porosity by Athy's equation
        Sv_eff=GeoMechParams["Sv"]-GeoMechParams["P_pore"]
        GeoMechParams["PORO_Athy"]=phi0*np.exp(-beta*Sv_eff)

        #5. Pore pressure by Athy's equation
        GeoMechParams["P_pore_Athy"]=GeoMechParams["Sv"]+1/beta*np.log(GeoMechParams["PORO"]/phi0)

        #Storage New variables into LAS system
        for name, data in GeoMechParams.items():#Fix inf -inf value in data
            data[data==-np.inf]=np.nan
            data[data==np.inf]=np.nan

        plm.appendCurve(l,'Sv', GeoMechParams["Sv"]/1e6, unit='MPa',descr='PyLasMech overburden stress',dataIndex=NonNanIndex)
        plm.appendCurve(l,'P_pore', GeoMechParams["P_pore"]/1e6, unit='MPa',descr='PyLasMech pore pressure',dataIndex=NonNanIndex)
        plm.appendCurve(l,'PORO', GeoMechParams["PORO"], unit='-',descr='PyLasMech porosity',dataIndex=NonNanIndex)
        plm.appendCurve(l,'PORO_Athy', GeoMechParams["PORO_Athy"], unit='-',descr='PyLasMech porosity from Athy',dataIndex=NonNanIndex)
        plm.appendCurve(l,'P_pore_Athy', GeoMechParams["P_pore_Athy"]/1e6, unit='MPa',descr='PyLasMech pore pressure from Athy',dataIndex=NonNanIndex)


    if("DT" in param.CurveNames and "DTS" in param.CurveNames):
        #6. Shear modulus (G,MPa), Possion ratio and Youngs Modulus (E, MPa)
        Vp=1/DT
        Vs=1/DTS

        G=RHOB*Vs*Vs
        GeoMechParams["v"]=(Vp**2-2*Vs**2)/2/(Vp**2-Vs**2)
        GeoMechParams["E"]=2*G*(1+GeoMechParams["v"]) 

        #7. UCS
        GeoMechParams["UCS"]=np.exp(-6.36+2.45*np.log10(0.86*Vp-1172))*mega*Pa
        
        #Storage New variables into LAS system
        for name, data in GeoMechParams.items():#Fix inf -inf value in data
            data[data==-np.inf]=np.nan
            data[data==np.inf]=np.nan

        plm.appendCurve(l,'v', GeoMechParams["v"], unit='-',descr='PyLasMech possion ratio',dataIndex=NonNanIndex)
        plm.appendCurve(l,'E', GeoMechParams["E"]/1e9, unit='GPa',descr='PyLasMech Youngs modulus',dataIndex=NonNanIndex)
        plm.appendCurve(l,'UCS', GeoMechParams["UCS"]/1e6, unit='MPa',descr='PyLasMech UCS',dataIndex=NonNanIndex)
    

    
    
    #Export solution into figures
    WellName=WellLogs[i].plm_param.WellName
    fname=OutputFolder+WellName.replace("/","_")+'_GeoMech.png'

    XLims={"P_pore":(10,90),"Sv":(10,90),"PORO_Athy":(0,0.5),"PORO":(0,0.5)}
    fig=plm.plotLogs(LogData=l,CurveNames=GeoMechParams.keys(),XLims=XLims)    
    plt.savefig(fname,dpi=120,bbox_inches = 'tight')
    print("[IO] Save log figure as ",os.getcwd()+fname)
    plt.close(fig)

    

      
       
    
