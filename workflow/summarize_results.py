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


outputfolder_summary="/home/west/Projects/hydrofabrics/20210511/summary/"
if not os.path.exists(outputfolder_summary): os.mkdir(outputfolder_summary)
    
hydro_fabrics_input_dir="/home/west/Projects/hydrofabrics/20210511/"
Resolution=30
outputfolder_twi="/home/west/Projects/hydrofabrics/20210511/TWI_"+str(Resolution)+"m/TOPMODEL_cat_file/"

catchments = os.path.join(hydro_fabrics_input_dir, 'catchments_proj.geojson')
flowpaths = os.path.join(hydro_fabrics_input_dir, 'flowpaths.geojson')
 

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
        print ("File does not exist " + str(cat))
        #DirCat=os.path.join(outputfolder_twi, str(cat))
        #if not os.path.exists(DirCat): os.mkdir(DirCat)
        # DatFile=os.path.join(outputfolder_twi,"cat-"+str(cat)+".dat")
        # f= open(DatFile, "w")
        # f.write("1  1  1\n")
        # f.write("%s" %("Extracted study basin: " + str(cat) +"\n"))
        # f.write("1 1\n")
        # f.write("1.000000 50.500000\n")
        # f.write("3\n")  
        # f.write("0.0  500.  0.5  1000.  1.0  1500.\n") 
        # f.write("$mapfile.dat\n") 
        # f.close()        
    
    
    # CDFplot = CDF.plot(kind='scatter',x='TWI',y='AccumFreq',color='blue').get_figure()
    # df.interpolate(method='nearest')
    rvds = None
    mem_ds = None
    feat = vlyr.GetNextFeature()    

plt.xlabel('TWI')
plt.ylabel('CDF')

plt.savefig(outputfolder_summary+"twi_"+str(Resolution)+"all.png",bbox_inches='tight')
plt.close() 
check_twi_data=pd.DataFrame({'cat':catAr, 'ncolsAr':ncolsAr})
   
check_twi_data.to_csv(outputfolder_summary+"twi_nclasses_"+str(Resolution)+".txt")

# Read width function
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
        f = open(DatFile, "r")
        lines = list(f)
        WFline=lines[len(lines)-2].split(" ")
        WF=[];CDF=[]
        for i in range(0,len(WFline)-1):
             if(i % 2 == 0):
                 CDF.append(float(WFline[i]))
             else:
                 WF.append(float(WFline[i]))
            

        WF_df=pd.DataFrame({'WF_ordinates':CDF, 'dist_m':WF})       
        plt.plot(WF_df['dist_m'],WF_df['WF_ordinates'],'-')
        ncolsAr.append(len(WF_df))
    else:
        NoFiles.append(cat)
        ncolsAr.append(-9)
        print ("File does not exist " + str(cat))

    rvds = None
    mem_ds = None
    feat = vlyr.GetNextFeature()    

plt.xlabel('Distance to outlet (m)')
plt.ylabel('CDF')

plt.savefig(outputfolder_summary+"WF_"+str(Resolution)+"all.png",bbox_inches='tight')
plt.close() 
check_WF_data=pd.DataFrame({'cat':catAr, 'ncolsAr':ncolsAr})
   
check_WF_data.to_csv(outputfolder_summary+"WF_nclasses_"+str(Resolution)+".txt")

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

methodAr=[1]
for method in methodAr:
    outputfolder_giuh="/home/west/Projects/hydrofabrics/20210511/GIUH_"+str(Resolution)+"m_"+str(method)+"/CFE_config_file/"

    plt.figure()
    vds = ogr.Open(catchments, GA_ReadOnly)  # TODO maybe open update if we want to write stats
    assert(vds)
    vlyr = vds.GetLayer(0)
    
    total = vlyr.GetFeatureCount(force = 0)
    vlyr.ResetReading()
    count = 0
    feat = vlyr.GetNextFeature()
    ncolsAr=[];catAr=[];giuhAr=[]
    NoFiles=[]
    while feat is not None:
        cat = feat.GetField('ID')
        count = count + 1          
        DatFile=os.path.join(outputfolder_giuh,"cat-"+str(cat)+"_bmi_config_cfe_pass.txt")
        catAr.append(cat)
        if os.path.exists(DatFile): 
            #print (DatFile)
            # TWI=pd.read_csv(DatFile, sep=' ',skiprows=3,skipfooter=3,header=None,engine='python')    
            # TWI=TWI.rename(columns={TWI.columns[0]: "Freq",TWI.columns[1]: "TWI"})
            #ncolsAr.append(len(TWI))
            # TWI=TWI.sort_values(by=['TWI'], ascending=True)
            # TWI['AccumFreq']=TWI["Freq"].cumsum()
            
            with open(DatFile) as f:
                for line in f:
                    pass
                last_line = line
            f.close()
            giuh=last_line.split("giuh_ordinates=")[1].replace("\n","").split(",")
            
            
            giuh=[float(i) for i in giuh]
            giuh_df=pd.DataFrame({'giuh_ordinates':giuh, 'time_hours':range(1,len(giuh)+1)})
            giuh_df['AccumFreq']=giuh_df["giuh_ordinates"].cumsum()
            if(max(giuh_df['AccumFreq'])>1):
                print (str(Resolution) + " Method " +str(method) + " Larger than 1 : " + str(cat) )
            
            plt.plot(giuh_df['time_hours'],giuh_df['AccumFreq'],'-')
            giuhAr.append(giuh)
            ncolsAr.append(len(giuh))
        else:
            NoFiles.append(cat)
            ncolsAr.append(-9)
            # f= open(DatFile, "w")
            # string="forcing_file=BMI\nsoil_params.depth=2.0\nsoil_params.b=4.05\nsoil_params.mult=1000.0\nsoil_params.satdk=0.00000338\nsoil_params.satpsi=0.355\nsoil_params.slop=1.0\nsoil_params.smcmax=0.439\nsoil_params.wltsmc=0.066\nmax_gw_storage=16.0\nCgw=0.01\nexpon=6.0\ngw_storage=50%\nalpha_fc=0.33\nsoil_storage=66.7%\nK_nash=0.03\nK_lf=0.01\nnash_storage=0.0,0.0\n"
            # f.write("%s" %(string))
            # giuh="giuh_ordinates=0.06,0.51,0.28,0.12,0.03\n"
            # f.write("%s" %(giuh))
            # f.close()      
        
        
        # CDFplot = CDF.plot(kind='scatter',x='TWI',y='AccumFreq',color='blue').get_figure()
        # df.interpolate(method='nearest')
        rvds = None
        mem_ds = None
        feat = vlyr.GetNextFeature()    
    
    plt.xlabel('Travel time (hours)')
    plt.ylabel('CDF')

    plt.savefig(outputfolder_summary+"giuh_"+str(Resolution)+"all"+str(method)+".png",bbox_inches='tight')
    plt.close() 
    check_giuh_data=pd.DataFrame({'cat':catAr, 'ncolsAr':ncolsAr})
   
    check_giuh_data.to_csv(outputfolder_summary+"giuh_nclasses_"+str(Resolution)+"all"+str(method)+"txt")