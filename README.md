Bias and Wasserstein Distance is calculated over 13 variables in user-specified watershed area. Streams are broken up into segments denoted as gaged or ungaged and then bias is recalculated to find which ungaged sections would reduce bias in user-specified variables were a gage to theoretically be installed. 

## Overview

Welcome to the landing page for the Gage Placement Analysis toolbox. [Krabbenhoft et al (2022)](https://www.nature.com/articles/s41893-022-00873-0) created a workflow process for assessing the placement bias of stream gages using a global stream gage dataset. 19 assorted attributes were selected as the independant variables in the study ranging from socioecological (population, GDP), hydrologic (perennial, non-perennial), and physiographic (mountainous, vegetation type) factors to determine those most instrumental in creating bias in the location and placement of stream gages. This project is predicated on the observation that are significant disparities in the placement of hydrologic gages across the world which impacts decisions made concerning water security, water conservation, and water-monitoring strategies. As a next step for the Streamflow Catalog project, we apply the same processes to the gage locations contained in the up-to-date catalog to obtain a placement bias for gages in the Pacific Northwest (Idaho, Washington, Oregon). The global bias assessment was conducted using 41,000 stream gage locations; the current streamflow catalog has 34,400 gages. The higher quantity of gages contained in a smaller geographic area will ideally produce a higher level of accuracy in the bias assessment. All data used is pubicly available and automations were performed using Python and R coding libraries. 

**Authors**
- Kendra Kaiser, Boise State University   | kendrakaiser@boisestate.edu
- Steven Schmitz, Boise State University  | stevenschmitz@u.boisestate.edu
  
This repository contains the gage data from the [Streamflow Catalog](https://github.com/AppliedHydro/StreamflowCatalog) project and all relevant files being used to replicate a placement bias assessment as seen in [Krabbenhoft et al (2022)](https://www.nature.com/articles/s41893-022-00873-0). 

## Getting Started

### Step 1. Clone the Repository

On the landing page under <> Code, clone the repository by downloading as a zip file. Once downloaded extract on to your machine. 

### Step 2. main.r
Under the *main* directory, main.r is the launching script that will conduct all necessary actions. Inside exist 2 variables that must be manually input by the user:

* @variable_names: these are the variables that will be tested for bias. Up to 3 can be included. See Variables.csv for options.
* @watershed: The watershed that will be tested for bias. See Watersheds.csv for options.

The code process starts by cropping the large dataset (spanning the entire PNW) to the watershed area provided by the user. The GRADES river segments that fall within this watershed boundary are selected and used to denote river sections.

Example:

`variable_names <- c("gdp_ud_usu", "urb_pc_use","pre_mm_cyr")`    
`watershed <- "South Fork Payette"`

### Step 3. Processes
main.r first calls library.r to load all input filepaths. The library *here* is used to create relative file directories and load all required libraries. A check is performed to see if your machine has the required packages. If required packages are not present, library.r will automatically install them. **If you change the file structure or file locations within the repository, the code will not execture properly.** 

Next, main.r calls Placement_analysis.R which performs the actual analysis and figure creation.

The outputs will be saved in the *output* directory in the main folder. Figures are saved in .png format.

The final portion of main.r generates an interactive leaflet map that overlays the segment of interest on satellite imagery with labels. An .html object is saved in outputs that can be loaded in the browser to view the segment and location. 


## Data Sources

### Global Reach-level A priori Discharge Estimates for Surface Water and Ocean Topography (GRADES)
A data set containing ~2.94 million vector river polylines and discharge estimates. GRADES is derived from the MERIT-Hydro model. More information can be found [here](https://www.reachhydro.org/home/records/grades)

### HydroATLAS
HydroATLAS is a global-ranging dataset that contains hydro-environmental characteristics for global river networks. More information can be found [here](https://www.hydrosheds.org/hydroatlas)

### Streamflow Catalog
All gage locations have been collected from the current version of the [Streamflow Catalog](https://scholarworks.boisestate.edu/redi_data/2/) -> [Git](https://github.com/AppliedHydro/StreamflowCatalog) on which the authors are also the primary contributors. 

### Python, R, supplementary code
Ancillary scripts, methods, and data source links were obtained from the [public repository](https://github.com/dry-rivers-rcn/G4) of the Global Gauge Gaps Group (G4) Project.

*------------------------------------------------------------------------------------------------------------------------* <br/>
The background variable data used to conduct the placement bias was assembled from two sources: the GRADES dataset and HydroAtlas. A compilation of 13 variables were chosen and were sourced from GRADES and HydroATLAS datasets and combined into a single dataset using the Python GeoPandas library for geospatial analysis. Specifically, spatial joins were used to assign HydroATLAS variables to GRADES river segments to enable comparison of gages to a single object with all pertinent variables rather than multiple objects in sequence. Prior to spatial joins, the 9 unique HydroATLAS datasets were combined into a single dataset, organized by location, with non-relevant data trimmed off for memory efficiency. The initial HydroATLAS dataset prior to processing was 456 GB in raw format. 

The GRADES river segments dataset encompassed the North American continent and was trimmed to our study area (The Pacific Northwest (PNW): Oregon, Washington, Idaho) using Arcgis Pro geospatial processing tools. The resulting dataset was 14,239 GRADES river segments.

To combine the datasets accurately, GeoPandas was used to create a series of points located at the center of each GRADES river segment that the HydroATLAS data could then be snapped based on 'nearest search' protocols.

The source material for our gage locations is from the [Streamflow Catalog](https://github.com/AppliedHydro/StreamflowCatalog). Data was procurred in excel format (.xlsx) and represents the most up-to-date version of the catalog, 9/7/2023, with approximately 36,000 streamflow gages and location data. For the purposes of this study, the dataset was trimmed to include only relevent variables.

Major script files to perform data cleaning were obtained from the G4 Public Repository that contains source code used for initial placement analysis. Because the initial studies were conducted in a global study area, code corrections needed to be made to refine the working area of the scripts. Scripts were written in both Python and R, Python being used primarily for spatial analysis using the GeoPandas library. Additionally, file directories and loops needed to be rewritten to access files and quantities unique to our study area.

