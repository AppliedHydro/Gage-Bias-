## Contents of Original Attribute File
The following contents are necessary components of the data file loaded into the placement analysis R file. Refer to Attribute_COLUMN_INFO.xlsx

1. Sorting ID, GRADES ID, HydroATLAS ID
2. GRADES/MERIT Data
3. HydroATLAS attributes
4. GloRIC data (?)
5. Gage data (Gage_No, lat, long, distance (?), noFlowGauge (1 = intermittent, 0 = perennial)
6. GRADES flow permanence (fPermMQ)

## Process for assembling data package for analysis R script

1) Filter streamflow catalog dataset to subset you want (see Catalog_Subsetting.py)

2) Use join_GRADES_HydroATLAS.py to join GRADES data with HydroATLAS attributes. Once the output file is generated, the data from
the HydroATLAS attribute file can be joined to the GRADES segments using HydroATLAS REACH_ID variable. This will yield a dataset with 
GRADES segments (crop to study area - Idaho, Washington, Oregon) and associated HydroATLAS variables to be used for analysis.

3) Join catalog gages to GRADES river segments, including Gage_No, lat, and long with join_gauge_GRADES.py 

## Notes

The current analysis R script is created in such a way that it only supports one gauge per GRADES river segment. Because the gage records of the streamflow catalog are significantly denser that the original gage placement analysis, this is going to yield less-accurate biases, especially in the case of many gages being grouped closely together. To improve our analysis, this factors should be addressed. The current work-around is using a filtering script to only include one gage per GRADES segment and remove any duplicate COMID's.

The freshwater ecoregions variable has been omitted from placement analysis. This will be updated once we have decided on a 
standard for assigning habitat types to gage locations.

Need to re-run noFlow script to update flow permanence records for GRADES river segments - last update was in 2021.
