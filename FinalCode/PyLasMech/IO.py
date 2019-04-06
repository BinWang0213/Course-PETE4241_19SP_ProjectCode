
import sys,os
import numpy as np
sys.path.append(os.path.realpath('..'))

from .lasio import read
from .utils import showTable,showTables,findIntersection,type_of_script


#Unit system
ft=0.3048 # 1 ft = 0.3048 m


#Common parameters 
class Params:
    def __init__(self):
        """Basic parameters for PyLasMech

        SI unit is the default unit system
        
        Arguments
        ---------
        Depth         -- [startDepth,endDepth]
        Depth_step    -- measurement depth step
        unit          -- SI unit conversion factor

        NonNanDict    -- The array index for non-nan values

        Author:Bin Wang(binwang.0213@gmail.com)
        Date: April. 2019
        """
        self.fname=""
        self.WellName=""
        self.Depth=[0,100]
        self.Depth_step=0.5

        
        #Curves information
        self.CurveNames=[]
        self.Units=[]
        self.AvailDepth=[]
        self.CommonDepth=[]
        self.MinMaxVal=[]
        self.Comments=[]
        self.NonNanDict={}


def LasFinder(path="../Data/"):
    #Search all log files from the folder and subfolder
    DataFolder=os.path.abspath(path)
    fnames={}

    for root, dirs, files in os.walk(DataFolder):
        for file in files:
            if file.lower().endswith(".las"):
                fnames[file]=os.path.join(root, file)
    
    print("[IO] Found %d log files" %(len(fnames)))

    #print relative path looks better than absolute path
    relative_paths = [os.path.relpath(path, os.getcwd()) for path in fnames.values()]
    if(len(fnames)>0):
        if(type_of_script()=="terminal"):
            showTable([list(fnames.keys()),relative_paths],["FileName","Location"])
        else:
            showTables([list(fnames.keys()),relative_paths],XLables=["FileName","Location"],preview=len(fnames)+5)

    return list(fnames.values())


def ReadLas(fname):
    Data=read(fname)

    print("[IO] Reading %s....."% (fname),end='')
    #Collect import parameters
    param=Params()
    param.fname=fname
    param.Depth=[Data.well.STRT.value,Data.well.STOP.value]
    param.Depth_step=Data.well.STEP.value
    param.NULL_Val=Data.well.NULL.value
    param.WellName=Data.well.well.value

    #Collect useful information for plot and post-processing
    for key,value in Data.items():
        index=np.where(np.isnan(value)==False)[0]
        param.NonNanDict[key]=index

        param.CurveNames.append(key)
        param.Units.append(Data.curves[key].unit)
        param.Comments.append(Data.curves[key].descr)
        minDepth,maxDepth=Data[0][index[0]],Data[0][index[-1]]
        param.AvailDepth.append([minDepth,maxDepth])
        minVal,maxVal=np.nanmin(Data[key][index]),np.nanmax(Data[key][index])
        param.MinMaxVal.append([minVal,maxVal])


    #Find overlap depth intervals where all data available
    param.CommonDepth=findIntersection(param.AvailDepth[1:])

    #print(CurveNames)
    #print(Units)
    #print(Comments)
    
    NumLines_estimate=int((param.Depth[1]-param.Depth[0])/param.Depth_step+1)
    if NumLines_estimate!=len(Data[0]):
        print("\n[Warnning] Data size (%d,%d) is in-comptabile with depth/depth_step!" %(NumLines_estimate,len(Data[0])))

    print("Done!")

    #Create a plm_param copy in lasio class
    Data.plm_param=param
    return Data,param

def printLas(param):
    #Print las param
    print("[LAS Info]")
    print("Well Name=",param.WellName)
    print("Start/Step/End Depth=(%lf:%lf:%lf)"
        %(param.Depth[0],param.Depth_step,param.Depth[1]))
    print("NULL value=",param.NULL_Val)
    print("Common Depth=",param.CommonDepth)

    #print las information
    showTables([param.CurveNames,param.AvailDepth,param.MinMaxVal,param.Units,param.Comments],
       XLables=["Curves","Available Depth (Non-NULL)","Raw Min/Max Val","Unit","Comments"],preview=len(param.Units)+5)


