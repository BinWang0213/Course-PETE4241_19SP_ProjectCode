# PETE4241_19SP_Project_Volve_Field_Data

### Well Log Data Summary Table

	Below 9 wells appears in CMG simulation model
| WellName |      LAS      |  RHOB |  DTC/DT | DTS | TVD|
|----------|----------------  |------------------- |--|--|--|
| 15_9-F4  |:heavy_check_mark:| :heavy_check_mark: |:heavy_check_mark:|:heavy_check_mark:|:x:|
| 15_9-F1B |:heavy_check_mark:| :heavy_check_mark: |:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
| 15_9-F5  | :heavy_check_mark:| :heavy_check_mark: |:heavy_check_mark:|:x:|:x:|
| 15_9-F1C | :heavy_check_mark:| :heavy_check_mark: |:x:|:x:|:heavy_check_mark:|
| 15_9-F11B| :heavy_check_mark:| :heavy_check_mark: |:x:|:x:|:heavy_check_mark:|
| 15_9-F12 | :heavy_check_mark:| :heavy_check_mark: |:heavy_check_mark:|:x:|:x:|
| 15_9-F14 |:heavy_check_mark:| :heavy_check_mark: |:heavy_check_mark:|:heavy_check_mark:|:x:|
| 15_9-F15C| :heavy_check_mark:| :heavy_check_mark: |:heavy_check_mark:|:x:|:x:|
| 15_9-F15D| :heavy_check_mark:| :heavy_check_mark: |:x:|:x:|:heavy_check_mark:|

### Fluid & Rock Properties in Volve Field

| Variables					|      Value      |  Unit |  Reference |
|----------					|---------------- |------------ |--|
| Water Density (![equation](https://latex.codecogs.com/png.latex?%24%5Crho_%7Bw%7D%24))  |1.0| g/cc |Ref.3|
| Grain Density (![equation](https://latex.codecogs.com/png.latex?%24%5Crho_%7Bma%7D%24))  |2.65| g/cc |Ref.3|
| Initial Porosity (![equation](https://latex.codecogs.com/png.latex?\phi_0))  |0.37| - |Ref.5|
| Compaction parameter (![equation](https://latex.codecogs.com/png.latex?\beta))  |0.0266| MPa |Ref.5|


### Petrophysics correlations for Volve Field

| Variables					|     Equation    | Unit|  Reference |
|----------					|---------------- |------------ |--|
| UCS  |![equation](https://latex.codecogs.com/png.latex?%24e%5E%7B-6.36&plus;2.45log%280.86V_p-1172%29%7D%24)|V_p(m/s), UCS(MPa)			|Ref.4|
| ![equation](https://latex.codecogs.com/png.latex?%24%5Cphi%24)  |TODO|TODO		|Ref.3|

### References

1. https://www.spec2000.net/05-abrev-log.htm
2. https://www.spec2000.net/05-logaliastable.htm
3. Sleipner Øst and Volve Model Hugin and Skagerrak Formation Petrophysical Evaluation, 2006 
4. Kalani, M., 2018. Multiscale seal characterization in the North Sea Implications from clay
sedimentology, well logs interpretation and seismic analyses
5. Karstens, J., 2015. Focused fluid conduits in the Southern Viking Graben and their implications for the
Sleipner CO2 storage project (Doctoral dissertation, Christian-Albrechts-Universität)
