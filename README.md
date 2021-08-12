
# Project Title

**Description**:  
Calculates the topographic wetness index (TWI) for Topmodel (version 0) and GIUH for the CFE model. 

This code:
1) Download data from http://web.corral.tacc.utexas.edu/nfiedata/HAND/ for multiple HUC06 
2) Allows the use of 10 or 30 meters DEM
3) Calculate a raster with the topographic wetness index (TWI) using TauDEM
4) For each sub-basin in the HUC06, calculate the TWI histogram (maximum 30 classes)
5) Generates the subcat.dat file needed to run topmodel - the file name contains the ID of the sub-basin. 
6) Generates an improved representation of the river network.
7) Calculates time of travel in each pixe based on:
7.1) A constant velocity model (channel, gully and overland flow).
7.2) The model proposed by Wong, 1997* and a constant velocity for the channel
8) For each sub-basin in the HUC06, calculate the GIUH histogram (hourly)
9) Generates the parameter file for CFE including the GIUH. 

*Wong, T. S., & Chen, C. N. (1997). Time of concentration formula for sheet flow of varying flow regime. Journal of Hydrologic Engineering, 2(3), 136-139.

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

## Future improvements
1) Use dropanalysis to determine the correct threshold to generate the river network
2) Separate the channel and overland flow GIUH in CFE. Overland flow depends on the rain rate, slope, land cover, and upstream area. Channel velocity can be estimated using the USGS river measurements data. 
 
## Credits and references


