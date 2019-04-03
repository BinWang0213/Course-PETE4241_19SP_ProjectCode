from math import log10
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import random
import string
from numpy import *
import numpy.matlib

class seismicData(object):
    def __init__(self, filename,densed,densea=0,seafloor=0,denwaters =1,densmatr =2.7,gravity =10):
        self.filename = filename
        self.densea = densea * 1000
        self.densed = densed * 1000
        self.gravity = gravity
        self.denwaters = denwaters
        self.denwater = denwaters * 1000
        self.densmatr = densmatr
        self.seafloor = seafloor *0.3048
        datanumpy = loadtxt(self.filename)
        self.depth = datanumpy[:,0];
        self.density = datanumpy[:,1];
        self.delTcomp = datanumpy[:,2];
        self.depthm = self.depth*0.3048;
        self.densitym = self.density * 1000;
        self.delTshear = datanumpy[:,3];
        
    
    def hydro_Pressure(self):
        numel = len(self.depth)
        macro = np.diff(self.depthm);
        Sv = np.zeros(numel, dtype = float) 
        if self.densea == 0:
            Sv[0] = (self.denwater * self.depthm[0]  *self.gravity)/10**6;
            for i in range(1, numel):
                Sv[i] = (self.denwater*macro[i-1]*self.gravity)/10**6;
            Svsum = np.cumsum(Sv, dtype=float) 
        if self.densea != 0:
            Sv[0] = (self.denwater * self.depthm[0]  *self.gravity)/10**6;
            for i in range(1, numel):
                Sv[i] = (self.denwater*macro[i-1]*self.gravity)/10**6;
            Svsum = np.cumsum(Sv, dtype=float) 
        return Svsum
    
    def porosity(self):
        Poro = (self.density - self.densmatr) /(self.denwaters-self.densmatr);
        for i in range(1, len(Poro)):
            if Poro[i]<0:
                Poro[i]=0
        return Poro
    
    def compwave(self):
        numel = len(self.depth)
        velComp = np.zeros(numel, dtype = float) 
        velComp = self.delTcomp / (1000000*0.3048)
        velComp = 1/velComp
        
        return velComp
    
    def shearwave(self):
        numel = len(self.depth)
        velShear = np.zeros(numel, dtype = float) 
        velShear = self.delTshear / (1000000*0.3048)
        velShear = 1/velShear
        
        return velShear
    
    def shearModulus(self):
        shearModulu = (self.velShear() ** 2) * self.densitym
        
        return shearModulu
    
    def bulkModulus(self):
        bulkModulu = ((self.velComp() ** 2) * self.densitym) - ((4*self.shearModulus())/3)
        
        return bulkModulu 
    
    def poissonRatio(self):
        poissonRati = ((3*self.bulkModulus()) - (2*self.shearModulus())) / (2*((3*self.bulkModulus())+self.shearModulus()))
        
        return poissonRati 
    
    def youngModulus(self):
        youngModulu = (2*self.shearModulus() * (1+self.poissonRatio())) / 1000000
        
        return youngModulu 
    
        



