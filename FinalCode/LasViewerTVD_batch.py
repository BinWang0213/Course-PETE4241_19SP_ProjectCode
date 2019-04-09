import os
import matplotlib.pyplot as plt

import PyLasMech as plm

#Find all LAS files from a dir
LogFiles=plm.FileFinder("../Data/Drilling")

#Read all las data into WellLogs and WellLogParams
NumWells=len(LogFiles)

WellLogs=[]
for log in LogFiles: #We only need INPUT LAS file for each well
    log=plm.ReadLas(log)
    
    WellLogs.append(log)

#Print one Well log info
plm.printLas(WellLogs[5])

#Output all log data into picture
OutputFolder="./output/TVD/"
os.makedirs(OutputFolder, exist_ok=True)

for i in range(len(WellLogs)):   
    WellName=WellLogs[i].plm_param.WellName
    fname=OutputFolder+WellName.replace("/","_")+'_TVDlog.png'
    
    MD_range=WellLogs[i].plm_param.MinMaxVal[0]
    TVD_range=WellLogs[i].plm_param.MinMaxVal[1]
    Common_range=[min(MD_range+TVD_range),max(MD_range+TVD_range)]
    Xlim={"DEPT":Common_range,"DVER":Common_range}

    fig=plm.plotLogs(LogData=WellLogs[i],CurveNames=["DEPT","DVER"],XLims=Xlim)
    plt.savefig(fname,dpi=120,bbox_inches = 'tight')
    print("[IO] Save log figure as ",os.getcwd()+fname)
    plt.close(fig)