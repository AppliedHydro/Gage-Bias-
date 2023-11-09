## Contents of Original Attribute File
The following contents are necessary components of the data file loaded into the placement analysis R file. Refer to Attribute_COLUMN_INFO.xlsx

1. Sorting ID, GRADES ID, HydroATLAS ID
2. GRADES/MERIT Data
3. HydroATLAS attributes
4. GloRIC data (?)
5. Gage data (Gage_No, lat, long, distance (?), noFlowGauge (1 = intermittent, 0 = perennial)
6. GRADES flow permanence (fPermMQ)

## Process for assembling data package for analysis R script

1. Filter streamflow catalog dataset to subset you want (see Catalog_Subsetting.py)
2. Take main HydroATLAS attribute file and clip out old gage data (stationid, lat, long, distance) so that streamflow catalog dataset can be loaded into it after being merged with GRADES river segments. the COMID from the merge of gage data and GRADES will be used to merge the gage dataset into the HydroATLAS attributes.
3. Use Arcgis Pro to clip GRADES dataset to study area before merging gages. The GRADES dataset is quite large as it spans the entire globe so this step helps release computer memory for more rapid processing times.
4. Use join_gauge_GRADES.py to join gages and GRADES data - gage variables should include Gage_No, lat, and long. The output will have an excel sheet with COMID of GRADES river segment and that associated nearest streamflow gage<sup>1</sup> with location data. This COMID will be the merge vector for joining GRADES with HydroATLAS
5. Use Hydro_attr_merge.py to clip HydroATLAS attributes to study area.
6. 

## Notes

<sup>1</sup>     The current analysis R script is created in such a way that it only supports one gauge per GRADES river segment. Because the gage records of the streamflow catalog are significantly denser that the original gage placement analysis, this is going to yield less-accurate biases, especially in the case of many gages being grouped closely together. To improve our analysis, this factors should be addressed. The current work-around is using a filtering script to only include one gage per GRADES segment and remove any duplicate COMID's.

The freshwater ecoregions variable has been omitted from placement analysis. This will be updated once we have decided on a 
standard for assigning habitat types to gage locations.

Need to re-run noFlow script to update flow permanence records for GRADES river segments - last update was in 2021.
