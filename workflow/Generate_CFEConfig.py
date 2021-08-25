#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 15:45:17 2021

@author: west
"""

import pandas as pd
import os 
from osgeo import gdal, ogr
from osgeo.gdalconst import *

catchments="/home/west/Projects/hydrofabrics/20210511/catchments.geojson"
outputfolder_giuh_param_file="/home/west/Projects/hydrofabrics/20210511/width_function/"
outputfolder_giuh_config_file="/home/west/Projects/hydrofabrics/20210511/GIUH_30m_1/"

soil_params="/home/west/Projects/hydrofabrics/releases/beta/01a"
vds = ogr.Open(catchments, GA_ReadOnly)  
assert(vds)
vlyr =   vds.GetLayer(0)

skippednulgeoms = False
total = vlyr.GetFeatureCount(force = 0)
vlyr.ResetReading()
count = 0
feat = vlyr.GetNextFeature()

forcing_file="./forcings/cat58_01Dec2015.csv"
soil_params_depth=2.0
soil_params_b=4.05
soil_params_mult=1000.0
soil_params_satdk=0.00000338
soil_params_satpsi=0.355
soil_params_slop=1.0
soil_params_smcmax=0.439
soil_params_wltsmc=0.066
max_gw_storage=16.0
Cgw=0.01
expon=6.0
gw_storage=50
alpha_fc=0.33
soil_storage=66.7
K_nash=0.03
K_lf=0.01
nash_storage='0.0,0.0'
giuh_ordinates='0.06,0.51,0.28,0.12,0.03'
          
  
while feat is not None:
    cat = feat.GetField('ID')
    count = count + 1
             
    
    DatFile=os.path.join(outputfolder_giuh_param_file,"cat-"+str(cat)+"_giuh.csv")
    CDF=pd.from_csv(DatFile)             

    DatFile=os.path.join(outputfolder_giuh_config_file,"cat-"+str(cat)+"_bmi_config_cfe_pass.txt")
    f= open(DatFile, "w")
    string="forcing_file=BMI\nsoil_params.depth=2.0\nsoil_params.b=4.05\nsoil_params.mult=1000.0\nsoil_params.satdk=0.00000338\nsoil_params.satpsi=0.355\nsoil_params.slop=1.0\nsoil_params.smcmax=0.439\nsoil_params.wltsmc=0.066\nmax_gw_storage=16.0\nCgw=0.01\nexpon=6.0\ngw_storage=50%\nalpha_fc=0.33\nsoil_storage=66.7%\nK_nash=0.03\nK_lf=0.01\nnash_storage=0.0,0.0\n"
    f.write("%s" %(string))
    giuh="giuh_ordinates="+"{0:.2f}".format((round(CDF['Freq'].iloc[0],4)))
    for icdf in range(1,len(CDF)):
        giuh=giuh+","+"{0:.2f}".format((round(CDF['Freq'].iloc[icdf],4)))
    giuh =giuh+"\n"  
    f.write("%s" %(giuh))
    f.close()