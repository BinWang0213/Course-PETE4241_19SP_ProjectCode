# PETE4241_19SP_ProjectCode - PyLasMech

PyLasMech is a simple tool to read well log data (ASCII LAS) and compute geo-mechanical parameters (S1, S2, S3, UCS, E, ν, Pp, and ϕ).

Currently, it support following features

* 1. Read arbitrary well log data (ASCII LAS file) using lasio (https://github.com/kinverarity1/lasio)
* 2. Plot and visualize the well logs
* 3. Compute geo-mechanical parameters
	* 3.1 Pore pressure, Pp
	* 3.2 Porosity, ϕ
	* 3.3 Young's Modulus, E
	* 3.4 Possion ratio, v
	* 3.5 Unconfined compressive strength, UCS
	* 3.6 [TODO] Principle Stress, S1, S2, S3
* 4. Interpoate the grid block value based on calculated geo-mechanical parameters

## Examples-1 Well Log Visualization

```python
import PyLasMech as plm
LogFiles=plm.FileFinder("../Data/Petrophysics")
```
|    | FileName             | Location                                             |
|----|----------------------|------------------------------------------------------|
|  0 | 15_9-F-11B_INPUT.LAS | ..\Data\Petrophysics\15_9-F-11B\15_9-F-11B_INPUT.LAS |
|  1 | 15_9-F-12_INPUT.LAS  | ..\Data\Petrophysics\15_9-F-12\15_9-F-12_INPUT.LAS   |
|  2 | 15_9-F-14_INPUT.las  | ..\Data\Petrophysics\15_9-F-14\15_9-F-14_INPUT.las   |
```python
WellLog=plm.ReadLas(LogFiles[5])
plm.printLas(WellLog)
```
|    | Curves   | Available Depth (Non-NULL)   | Raw Min/Max Val      | Unit   | Comments                         |
|----|----------|------------------------------|----------------------|--------|----------------------------------|
|  0 | DEPTH    | [145.9, 3464.9]              | [145.9, 3464.9]      | M      | 0  Depth                         |
|  8 | DT       | [2998.5, 3424.6]             | [54.9283, 125.9827]  | us/ft  | 8  DT:COMPOSITE:rC:NONE:v1       |
|  9 | DTS      | [2999.0, 3424.7]             | [99.9092, 202.14]    | us/ft  | 9  DTS:COMPOSITE:rC:NONE:v1      |
| 17 | RHOB     | [3098.5, 3442.5]             | [2.1118, 3.0517]     | g/cm3  | 17  RHOB:COMPOSITE:rC:NONE:v1    |
```python
fig=plm.plotLogs(LogData=WellLog,CurveNames=["DT","DTS","RHOB","NPHI"])
```
<p align="center">
  <img src = "https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/blob/master/FinalCode/output/WellLog/15_9-F-14_log.png" height="600">
</p>

## Example-2 Geomechanical parameters calculation
```python
import PyLasMech as plm
LogFiles=plm.FileFinder("../Data/Petrophysics")

#RHOB DT DTS etc from Log
l=WellLog
param=l.plm_param
GeoMechParams={}
```
```python
NonNanIndex=param.getCommonNonNanIndex(l,["RHOB","DT","DTS"])
DZ=l[0][NonNanIndex]
RHOB=l["RHOB"][NonNanIndex]
DT=l["DT"][NonNanIndex]
DTS=l["DTS"][NonNanIndex]


#1. Overburden stress
Sv0=rho_w*g*z_w+RHOB_avg*g*(z_0-z_w)
Sv=[Sv0]+list(Sv0+integrate.cumtrapz(RHOB*g, DZ))
GeoMechParams["Sv"]=np.array(Sv)
GeoMechParams["Sv_grad"]=GeoMechParams["Sv"]/DZ

#2. Pore pressure
GeoMechParams["P_pore"]=rho_w*g*DZ

#3. Porosity
GeoMechParams["PORO"]=(rho_m-RHOB)/(rho_m-rho_w)

#4. Shear modulus (G,MPa), Possion ratio and Youngs Modulus (E, MPa)
Vp=1/DT
Vs=1/DTS

G=RHOB*Vs*Vs
GeoMechParams["v"]=(Vp**2-2*Vs**2)/2/(Vp**2-Vs**2)
GeoMechParams["E"]=2*G*(1+GeoMechParams["v"]) 

#5. UCS
GeoMechParams["UCS"]=np.exp(-6.36+2.45*np.log10(0.86*Vp-1172))*mega*Pa
```
```python
#Save Geomechanical parameters into log data
plm.appendCurve(l,'Sv', GeoMechParams["Sv"]/1e6, unit='MPa',descr='PyLasMech overburden stress',dataIndex=NonNanIndex)
plm.appendCurve(l,'P_pore', GeoMechParams["P_pore"]/1e6, unit='MPa',descr='PyLasMech pore pressure',dataIndex=NonNanIndex)
plm.appendCurve(l,'PORO', GeoMechParams["PORO"], unit='-',descr='PyLasMech porosity',dataIndex=NonNanIndex)

XLims={"P_pore":(10,90),"Sv":(10,90),"PORO":(0,0.5)}
fig=plm.plotLogs(LogData=l,CurveNames=GeoMechParams.keys(),XLims=XLims)
```

<p align="center">
  <img src = "https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/blob/master/FinalCode/output/GeoMech/15_9-F-14_GeoMech.png" height="600">
</p>
