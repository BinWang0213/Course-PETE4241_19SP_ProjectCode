# PETE4241_19SP_ProjectCode

As a group, compare your Python codes for homeworks 1 – 4 with those of the other graduate students and figure out the sources of the differences. 

- [ ] Fix any typos or bugs in your codes 
- [ ] Extend your python code to be able to read in well logs from multiple wells and perform all the calculations in homeworks 1 through 3.
- [ ] Compute all the components of the MEM for all the wells in the Volve field (as in Homeworks 1-3) 
- [ ] Explore the given flow simulation data (CMG), and for each well in the reservoir simulation model, estimate the values of S1, S2, S3, UCS, E, ν, Pp, and ϕ against depth and at the depth interval (or resolution) of the well logs.
- [ ] Also estimate the block or average values of S1, S2, S3, UCS, E, ν, Pp, and ϕ for each grid block through which the well passes.
- [ ] Compare your estimated porosity and pore pressure values with the values in the reservoir simulation model.

## Work breakdown

- [ ] 1.1 Compile/Convert  all well log data in Volve field into ASCII LAS file using Schlumberger Log Data Toolbox
- [ ] 1.2 Find/Compile all equation empirical constants from our homeworks suitable for Volve field
- [ ] 2.1 Write a general LAS reader to read all well logs in Volve field
- [ ] 2.2 Write a spreadsheet exporter to output above parameters into spreadsheet.
- [ ] 3. Write a general and verified computation tool to calculate all parameters (S1, S2, S3, UCS, E, ν, Pp, and ϕ) in HW1-3
