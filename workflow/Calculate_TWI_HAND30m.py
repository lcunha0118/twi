# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 15:45:46 2021

@author: lcunha
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:58:36 2021

@author: lcunha
"""
import os
from osgeo import ogr
from osgeo.gdalconst import GA_ReadOnly
import matplotlib.pyplot as plt     
import sys 
import pandas as pd
sys.path.append("/home/west/Projects/IUH_TWI/")
import generate_twi_per_basin as ZS

HUCAr=['010100','010200','010300','010400','010500','010600','010700','010801','010802','010900','011000','041505']
HUCAr=['011000']

hydro_fabrics_input_dir="/home/west/Projects/hydrofabrics/20210511/"
Resolution=30
TauDEM_files_base_dir="/home/west/Projects/IUH_TWI/HAND_"+str(Resolution)+"m/"
check_file=0 # Check if all files for the hydrofabrics are available
output_flag=1 # output_flag=0 writes to Json File, output_flag=1 writes to subcat.dat

outputfolder_twi=hydro_fabrics_input_dir+"/TWI/"
if not os.path.exists(outputfolder_twi): os.mkdir(outputfolder_twi)

catchments = os.path.join(hydro_fabrics_input_dir, 'catchments_proj.geojson')
flowpaths = os.path.join(hydro_fabrics_input_dir, 'flowpaths.geojson')
 
CatIDdictAll={}
for HUC in HUCAr: 
    if(Resolution==30): file_name=HUC+"_30m"
    else: file_name=HUC
    TauDEM_files="/home/west/Projects/IUH_TWI/HAND_30m/"+HUC+"/"
    twi_raster = TauDEM_files+ file_name+"twi_cr.tif"
    slope_raster = TauDEM_files+ file_name+"slp_cr.tif"
    print (twi_raster)
    CatIDdict = ZS.generate_twi_per_basin(HUC,catchments,twi_raster,slope_raster,outputfolder_twi,output_flag,nodata_value=-999,buffer_distance=0.001)  
    #frames=[CatIDdictAll,CatIDdict]
    #CatIDdictAll=pd.concat(frames)
            
# Log File
if(check_file==1):
    plt.figure()
    vds = ogr.Open(catchments, GA_ReadOnly)  # TODO maybe open update if we want to write stats
    assert(vds)
    vlyr = vds.GetLayer(0)
    
    total = vlyr.GetFeatureCount(force = 0)
    vlyr.ResetReading()
    count = 0
    feat = vlyr.GetNextFeature()
    ncolsAr=[];catAr=[]
    NoFiles=[]
    while feat is not None:
        cat = feat.GetField('ID')
        count = count + 1          
        DatFile=os.path.join(outputfolder_twi,"cat-"+str(cat)+".dat")
        catAr.append(cat)
        if os.path.exists(DatFile): 
            TWI=pd.read_csv(DatFile, sep=' ',skiprows=3,skipfooter=3,header=None,engine='python')    
            TWI=TWI.rename(columns={TWI.columns[0]: "Freq",TWI.columns[1]: "TWI"})
            ncolsAr.append(len(TWI))
            TWI=TWI.sort_values(by=['TWI'], ascending=True)
            TWI['AccumFreq']=TWI["Freq"].cumsum()
            plt.plot(TWI['TWI'],TWI['AccumFreq'],'-')
        else:
            NoFiles.append(cat)
            ncolsAr.append(-9)
            #print ("File does not exist " + str(cat))
            #DirCat=os.path.join(outputfolder_twi, str(cat))
            #if not os.path.exists(DirCat): os.mkdir(DirCat)
            DatFile=os.path.join(outputfolder_twi,"cat-"+str(cat)+".dat")
            f= open(DatFile, "w")
            f.write("1  1  1\n")
            f.write("%s" %("Extracted study basin: " + str(cat) +"\n"))
            f.write("1 1\n")
            f.write("1.000000 50.500000\n")
            f.write("3\n")  
            f.write("0.0  500.  0.5  1000.  1.0  1500.\n") 
            f.write("$mapfile.dat\n") 
            f.close()        
        
        
        # CDFplot = CDF.plot(kind='scatter',x='TWI',y='AccumFreq',color='blue').get_figure()
        # df.interpolate(method='nearest')
        rvds = None
        mem_ds = None
        feat = vlyr.GetNextFeature()    
    
    plt.xlabel('TWI')
    plt.ylabel('CDF')

    plt.savefig(hydro_fabrics_input_dir+"twi_all.png",bbox_inches='tight')
    plt.close() 
    check_twi_data=pd.DataFrame({'cat':catAr, 'ncolsAr':ncolsAr})
   
    check_twi_data.to_csv(hydro_fabrics_input_dir+"twi_nclasses.txt")
    
    # textfile = open(hydro_fabrics_input_dir+"twi_missing.txt", "w")
    # for element in NoFiles:
    #     textfile.write(str(element) + "\n")
    #     NoFiles.append(cat)
    #     ncolsAr.append(-9)
    #     #print ("File does not exist " + str(cat))
    #     #DirCat=os.path.join(outputfolder_twi, str(cat))
    #     #if not os.path.exists(DirCat): os.mkdir(DirCat)
    #     DatFile=os.path.join(outputfolder_twi,"cat-"+str(element)+".dat")
    #     f= open(DatFile, "w")
    #     f.write("1  1  1\n")
    #     f.write("%s" %("Extracted study basin: " + str(element) +"\n"))
    #     f.write("%s" %"1 1\n")
    #     f.write("%s" %"1.000000 50.500000\n")
    #     f.write("3\n")  
    #     f.write("0.0  500.  0.5  1000.  1.0  1500.\n") 
    #     f.write("$mapfile.dat\n") 
    #     f.close()
            
    # textfile.close()
