import os
import matplotlib.pyplot as plt

import PyLasMech as plm

#Find all LAS files from a dir
LogFiles=plm.FileFinder("../Data/PetrophysicsTVD")

#Read all las data into WellLogs and WellLogParams
NumWells=len(LogFiles)

WellLogs=[]
for log in LogFiles: #We only need INPUT LAS file for each well
    log=plm.ReadLas(log)
    
    WellLogs.append(log)

#Print one Well log info
plm.printLas(WellLogs[5])

#Output all log data into picture
OutputFolder="./output/WellLog/"
os.makedirs(OutputFolder, exist_ok=True)

for i in range(len(WellLogs)):   
    WellName=WellLogs[i].plm_param.WellName
    fname=OutputFolder+WellName.replace("/","_")+'_TVDlog.png'
    
    fig=plm.plotLogs(LogData=WellLogs[i],CurveNames=["DT","DTS","RHOB","NPHI","TVD"])
    plt.savefig(fname,dpi=120,bbox_inches = 'tight')
    print("[IO] Save log figure as ",os.getcwd()+fname)
    plt.close(fig)