#------------------------------------------------------------------------------#
# Main 
# author: Steven Schmitz
# last update: 7.15.2024
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
#------------------------------------------------------------------------------#

library(here)
here::i_am('main/main.r')
source(here('main','library.r'))

output_path <- here('outputs')
variable_names <- c("gdp_ud_usu", "urb_pc_use","pre_mm_cyr")
watershed <- "South Fork Payette" # for complete list of watersheds, see watersheds.csv

source(here('main','Placement_analysis.R'))

