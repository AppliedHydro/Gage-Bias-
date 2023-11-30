# StreamflowCatalog_PlacementBias
**Authors**
- Kendra Kaiser, Boise State University   | kendrakaiser@boisestate.edu
- Steven Schmitz, Boise State University  | stevenschmitz@u.boisestate.edu
  
This repository contains the gage data from the [Streamflow Catalog](https://github.com/AppliedHydro/StreamflowCatalog) project and all relevant files being used to replicate a placement bias assessment as seen in [Krabbenhoft et al (2022)](https://www.nature.com/articles/s41893-022-00873-0). Contained below are the:

1. overview
1. data sources
1. methods
1. source code

## Overview

[Krabbenhoft et al (2022)](https://www.nature.com/articles/s41893-022-00873-0) created a workflow process for assessing the placement bias of stream gages using a global stream gage dataset. 19 assorted attributes were selected as the independant variables in the study ranging from socioecological (population, GDP), hydrologic (perennial, non-perennial), and physiographic (mountainous, vegetation type) factors to determine those most instrumental in creating bias in the location and placement of stream gages. This project is predicated on the observation that are significant disparities in the placement of hydrologic gages across the world which impacts decisions made concerning water security, water conservation, and water-monitoring strategies. As a next step for the Streamflow Catalog project, we apply the same processes to the gage locations contained in the up-to-date catalog to obtain a placement bias for gages in the Pacific Northwest (Idaho, Washington, Oregon). The global bias assessment was conducted using 41,000 stream gage locations; the current streamflow catalog has 34,400 gages. The higher quantity of gages contained in a smaller geographic area will ideally produce a higher level of accuracy in the bias assessment. All data used is pubicly available and automations were performed using Python and R coding libraries. 

## Data Sources

### Global Reach-level A priori Discharge Estimates for Surface Water and Ocean Topography (GRADES)
A data set containing ~2.94 million vector river polylines and discharge estimates. GRADES is derived from the MERIT-Hydro model. More information can be found [here](https://www.reachhydro.org/home/records/grades)

### HydroATLAS
HydroATLAS is a global-ranging dataset that contains hydro-environmental characteristics for global river networks. More information can be found [here](https://www.hydrosheds.org/hydroatlas)

### Streamflow Catalog
All gage locations have been collected from the current version of the [Streamflow Catalog](https://scholarworks.boisestate.edu/redi_data/2/) -> [Git](https://github.com/AppliedHydro/StreamflowCatalog)) on which the authors are also the primary contributors. 

### Python, R, supplementary code
Ancillary scripts, methods, and data source links were obtained from the [public repository](https://github.com/dry-rivers-rcn/G4) of the Global Gauge Gaps Group (G4) Project.
the 
## Methods

This section details the pre-processing steps and methodological approach to performing the assessment bias. 

### i) Data Assemblage
The background variable data used to conduct the placement bias was assembled from two sources: the GRADES dataset and HydroAtlas. A compilation of 13 variables were chosed and were sourced from GRADES and HydroATLAS datasets and combined into a single dataset using the Python GeoPandas library for geospatial analysis. Specifically, spatial joins were used to assign HydroATLAS variables to GRADES river segments to enable comparison of gages to a single object with all pertinent variables rather than multiple objects in sequence. Prior to spatial joins, the 9 unique HydroATLAS datasets were combined into a single dataset, organized by location, with non-relevant data trimmed off for memory efficiency. The initial HydroATLAS dataset prior to processing was 456 GB in raw format. 

The GRADES river segments dataset encompassed the North American continent and was trimmed to our study area (The Pacific Northwest (PNW): Oregon, Washington, Idaho) using Arcgis Pro geospatial processing tools. The resulting dataset was 14,239 GRADES river segments.

To combine the datasets accurately, GeoPandas was used to create a series of points located at the center of each GRADES river segment that the HydroATLAS data could then be snapped based on 'nearest search' protocols.

The source material for our gage locations is from the [Streamflow Catalog](https://github.com/AppliedHydro/StreamflowCatalog). Data was procurred in excel format (.xlsx) and represents the most up-to-date version of the catalog, 9/7/2023, with approximately 34,000 streamflow gages and location data. For the purposes of this study, the dataset was trimmed to include only relevent variables.

### ii) Code Edits
Major script files to perform data leaning were obtained from the G4 Public Repository that contains source code used for initial placement analysis. Because the initial studies were conducted in a global study area, code corrections needed to be made to refine the working area of the scripts. Scripts were written in both Python and R, Python being used primarily for spatial analysis using the GeoPandas library. Additionally, file directories and loops needed to be rewritten to access files and quantities unique to our study area.

## Running the Code
This code uses datasets from 3 different locations and will need to be acquired and modified into the appropriate format to execute successfully. If you do not have the files, please refer to section i, Data Assemblage, for procurement information.

### Step 1. Gathering your Gage Dataset
1. Procure the Streamflow Catalog dataset from [Kendra Kaiser](kendrakaiser@boisestate.edu) or [Steven Schmitz](stevenschmitz@u.boisestate.edu).
2. Load the Catalog into Catalog_Subsetting.py. This script will filter the catalog based on variables that you provide. For instance, you can isolate gages by state, by Huc, or by ecoregion before conducting your placement analysis. Refer to the [subset options](https://github.com/AppliedHydro/Gauge-Placement-Analysis/blob/master/subset_options.xlsx) to see what variables are available for sorting. The output dataset will be a .csv file with the gages of choice.
3. Load the filtered Catalog into join_Gauge_GRADES.py along with the GRADES river segments from the appropriate shapefile (see Data Assemblage). This script geospatially merges the location data of the catalog gages with the GRADES river segments and relevant attributes. The output file will be a .csv with catalog gages and the COMID (identification for GRADES segments) of the nearest river segment. The attributes associated with the GRADES river segments is joined with gage information.
4. Load the merged gage/GRADES with join_GRADES_HydroATLAS.py to geospatially merge HydroATLAS data with the GRADES river segments. The output file will have gage information, COMID (GRADES), and REACH_ID (HydroATLAS).
5. The final step is to run Data_filter.py which joins these datasets into a final version which contains a) gage location information b) GRADES data c) HydroATLAS attributes. This is the dataset that the placement analysis will be performed on.

### Step 2. Running the Placement Analysis
The analysis is done using the [Placement_analysis.R](https://github.com/AppliedHydro/Gauge-Placement-Analysis/blob/master/Placement_analysis.R) program. In addition to the gage dataset created above, two additional files are necessary, VARNames and FHTNames, which can be found in the github repository. These are used for variable tracking and labelling for more efficient code readability. 
