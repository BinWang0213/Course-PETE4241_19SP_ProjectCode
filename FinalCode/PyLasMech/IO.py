
import sys,os
import numpy as np
sys.path.append(os.path.realpath('..'))

from .externalLib.lasio import read,LASFile
from .utils import showTable,showTables,findIntersection,type_of_script,fillNanByInterp


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
    
    def getCurveIndex(self,CurveName):
        #Get the index of a curve
        return self.CurveNames.index(CurveName)

    def getNonNanIndex(self,Data,CurveName):
        AvailDZ=self.AvailDepth[self.getCurveIndex(CurveName)]
        return np.where(((Data[0]>=AvailDZ[0]) & (Data[0]<=AvailDZ[1])))[0] # first curve is always the DEPTH

    def getCommonNonNanIndex(self,Data,CurveNames):
        #Get common Non-nan index from a list of curves 
        #param.getCommonNonNanIndex(l,["RHOB","DT","DTS"])
        
        CurveIdxs=[self.getNonNanIndex(Data,name) for name in CurveNames if name in self.CurveNames]
        IdxRanges=[[Idx[0],Idx[-1]] for Idx in CurveIdxs]
        CommonRange=list(findIntersection(IdxRanges))
        CommonRange[-1]+=1
        CommonRange=np.array(CommonRange,dtype=int)

        RawCommonIdxs=np.arange(*CommonRange,dtype=int)

        #Remove nan index within the a continuos range
        for name in CurveNames:
            if name in self.CurveNames:
                CommonData=Data[name][RawCommonIdxs]
                inBetweenNan=list(np.where(np.isnan(CommonData)==True)[0])
                if(len(inBetweenNan)>0):
                    print(name,"[Warning] has %d NAN values in between" %(len(inBetweenNan)))
                    Data[name][RawCommonIdxs]=fillNanByInterp(Data[name][RawCommonIdxs])

        return RawCommonIdxs

    def getNonNanCurve(self,Data,CurveName):
        #Get the non-Nan value of a curve
        #AvailDZ=self.AvailDepth[self.getCurveIndex(CurveName)]
        #NonNanIdx=np.where(((Data[0]>=AvailDZ[0]) & (Data[0]<=AvailDZ[1])))[0] # first curve is always the DEPTH
        NonNanIdx=self.getNonNanIndex(Data,CurveName)
        return Data[0][NonNanIdx],Data[CurveName][NonNanIdx]

def append_Params(param,DEPTH,CurveName,data,unit,descr):
    #Append a curve into class Param data structure
    
    #Find non-nan value index
    index=np.where(np.isnan(data)==False)[0]
    param.NonNanDict[CurveName]=index

    #Append parameters
    param.CurveNames.append(CurveName)

    #normalize the unit
    if(unit in ["US/F","US/FT","US/F","us/ft"]): unit="us/ft"
    if(unit in ["G/C3","g/cm3","G/CC"]): unit="g/cm3"
    if(unit in ["M"]):unit="m"
    if(unit in ["F","FT","ft"]): unit="ft"
    param.Units.append(unit)
    param.Comments.append(descr)
    minDepth,maxDepth=DEPTH[index[0]],DEPTH[index[-1]]
    param.AvailDepth.append([minDepth,maxDepth])
    minVal,maxVal=np.nanmin(data[index]),np.nanmax(data[index])
    param.MinMaxVal.append([minVal,maxVal])


#-------------------------Key Functions----------------------------
def FileFinder(path="../Data/",fext=".las"):
    #Search all log files from the folder and subfolder
    DataFolder=os.path.abspath(path)
    fnames={}

    for root, dirs, files in os.walk(DataFolder):
        for file in files:
            if file.lower().endswith(fext):
                fnames[file]=os.path.join(root, file)
    
    print("[IO] Found %d log files" %(len(fnames)))

    #print relative path looks better than absolute path
    relative_paths = [os.path.relpath(path, os.getcwd()) for path in fnames.values()]
    if(len(fnames)>0):
        if(type_of_script()=="terminal"):
            showTable([list(fnames.keys()),relative_paths],["FileName","Location"],preview=len(fnames)+5)
        else:
            showTables([list(fnames.keys()),relative_paths],XLables=["FileName","Location"],preview=len(fnames)+5)

    return list(fnames.values())


def ReadLas(fname):
    Data=read(fname)

    print("[IO] Reading %s....."% (fname))
    #Collect import parameters
    param=Params()
    param.fname=fname
    param.Depth=[Data.well.STRT.value,Data.well.STOP.value]
    param.Depth_step=Data.well.STEP.value
    param.NULL_Val=Data.well.NULL.value
    param.WellName=Data.well.well.value.replace("/","_") #replace back slash in well name

    #Collect useful information for plot and post-processing
    for key,value in Data.items():
        '''
        index=np.where(np.isnan(value)==False)[0]
        param.NonNanDict[key]=index

        param.CurveNames.append(key)
        param.Units.append(Data.curves[key].unit)
        param.Comments.append(Data.curves[key].descr)
        minDepth,maxDepth=Data[0][index[0]],Data[0][index[-1]]
        param.AvailDepth.append([minDepth,maxDepth])
        minVal,maxVal=np.nanmin(Data[key][index]),np.nanmax(Data[key][index])
        param.MinMaxVal.append([minVal,maxVal])
        '''
        append_Params(param,Data[0],key,value,Data.curves[key].unit,Data.curves[key].descr)

    #Find overlap depth intervals where all data available
    param.CommonDepth=findIntersection(param.AvailDepth[1:])

    #print(CurveNames)
    #print(Units)
    #print(Comments)
    
    NumLines_estimate=int((param.Depth[1]-param.Depth[0])/param.Depth_step+1)
    if NumLines_estimate!=len(Data[0]):
        print("[Warnning] Data size (%d,%d) is in-comptabile with depth/depth_step!" %(NumLines_estimate,len(Data[0])))

    print("Done!")

    #Create a plm_param copy in lasio class
    Data.plm_param=param
    return Data#,param

def createLas(WellName,CurveNames,CurveData,CurveUnit):
    #Create a LAS data using lasio
    l=LASFile()
    l.well["WELL"]=WellName
    NumCurves=len(CurveNames)
    for i in range(NumCurves):
        l.add_curve(CurveNames[i],CurveData[i],unit=CurveUnit[i],descr="User PyLasMech curve")
    return l

def saveLas(Data,fname):
    with open(fname, mode="w") as f: # Write LAS file to disk\n"
        Data.write(f)
    print("Write Las file @",fname)

def printLas(Data):
    param=Data.plm_param
    #Print las param
    print("[LAS Info]")
    print("Well Name=",param.WellName)
    print("Start/Step/End Depth=(%lf:%lf:%lf)"
        %(param.Depth[0],param.Depth_step,param.Depth[1]))
    print("NULL value=",param.NULL_Val)
    print("Common Depth=",param.CommonDepth)

    #print las information
    if(type_of_script()=="terminal"):
        showTable([param.CurveNames,param.AvailDepth,param.MinMaxVal,param.Units,param.Comments],
        ["Curves","Available Depth (Non-NULL)","Raw Min/Max Val","Unit","Comments"],preview=len(param.Units)+5)
    else:
        showTables([param.CurveNames,param.AvailDepth,param.MinMaxVal,param.Units,param.Comments],
        XLables=["Curves","Available Depth (Non-NULL)","Raw Min/Max Val","Unit","Comments"],preview=len(param.Units)+5)


def appendCurve(Data,CurveName,data,unit="m",descr="User PyLasMech curve",dataIndex=[]):
    #Add a new curve into pylasmech system
    if(len(data)!=len(Data[0]) and len(dataIndex)>0):
        print("Input data size(%d) < DEPTH size (%d), NULL value (nan) will be added"%(len(data),len(Data[0])))
        Newdata=np.ones(len(Data[0]))*np.nan
        Newdata[dataIndex]=data
        data=Newdata
    
    if(CurveName in Data.plm_param.CurveNames):
        print("[IO] Curve %s is already existed! Update the data array"%(CurveName))
        Data.delete_curve(CurveName)
        Data.add_curve(CurveName, data, unit=unit, descr=descr)
        return

    #Append data into lasio
    Data.add_curve(CurveName, data, unit=unit, descr=descr)

    #Append data into pylasmech
    DEPTH=Data[0]
    append_Params(Data.plm_param,DEPTH,
                  CurveName,data,unit,descr)
    
    #Update overlap depth intervals where all data available
    Data.plm_param.CommonDepth=findIntersection(Data.plm_param.AvailDepth[1:])



    