options(warn = -1) # suppresses console warnings

library(here)
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

data <- read.csv(here('inputs','Final_data.csv'), header=TRUE)

VARnames <- read.csv(here('inputs','VARnames.csv'), header=FALSE)
ECOnames <- read.csv(here('inputs','ECOnames.csv'), header=FALSE)
FHTnames <- read.csv(here('inputs','FHTnames.csv'), header=FALSE)
VARnames1 <- read.csv(here('inputs','VARnames_noeco.csv'), header=FALSE)

shapefile_path <- here('inputs','WatershedHUC8.shp')
