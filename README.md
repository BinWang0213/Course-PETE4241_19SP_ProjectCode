# PETE4241_19SP_Project
Bin Wang (binwang.0213@gmail.com), Sulav Dhakal <sdhaka5@lsu.edu> and Temitope A Ajayi <tajayi3@lsu.edu>, Craft and Hawkins Department of Petroleum Engineering, Louisiana State University, Baton Rouge, US


As a group, compare your Python codes for homeworks 1 – 4 with those of the other graduate students and figure out the sources of the differences. 

### Q1. As a group, compare your Python codes for homeworks 1 – 4 with those of the other graduate students and figure out the sources of the differences.

- [x] 1.1 Fix any typos or bugs in your codes
- [x] 1.2 Extend your python code to be able to read in well logs from multiple wells and perform all the calculations in homeworks 1 through 3.
- [x] 1.3 Compute all the components of the MEM for all the wells in the Volve field (as in Homeworks 1-3) 
- [x] 1.4 Explore the given flow simulation data (CMG), and for each well in the reservoir simulation model, estimate the values of S1, S2, S3, UCS, E, ν, Pp, and ϕ against depth and at the depth interval (or resolution) of the well logs.
- [x] 1.5 Also estimate the block or average values of S1, S2, S3, UCS, E, ν, Pp, and ϕ for each grid block through which the well passes.

<p align="center">
  <img src = "https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/blob/master/FinalCode/output/GeoMech/15_9-F-14_GeoMechTVD.png" height="600">
</p>

- [x] 1.6 Compare your estimated porosity and pore pressure values with the values in the reservoir simulation model.

<p align="center">
  <img src = "https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/blob/master/Results/Log_CMG_Compare/I-F-5_POROcompare.png" height="400">
</p>

* Check figures @ https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/tree/master/Results/GeoMech
* Check figures @ https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/tree/master/Results/Log_CMG_Compare

### Q2. Submit one Excel file with the following tabs:

- [x] 2.1 A tab with the following columns: X, Y and Z co-ordinates of the centroid of the cells in
each layer through which the well passes, as well as the corresponding values of S1, S2,
S3, UCS, E, and 𝜈 for this cell (computed in 1 v above).
- [x] 2.2 A second tab with the X, Y and Z co-ordinates of the centroid of all the cells in the CMG
simulation data file given. 

* Download spreadsheets @ https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/blob/master/Results/CMGWell_Geomech.xlsx
* Download spreadsheets @ https://github.com/BinWang0213/PETE4241_19SP_ProjectCode/blob/master/Results/cmg_all_cells.xlsx

### Q3. Using the CMG reservoir simulation model provided, perform reservoir simulation for Volve field.

- [ ] 3.1 Perform flow simulator using IMEX and compare your well production performance forecasts with those in the “Volve Sim model and
HM per jan-16” powerpoint slides uploaded under Topic 11.

- [ ] 3.2 Using the CMG IMEX documentation on Geomechanics and the example simulation data
files that comes with your CMG installation (typically in C:\Program
Files(x86)\CMG\IMEX\2017.10\TPL\gmc), modify the CMG_gmc.dat file in the Volve CMG
folder to perform a coupled geomechanics and flow simulation.

- [ ] 3.3 Compare your results from the coupled geomechanics and flow simulation with the
original results from the flow simulation only.

Large CMG simulation file can be shared by https://filestogeaux.lsu.edu/