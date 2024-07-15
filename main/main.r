#------------------------------------------------------------------------------#
# Main 
# author: Steven Schmitz
# last update: 7.2.2024
#
# @variable_names: these are the variables that will be bias tested. You can 
# as many variable as you choose and the river segment with the largest average
# bias reduction will be returned. The format of the variable_names object should
# be: c("variable1", "variable2",...)
#
# See Variables.csv for possible inputs
#
# @watershed: this object is the watershed that the maps and calculations will 
# be cropped too. Currently, only one watershed at a time can be processed. 
# 
# See Watersheds.csv for possible inputs
#
#------------------------------------------------------------------------------#
library(here)
here::i_am('main/main.r')
source(here('main','library.r'))

output_path <- here('outputs')
variable_names <- c("gdp_ud_usu", "urb_pc_use","pre_mm_cyr")
watershed <- "South Fork Payette" # for complete list of watersheds, see watersheds.csv

source(here('main','Placement_analysis.R'))

#--------------------#
# Leaflet generator of selected segment with maximum bias reduction for
# chosen variables. The GRADES river segment is place on top of 
# satellite imagery and can be explored interactively.
#--------------------#

interactive_map <- leaflet() %>%
  addPolylines(data = selected_row, color = "red", weight = 4, group = "Selected Line") %>%
  addMarkers(lat = median_coordinates[2], lng = median_coordinates[1],
             label = paste("Segment location", median_coords_str), labelOptions = labelOptions(noHide = TRUE)) %>%
  addProviderTiles("Esri.WorldImagery", group = "Map") %>%
  addProviderTiles("OpenStreetMap.Mapnik", group = "Labels") %>%
  addLayersControl(
    baseGroups = c("Map", "Labels"),
    overlayGroups = c("Selected Line"),
    options = layersControlOptions(collapsed = FALSE)
  )

saveWidget(interactive_map, here('outputs','leaflet_map.html'))
