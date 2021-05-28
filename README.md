
# Project Title

**Description**:  
Calculates the topographic wetness index (TWI) for Topmodel (version 0)
This code:
1) Download data from http://web.corral.tacc.utexas.edu/nfiedata/HAND/ for multiple HUC06 
2) Allows the use of 10 or 30 meters DEM
3) Calculate a raster with the topographic wetness index (TWI) using TauDEM
4) For each sub-basin in the HUC06, calculate the TWI histogram (maximum 30 classes)
5) Generates the subcat.dat file needed to run topmodel - the file name contains the ID of the sub-basin. 

## Dependencies

 This code was tested in linux

# Software Requirements:
 TauDEM (which requires gdal, mpiexec,... see https://github.com/dtarb/TauDEM)
 python if the TWI histogram per basin will be created. Anaconda distribution was used but is not a requirement.
 curl to download the data

# Data Requirements:
hydrofabrics if the TWI histogram per basin will be created

## Usage
Edit the workflow_hand_twi_giuh.env file
 - specify directories, HUC06, resolution (10 or 30 meters DEM), environmental variables

Run: source workflow_hand_twi_giuh.sh 

## Open source licensing info


## Credits and references


