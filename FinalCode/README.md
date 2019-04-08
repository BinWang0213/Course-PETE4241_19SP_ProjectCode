# PETE4241_19SP_ProjectCode

PyLasMech is a simple tool to read well log data (ASCII LAS) and compute geo-mechanical parameters (S1, S2, S3, UCS, E, ν, Pp, and ϕ).

Currently, it support following features

	* 1. Read arbitrary well log data (ASCII LAS file) using lasio (https://github.com/kinverarity1/lasio)
	* 2. Plot and visualize the well logs
	* 3. Compute geo-mechanical parameters
		* Pore pressure, Pp
		* Porosity, ϕ
		* Young's Modulus, E
		* Possion ratio, v
		* Unconfined compressive strength, UCS
		* [TODO] Principle Stress, S1, S2, S3

## Examples

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
