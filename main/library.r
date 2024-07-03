library(tidyverse)
library(sf)
library(ggplot2)
library(SimDesign)
library(transport)
library(gridExtra)
library(heatmaply)
library(maps)
library(sp)
library(leaflet)
library(rmarkdown)
library(htmlwidgets)

data <- read.csv('H:/Final_data.csv', header=TRUE)

VARnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/VARnames.csv', header=FALSE)
ECOnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/ECOnames.csv', header=FALSE)
FHTnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/FHTnames.csv', header=FALSE)
VARnames1 <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/VARnames_noeco.csv', header=FALSE)

shapefile_path <- "H:/gage_bias_master/GRADES_PNW/WatershedHUC8.shp"
