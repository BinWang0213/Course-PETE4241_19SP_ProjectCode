import matplotlib.pyplot as plt
import numpy as np

from .utils import setPlotStyle,findUnion


ColorScheme=['tab:blue', 'tab:green', 'tab:red', 'tab:orange','tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
#['b', 'g','k', 'r', 'c']

def setCurveLim(ax,Curve,CurveName):
    
    lim=[]
    LowerLimit=-99999999
    UpperLimit=99999999
    #Set general data limit
    if(CurveName=="RHOB"):
        LowerLimit=0
        UpperLimit=10
    elif(CurveName=="DT"):
        LowerLimit=0
        UpperLimit=1000
    elif(CurveName=="DTS"):
        LowerLimit=0
        UpperLimit=1000
    elif(CurveName=="NPHI"):
        LowerLimit=0
        UpperLimit=1.0

    lim=[max(LowerLimit,np.nanmin(Curve)),min(UpperLimit,np.nanmax(Curve))]
    print("\t",CurveName,"Corrected Min/Max Val",lim)
    ax.set_xlim(lim)

def plotLogs(LogData,CurveNames,Depth_Range=None,NumFigCurves=2):
    #https://github.com/petroGG/Basic-Well-Log-Interpretation/blob/master/Basic%20well%20log%20interpretation.ipynb
    #Up to triple Log plot generator

    param=LogData.plm_param
    #Remove non-existed name
    AvailNames=param.CurveNames
    PlotNames=[x for x in CurveNames if x in AvailNames]
    
    #Find reasonable depth range for all available variables
    PlotNamesIdx=[AvailNames.index(name) for name in PlotNames]
    AvailDepths=[param.AvailDepth[idx] for idx in PlotNamesIdx]
    if Depth_Range is None:
        Depth_Range=findUnion(AvailDepths)
        print("\tAuto Depth Range=",Depth_Range,"for ",PlotNames)
    #print(PlotNames,AvailNames)
    #print(PlotNamesIdx,AvailDepths)


    setPlotStyle()
    NumCurves=len(PlotNames)
    top_depth,bottom_depth=Depth_Range
    Data=LogData

    #Prepare the figure format
    NumCols=np.ceil(NumCurves/NumFigCurves)
    NumCols=int(NumCols)
    UnitFigWidth=3.5
    UnitFigHeight=10
    fig, axs = plt.subplots(nrows=1, ncols=NumCols, figsize=(UnitFigWidth*NumCols,UnitFigHeight), sharey=True)
    if(NumCols==1):  axs=[axs]
    fig.suptitle("Well %s\n%s"%(param.WellName,param.fname))
    fig.subplots_adjust(top=0.8,wspace=0.1)


    #General setting for all axis    
    for ax in axs:
        ax.set_ylim(top_depth,bottom_depth)
        ax.invert_yaxis()
        ax.yaxis.grid(True)
        ax.get_xaxis().set_visible(False)
    axs[0].set_ylabel("Depth")
    


    index=np.where(((Data[0]>=top_depth) & (Data[0]<=bottom_depth)))[0]
    Depth=Data[0][index]

    curveID=0
    for col in range(NumCols):#col by col plot
        for i in range(NumFigCurves):
            if(curveID>=NumCurves): break
            CurveName=PlotNames[curveID]
            Curve=Data[CurveName][index]
            color=ColorScheme[curveID]
            #print(CurveName,Depth,np.nanmin(Curve),np.nanmax(Curve))

            ax=axs[col].twiny()
            ax.plot(Curve, Depth, color)

            setCurveLim(ax,Curve,CurveName)
            #ax.set_xlim(np.nanmin(Curve),np.nanmax(Curve))
            ax.spines['top'].set_position(('outward',40*i))
            ax.spines['top'].set_color(color)
            ax.set_xlabel(CurveName,color=color)    
            ax.tick_params(axis='x',color=color)
            ax.grid(True)

            curveID+=1
    
    return fig
