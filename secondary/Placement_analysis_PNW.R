#-----------------------------------------------------#
# This version of Placement_analysis.R is used to specifically
# run all calculations across the entire Pacific Northwest.
# For watershed subsets, see Placement_analysis.R
#-----------------------------------------------------#

# importing data
data <- read.csv('H:/Final_data.csv', header=TRUE)


#------------------------------------------------#

# importing names associated with geospatial variables and major freshwater habitat type
VARnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/VARnames.csv', header=FALSE)
ECOnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/ECOnames.csv', header=FALSE)

# --------------------------------------------------------------------------------------------
# Calculating standard bias and Wassenstein distance for gauge reaches vs. all reaches

# sub-setting reaches to those containing gauges and removing reaches (n=22) with missing geospatial data
gagdata<-data %>% 
  filter(!is.na(Gage_No)) %>%
  select(COMID,uparea,order_,dor_pc_pva,slope,tmp_dc_cyr,pre_mm_cyr,crp_pc_use,urb_pc_use,pac_pc_cse,ppd_pk_uav,hft_ix_u09,gdp_ud_usu,ecoregion) 
# selecting all reaches and removing reaches (n=13,143) with missing missing geospatial data
alldata<-data %>% 
  filter(!is.na(dor_pc_pva)) %>%
  select(COMID,uparea,order_,dor_pc_pva,slope,tmp_dc_cyr,pre_mm_cyr,crp_pc_use,urb_pc_use,pac_pc_cse,ppd_pk_uav,hft_ix_u09,gdp_ud_usu,ecoregion) 

# calculating variable means for all data

varmeans<-alldata[,-1] %>%
  summarise_all(mean,na.rm=TRUE)

# calculating standardized bias and Wasserstein distance for each variable
all_bias<-matrix(, nrow = dim(gagdata[,-1])[2], ncol = 3)
rownames(all_bias)<-t(VARnames)
all_bias<-cbind(VARnames,all_bias)
all_bias[,2]<-bias(gagdata[,-1],varmeans,type='standardized')
colnames(all_bias)<-c("Variable", "bias", "wasser","Direction")

# note that the first column of gagdata and alldata is omitted b/c it is COMID
for (p in 1:dim(gagdata[, -1])[2]) {
  gagdata_std <- (gagdata[, p + 1] - mean(alldata[, p + 1])) / sd(alldata[, p + 1])
  all_bias[p, 3] <- wasserstein1d(gagdata_std, scale(alldata[, p + 1]), p = 1)
  
  # Check for missing values before making the comparison
  if (!is.na(all_bias[p, 2]) && all_bias[p, 2] > 0) {
    all_bias[p, 4] <- "positive"
  } else {
    all_bias[p, 4] <- "negative"
  }
}

# --------------------------------------------------------------------------------------------
# Producing Figure 2

# Figure 2a
all_bias <- all_bias[order(all_bias$wasser), ] 
all_bias$Variable <- factor(all_bias$Variable, levels = all_bias$Variable)
all_bias$Direction <- factor(all_bias$Direction, levels = c("positive","negative"))
all_bias$wasser[is.nan(all_bias$wasser)] <- 0

ggplot(all_bias, aes(x=Variable, y=`wasser`, color=Direction, size=wasser, fill=Direction)) + 
  geom_point(alpha=1)  + scale_size(range = c(1, 6)) +
  scale_color_manual(values=c("blue", "red"),name="Bias Direction", labels = c("Positive","Negative")) + 
  scale_fill_manual(values=c("blue", "red"),name="Bias Direction", labels = c("Positive","Negative")) + 
  labs(title="a",y="Wasserstein Distance (Bias)") + 
  coord_flip() +
  guides(size="none") +
  scale_y_continuous(limits=c(0,max(all_bias$wasser),0)) +
  theme (
    panel.grid.minor = element_blank(),
    axis.text.x = element_text(colour="black",size=12), 
    axis.text.y = element_text(colour="black",size=12),
    legend.text = element_text(colour="black",size=11),
    legend.title=element_text(colour="black",size=13), 
    plot.title=element_text(colour="black",size=14,hjust=0), 
    axis.title.y=element_blank(), 
    axis.title.x=element_text(colour="black",size=12), 
    panel.background = element_rect(fill = "lightgray", colour="black"),
    legend.position.inside = c(0.825, 0.1)
  )

# Figure 2b-f

# Plotting variable distributions to highlight some examples
temp<-c(rep("gag",dim(gagdata)[1]),rep("all",dim(alldata)[1]))
temp<-as.matrix(temp)
comdata<-cbind(temp,as.data.frame(rbind(gagdata,alldata)))
colnames(comdata)[1]<-"type"

a<-ggplot(comdata, aes(x = pre_mm_cyr,colour=type)) + stat_ecdf(linewidth=1.5) +
  scale_color_manual(values=c("black","#E69F00"),name="River Segment", labels = c("All","Gauged")) + 
  labs(title="a", x="Precipitation (mm/yr)", y="Cumulative probability")  +
  theme(
    panel.grid.minor = element_blank(),
    legend.position = c(0.85, 0.25),
    panel.background = element_rect(fill = "lightgray"),
    axis.text.x = element_text(colour="black",size=11), 
    axis.text.y = element_text(colour="black",size=11),
    legend.text = element_text(colour="black",size=10),
    legend.title=element_text(colour="black",size=10), 
    #plot.title=element_text(colour="black",size=14,hjust=0), 
    axis.title.y=element_text(colour="black",size=11), 
    axis.title.x=element_text(colour="black",size=11), 
  )

b<-ggplot(comdata, aes(x = log10(dor_pc_pva+1),colour=type)) + stat_ecdf(linewidth=1.5) +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray")) +
  labs(title="b", x="Flow Regulation (log+1) (%)", y="Cumulative probability")  +
  theme(
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "lightgray"),
    axis.text.x = element_text(colour="black",size=11), 
    axis.text.y = element_text(colour="black",size=11),
    axis.title.y=element_text(colour="black",size=11), 
    axis.title.x=element_text(colour="black",size=11), 
  )

c<-ggplot(comdata, aes(x = hft_ix_u09,colour=type)) + stat_ecdf(linewidth=1.5) +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray")) +
  labs(title="c", x="Human Footprint", y="Cumulative probability")  +
  theme(
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "lightgray"),
    axis.text.x = element_text(colour="black",size=11), 
    axis.text.y = element_text(colour="black",size=11),
    axis.title.y=element_blank(), 
    axis.title.x=element_text(colour="black",size=11), 
  )

d<-ggplot(comdata, aes(x = tmp_dc_cyr/10,colour=type)) + stat_ecdf(linewidth=1.5) +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray")) +
  labs(title="d", x="Air Temperature (°C)", y="Cumulative probability")   +
  theme(
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "lightgray"),
    axis.text.x = element_text(colour="black",size=11), 
    axis.text.y = element_text(colour="black",size=11),
    axis.title.y=element_blank(), 
    axis.title.x=element_text(colour="black",size=11), 
  )

# plotting in a 2-by-2 panel
grid.arrange(a,c,b,d)

# --------------------------------------------------------------------------------------------
# Producing Figure S4

# transforming data to aid intepretation
comdata$type <- factor(comdata$type, levels = c("all","gag"))
comdata$uparea_log<-log(comdata$uparea+1)
comdata$slope_log<-log10(comdata$slope+1)
comdata$pre_mm_cyr_log<-log10(comdata$pre_mm_cyr+1)
comdata$crp_pc_use_log<-log10(comdata$crp_pc_use+1)
comdata$urb_pc_use_log<-log10(comdata$urb_pc_use+1)
comdata$pac_pc_cse_log<-log10(comdata$pac_pc_cse+1)
comdata$ppd_pk_uav_log<-log10(comdata$ppd_pk_uav+0.01)
comdata$gdp_ud_usu_log<-log10(comdata$gdp_ud_usu+1)

a<-ggplot(comdata, aes(x = uparea_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black", "#E69F00"),name="River Segment", labels = c("All", "Gauged"))  +
  labs(title="a", x=expression(Catchment~Area~(log+1)~(m^2)), y="Cumulative probability")  +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(
    legend.key.size = unit(0.3, 'cm'),
    legend.title = element_text(size=10),
    panel.grid.minor = element_blank(),
    legend.position = c(0.7, 0.28),
    panel.background = element_rect(fill = "lightgray")
  )
b<-ggplot(comdata, aes(x = order_,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  scale_color_manual(values=c("black","#E69F00")) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray"),axis.title.y=element_blank()) +
  labs(title="b", x="Stream Order (Strahler)")  
c<-ggplot(comdata, aes(x = slope_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray"),axis.title.y=element_blank()) +
  labs(title="c", x=expression(Channel~Gradient~(log)~"(%)"))  
d<-ggplot(comdata, aes(x = pre_mm_cyr_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray")) +
  labs(title="d", x=expression(Precipitation~(log+1)~"(mm/year)"), y="Cumulative probability")
e<-ggplot(comdata, aes(x = crp_pc_use_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray"),axis.title.y=element_blank()) +
  labs(title="e", x="Crop Landuse (log+1) (%)")
f<-ggplot(comdata, aes(x = urb_pc_use_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray"),axis.title.y=element_blank()) +
  labs(title="f", x="Urban Landuse (log+1) (%)")
g<-ggplot(comdata, aes(x = pac_pc_cse_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray")) +
  labs(title="g", x="Protected Area (log+1) (%)", y="Cumulative probability")
h<-ggplot(comdata, aes(x = ppd_pk_uav_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray"),axis.title.y=element_blank()) +
  labs(title="h", x=expression(Pop~Density~(log+0.01)~(no.~km^-2)))  
i<-ggplot(comdata, aes(x = gdp_ud_usu_log,colour=type)) + stat_ecdf(linewidth=1.5)  +
  theme_bw() + 
  scale_color_manual(values=c("black","#E69F00")) +
  scale_y_continuous(limits=c(0,1.0),labels = scales::number_format(accuracy = 0.01)) +
  theme(panel.grid.minor = element_blank(),legend.position = "none",panel.background = element_rect(fill = "lightgray"),axis.title.y=element_blank()) +
  labs(title="i", x="Gross Domest Prod (log+1) (USD)")  

# plotting in a 4-by-4 panel
grid.arrange(a,b,c,d,e,f,g,h,i)


# --------------------------------------------------------------------------------------------
# Calculating standard bias and Wassenstein distance for gauge reaches vs. all reaches
# according to Major Freshwater Habitat Types (Freshwater Ecoregions of the World: Abell et al. 2008)

# creating matrix for results
ECOnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/ECOnames.csv',skip=1, header=FALSE)
VARnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/VARnames.csv', header=FALSE)
VARnames <- VARnames[-nrow(VARnames), ]

fht_results <- matrix(, nrow = 12, ncol = 14) #manually set dimensions
rownames(fht_results) <- t(VARnames)
colnames(fht_results) <- t(ECOnames)
print(fht_results)

for (j in 1:13) {
  # subsetting segments containing gauges and removing 3 reaches with NA
  gagdata_fht <- data %>%
    filter(!is.na(Gage_No) & ecoregion == j) %>%
    select(uparea, order_, dor_pc_pva, slope, tmp_dc_cyr, pre_mm_cyr, crp_pc_use, urb_pc_use, pac_pc_cse, ppd_pk_uav, hft_ix_u09, gdp_ud_usu)
  
  # selecting the same variables for all global segments
  alldata_fht <- data %>%
    filter(!is.na(dor_pc_pva) & ecoregion == j) %>%
    select(uparea, order_, dor_pc_pva, slope, tmp_dc_cyr, pre_mm_cyr, crp_pc_use, urb_pc_use, pac_pc_cse, ppd_pk_uav, hft_ix_u09, gdp_ud_usu)
  
  # calculating standardized bias and Wasserstein distance and test statistics for each variable
  print(paste('Processing ecoregion:', j))
  fht_bias <- matrix(, nrow = 12, ncol = 3)
  rownames(fht_bias) <- t(VARnames)
  fht_bias <- cbind(VARnames, fht_bias)
  fht_bias[, 2] <- bias(gagdata_fht, varmeans[, -ncol(varmeans)], type = 'standardized')
  colnames(fht_bias) <- c("Variable", "bias", "wasser", "Direction")
  
  print('Bias values:')
  print(fht_bias[, 2])
  
  # note that the first column of gagdata and alldata is omitted b/c it is 
  p = 0
  for (p in 1:dim(gagdata_fht)[2]) {
    gagdata_fht_std <- (gagdata_fht[, p] - mean(alldata_fht[, p])) / sd(alldata_fht[, p])
    fht_bias[p, 3] <- wasserstein1d(gagdata_fht_std, scale(alldata_fht[, p]), p = 1)
    
    # Check if fht_bias[p, 2] is not NA before evaluating the condition
    if (!is.na(fht_bias[p, 2]) && fht_bias[p, 2] < 0) {
      fht_bias[p, 3] <- as.numeric(fht_bias[p, 3]) * -1
    }
  }
  
  print('Wasserstein distances:')
  print(fht_bias[, 3])
  
  # output Wasserstein distances
  fht_results[, j] <- fht_bias[, 3]
}

# Producing Figure 3
theme_set(theme_bw())
fht_results<-t((fht_results))

fht_results_numeric <- apply(fht_results, 2, as.numeric)
any_na <- any(is.na(fht_results_numeric))
if (any_na) {
  cat("There are NA values in the converted numeric matrix.")
}

fht_results_df <- as.data.frame(fht_results_numeric)
fht_results_df[!is.finite(as.matrix(fht_results_df))] <- 0

a<-heatmaply(fht_results_df, 
             dendrogram = "row",
             xlab = "", ylab = "", 
             main = "",
             scale = "none",
             legend = TRUE,
             margins = c(60,100,40,20),
             grid_color = "white",
             grid_width = 0.00001,
             titleX = TRUE,
             hide_colorbar = FALSE,
             colorbar(titlefont=list(size=5)),
             branches_lwd = 0.1,
             label_names = c("FHT", "Variable:", "Value"),
             fontsize_row = 12, fontsize_col = 12,
             labCol = colnames(fht_results),
             labRow = rownames(fht_results),
             # layout(legend.font="Arial"),
             scale_fill_gradient_fun = ggplot2::scale_fill_gradient2(
               low = "dark blue", 
               high = "dark red", 
               midpoint = 0, 
               limits = c(-1.5, 1.5),
               name="Wasserstein \nDistance (Bias)"),
             heatmap_layers = theme(axis.line=element_blank(),axis.text.x=element_text(colour="black"),axis.text.y=element_text(colour="black")),
) 


a %>% layout(xaxis=list(tickfont = list(family = "Helvetica")),yaxis=list(tickfont = list(family = "Helvetica")))

# --------------------------------------------------------------------------------------------
# calculate the overall change in global bias in gauge placement (averaged across all variables) 
# if a new gauge were installed

# importing names associated with geospatial variables and major freshwater habitat type
VARnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/VARnames_noeco.csv', header=FALSE)
FHTnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/FHTnames.csv', header=FALSE)
ECOnames <- read.csv('C:/Users/stevenschmitz/Desktop/PlacementBias/Git/G4-master/in/ECOnames.csv', header=FALSE)

# sub-setting reaches to those containing gauges and removing reaches (n=22) with missing geospatial data
gagdata<-data %>% 
  filter(!is.na(Gage_No)) %>%
  select(COMID,uparea,order_,dor_pc_pva,slope,tmp_dc_cyr,pre_mm_cyr,crp_pc_use,urb_pc_use,pac_pc_cse,ppd_pk_uav,hft_ix_u09,gdp_ud_usu,lengthkm) 
# selecting all reaches and removing reaches (n=13,143) with missing missing geospatial data
alldata<-data %>% 
  filter(!is.na(dor_pc_pva)) %>%
  select(COMID,uparea,order_,dor_pc_pva,slope,tmp_dc_cyr,pre_mm_cyr,crp_pc_use,urb_pc_use,pac_pc_cse,ppd_pk_uav,hft_ix_u09,gdp_ud_usu,lengthkm) 

# calculating variable means for all data

varmeans<-alldata[,-1] %>%
  summarise_all(mean,na.rm=TRUE)

# defining the number of segments
no.seg<-dim(alldata)[1]
permutation_bias<-matrix(,ncol=13,nrow=no.seg)
for (j in 1:no.seg) {
  perdata<-rbind(gagdata, alldata[j,])
  permutation_bias[j,]<-c(alldata[j,1],bias(perdata[,2:(dim(gagdata)[2])],varmeans,type='standardized'))
}

# calculating % change in bias for each variable and overall mean across variables
current_bias<-as.matrix(bias(gagdata[,2:(dim(gagdata)[2])],varmeans,type='standardized'))
temp<-sweep(permutation_bias[,2:13], MARGIN=2,FUN="-", current_bias)
finalbias<-sweep(temp,MARGIN=2,FUN="/", current_bias)*100
finalbias<-cbind(permutation_bias[,1],finalbias,rowMeans(finalbias[,2:12]))
finalbias<-as.data.frame(finalbias)
colnames(finalbias)<-c("COMID", t(VARnames), "MeanBiasChange")

#This function takes the 'variable_name' argument as a string, refer to alldata import variables
# variable name - variable you are testing bias for
# alldata - see above
#
# This function is telling you, based on all of the locations in alldata, where the bias reduction
# would be the most if a gage were placed there.
# 
# output: COMID:river segment where, if gage were placed, results in max bias reduction
# 

place_bias <- function(variable_name, alldata, gagdata, varmeans) {
  if (!(variable_name %in% colnames(gagdata))) stop(paste("Variable", variable_name, "not found in gagdata"))
  
  variables <- c("uparea", "order_", "dor_pc_pva", "slope", "tmp_dc_cyr",
                 "pre_mm_cyr", "crp_pc_use", "urb_pc_use", "pac_pc_cse",
                 "ppd_pk_uav", "hft_ix_u09", "gdp_ud_usu")
  
  if (!(variable_name %in% variables)) stop(paste("Variable", variable_name, "not found in the common variables"))
  
  result <- data.frame(COMID = numeric(0), Position = numeric(0), BiasReduction = numeric(0))
  
  for (j in 1:nrow(alldata)) {
    if (j %in% gagdata$Position) next
    
    bias_before <- bias(gagdata[, variables], varmeans, type = 'standardized')
    perdata <- rbind(gagdata, alldata[j, ])
    bias_after <- bias(perdata[, variables], varmeans, type = 'standardized')
    
    variable_index <- which(names(bias_before) == variable_name)
    reduction <- bias_before[variable_index] - bias_after[variable_index]
    
    result <- rbind(result, data.frame(COMID = alldata[j, "COMID"], Position = j, BiasReduction = reduction))
  }
  
  max_reduction_row <- result[which.max(result$BiasReduction), ]
  return(max_reduction_row)
}

biasoutput <- place_bias("tmp_dc_cyr", alldata, gagdata, varmeans) # output saved to variable

#Plot grades segment with lowest bias

shapefile_path <- 'H:/GRADES/GRADES_eco.shp'
grades_sf <- st_read(shapefile_path)
comid <- biasoutput$COMID
selected_row <- grades_sf[grades_sf$COMID == comid, ]

ggplot() +
  geom_sf(data = grades_sf) +
  geom_sf(data = selected_row, color = "red") +
  labs(title = paste("COMID =", comid), subtitle = paste("Segment Location: ",round(st_bbox(selected_row)$ymax,3),",",round(st_bbox(selected_row)$xmax,3))) +
  coord_sf(xlim = c(st_bbox(selected_row)$xmin - 0.1, st_bbox(selected_row)$xmax + 0.1),
           ylim = c(st_bbox(selected_row)$ymin - 0.1, st_bbox(selected_row)$ymax + 0.1)) 

# leaflet
compute_median_coordinates <- function(multilinestring) {
  coords <- st_coordinates(multilinestring)
  median_coords <- apply(coords, 2, median)
  return(median_coords)
}

median_coordinates <- compute_median_coordinates(selected_row$geometry)
median_coordinates[1] <- round(median_coordinates[1],4)
median_coordinates[2] <- round(median_coordinates[2],4)
median_coordinates <- median_coordinates[1:2]
median_coords_str <- paste(median_coordinates, collapse = ", ")

leaflet() %>%
  addPolylines(data = selected_row, color = "red", weight = 4, group = "Selected Line") %>%
  addMarkers(lat = median_coordinates[2], lng = median_coordinates[1],
             label = paste("Segment location", median_coords_str), labelOptions = labelOptions(noHide = TRUE)) %>%
  addProviderTiles(providers$Esri.WorldImagery, group = "Satellite") %>%
  addProviderTiles(providers$Esri.WorldImageryLabels, group = "Labels") %>%
  addLayersControl(
    baseGroups = c("Satellite"),
    overlayGroups = c("Labels", "Selected Line"),
    options = layersControlOptions(collapsed = FALSE)
  )

# Rmarkdown


