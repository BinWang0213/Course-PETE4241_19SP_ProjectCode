from math import log10
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import random
import string
from numpy import *
import numpy.matlib

class wellPlot(object):
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
        self.depthm = self.depth*0.3048;
        self.densitym = self.density * 1000;
        
    
    def vertical_Stress(self):
        numel = len(self.depth)
        macro = np.diff(self.depthm);
        Sv = np.zeros(numel, dtype = float) 
        if self.densea == 0:
            Sv[0] = (self.densed * self.depthm[0]  *self.gravity)/10**6;
            for i in range(1, numel):
                Sv[i] = (self.densitym[i]*macro[i-1]*self.gravity)/10**6;
            Svsum = np.cumsum(Sv, dtype=float) 
        if self.densea != 0:
            Svfloor = (self.densea * self.seafloor *self.gravity)/10**6;
            Svsed = (((self.densed+self.densitym[0])/2) *  (self.depthm[0]-self.seafloor) *self.gravity)/10**6; 
            Sv[0] = Svfloor + Svsed;
            for i in range(1, numel):
                Sv[i] = (((self.densitym[i]+self.densitym[i-1])/2)*macro[i-1]*self.gravity)/10**6;
            Svsum = np.cumsum(Sv, dtype=float) 
        return Svsum
    
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
    
#    def gradVSD(self):
#        numel = len(self.depth)
#        Grad = np.zeros(numel, dtype = float) 
#        depthkm = self.depthm/1000
#        Grad = np.diff(self.vertical_Stress())/np.diff(depthkm);
#        return Grad
    
    def gradVSD(self):
        Grad = (1000 * self.vertical_Stress()) / (self.depthm);
        return Grad
    
    def porosity(self):
        Poro = (self.density - self.densmatr) /(self.denwaters-self.densmatr);
        for i in range(1, len(Poro)):
            if Poro[i]<0:
                Poro[i]=0
        return Poro
    
    def block_den(self,firstp,secondp,thirdp,fourthp):
        numel = len(self.depth)
        block1 = self.density[0:firstp];
        avgblock1 = mean(block1);
        rela1 = np.tile(avgblock1,[(firstp+1),1]);
        block2 = self.density[(firstp+1):secondp];
        avgblock2 = mean(block2);
        rela2 = np.tile(avgblock2,[(secondp-firstp),1]);
        block3 = self.density[(secondp+1):thirdp];
        avgblock3 = mean(block3);
        rela3 = np.tile(avgblock3,[(thirdp-secondp),1]);
        block4 = self.density[(thirdp+1):fourthp];
        avgblock4 = mean(block4);
        rela4 = np.tile(avgblock4,[(fourthp-thirdp),1]);
        block5 = self.density[(fourthp+1):numel];
        avgblock5 = mean(block5);
        rela5 =np.tile(avgblock5,[(numel-fourthp-1),1]);
        rela = np.concatenate((rela1 , rela2,rela3,rela4,rela5), axis=None)
        
        return rela
        



