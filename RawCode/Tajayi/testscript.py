# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:02:26 2019

@author: tajayi3
"""

from wellPlot import *

tre = wellPlot("GOMData.txt",1.7,1,1000)
SvGOM = tre.vertical_Stress()
HydroGOM = tre.hydro_Pressure()
gradGOM = tre.gradVSD()
poroGOM = tre.porosity()


tre2 = wellPlot("PythonBarnett.txt",1.8778)
SvBarnett = tre2.vertical_Stress()
HydroBarnett = tre2.hydro_Pressure()
gradBarnett = tre2.gradVSD()
poroBarnett = tre2.porosity()
blockBarnett = tre2.block_den(1402,9692,9807,12157)

tre3 = wellPlot("VolvePython.txt",1.8778)
SvVolve = tre3.vertical_Stress()
HydroVolve = tre3.hydro_Pressure()
gradVolve = tre3.gradVSD()
poroVolve = tre3.porosity()

tre4 = seismicData("HW3Data.txt",1.7)
HydroBarnett4 = tre4.hydro_Pressure()
poro4 = tre4.porosity()
shear4 = tre4.shearwave()
comp4 = tre4.compwave()
