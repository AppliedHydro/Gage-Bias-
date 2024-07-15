## Adding variable options

At this writing, the HydroATLAS dataset has 281 individual attributes that can be accessed. The code is currently only set up to analyze 13 of these variables. The Final_data.csv has a large portion of these variables
included but not loaded into the script for analysis. The primary steps to make these edits would be changing the input function and filter:

```r
gagdata<-data %>%
  filter(!is.na(Gage_No)) %>%
  select(COMID,uparea,order_,dor_pc_pva,slope,tmp_dc_cyr,pre_mm_cyr,crp_pc_use,urb_pc_use,pac_pc_cse,ppd_pk_uav,hft_ix_u09,gdp_ud_usu,ecoregion)

alldata<-data %>% 
  filter(!is.na(dor_pc_pva)) %>%
  select(COMID,uparea,order_,dor_pc_pva,slope,tmp_dc_cyr,pre_mm_cyr,crp_pc_use,urb_pc_use,pac_pc_cse,ppd_pk_uav,hft_ix_u09,gdp_ud_usu,ecoregion)
```

These lines take the full-sized dataset and filter outer all columns that aren't these select variables. After editing the select() statement, the user could edit the plot generators to include the variables of interest.

## Alternative labeling for leaflet()

Finding ways to label the leaflet() object for viewer clarity. Overlaying labels on the satellite imagery would improve visual clarity - labels such as county, nearest township, landmarks.

## Editing Place_Bias()

At this writing, Place_Bias() can only handle three variables but could theoretically include all 200 HydroATLAS variables to calculate maximum bias reduction across the entire set. Many variables would not be relevent because of geographic location, but having the option to include more than 3 would be a productive next step. 
