import os
import matplotlib.pyplot as plt

import PyLasMech as plm

#Find all LAS files from a dir
LogFiles=plm.LasFinder("../Data/")

#Read all las data into WellLogs and WellLogParams
NumWells=len(LogFiles)/2

WellLogs=[]
WellLogParams=[]
for log in LogFiles[::2]: #We only need INPUT LAS file for each well
    log,param=plm.ReadLas(log)
    
    WellLogs.append(log)
    WellLogParams.append(param)

#Output all log data into picture
OutputFolder="./output/"
os.makedirs(OutputFolder, exist_ok=True)

for i in range(len(WellLogs)):   
    fname=OutputFolder+WellLogParams[i].WellName.replace("/","_")+'_log.png'

    fig=plm.plotLogs(LogData=WellLogs[i],CurveNames=["DT","DTS","RHOB","NPHI"])
    plt.savefig(fname,dpi=300,bbox_inches = 'tight')
    print("[IO] Save log figure as ",os.getcwd()+fname)
    plt.close(fig)