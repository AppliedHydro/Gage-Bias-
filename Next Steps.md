## Adding variable options

At this writing, the HydroATLAS dataset has 281 individual attributes that can be accessed. The code is currently only set up to analyze 13 of these variables. The Final_data.csv has a large portion of these variables
included but not loaded into the script for analysis. The primary steps to make these edits would be changing the input function and filter:

`gagdata<-data %>%`
  `filter(!is.na(Gage_No)) %>%`
  `select(COMID,uparea,order_,dor_pc_pva,slope,tmp_dc_cyr,pre_mm_cyr,crp_pc_use,urb_pc_use,pac_pc_cse,ppd_pk_uav,hft_ix_u09,gdp_ud_usu,ecoregion)`
