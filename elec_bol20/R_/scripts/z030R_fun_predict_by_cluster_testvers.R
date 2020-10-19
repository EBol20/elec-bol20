#clustermodel function

#' predict_by_cluster
#'
#' @param vote_data Dataframe containing the counted votes. Must contain the columns given in the "summarized_cols" arguments. Must contain one column of all habilitados HAB and of all valid votes VV. Must also contain an identifier column given in the "identifier" argument.
# mesa_info : this has to contain the number of "habilitados" per identifier (given in the identifier argument), under the name of "HAB" @param mesa_info 
#' @param cluster_def this has to contain the cluster assignation of the "mesas". Has to contain  a "cluster"" column and an identifier column, normally "ID_MESA"
#' @param identifier by which identifier should the above frames be merged? Usually "ID_MESA"
#' @param summarized_cols at which columns should be summarized? Usually, enter here the names of the PERCENTAGE columns for the different parties, for example "cc", "mas", etc.
#'
#' @return A list of 5 elements:
# element 1: Total habilitados by cluster. (This depends only on cluster assignement and geopatron)
# element 2: Absolute counted votes by clusted for parties given in "summarized_cols". 
# element 3: mean votes per cluster as fraction of VV for the parties given in "summarized_cols"
# element 4: The prediction of the end result, as one row of a dataframe, coming with standard deviation and standard error. CARE: Those measures of uncertainty seem to be not suitable to correctly assess the uncertainty of the final result estimation. 
# element 5: The predicted total number of valid votes, at a count of 100% (this will be lower than the total number of "habilitados")
#In most of the cases, you will be interested in the 4th element.
#' @export
#'
#' @examples #For the prediction only: predict_by_cluster(mydata, dat_2019_final, cluster_mask, "ID_MESA",c("cc","mas","pdc"))[[3]]
predict_by_cluster_2 = function(vote_data, mesa_info, cluster_def, identifier, summarized_cols){
  
  get_perc = function(vec, totvec){
    return(vec/totvec*100)
  }
  
  vote_data_perc = vote_data %>%
    mutate(vv = get_perc(VV,HAB))%>%
    mutate_at(summarized_cols, 
              .funs = list(perc = ~ get_perc(., VV)))
  
  percentage_cols = paste0(summarized_cols,"_perc")
  

  #getting total habilitados by cluster
  total_by_cluster = dplyr::full_join(mesa_info, cluster_def, by = identifier) %>%
    dplyr::group_by(cluster)%>%
    dplyr::summarise(HAB = sum(HAB,na.rm=T))%>%
    na.omit()
  
  #allvalid = sum(total_by_cluster$VV) # usually not used. We use the estimated total VV instead
  allvotes = sum(total_by_cluster$HAB) # usually not used. We use the estimated total VV instead
  
  #combining
  mydata_combined = dplyr::full_join(vote_data_perc, cluster_def, by = identifier)
  
  #total votes that arrived by cluster
  cluster_total_vote = mydata_combined %>%
    dplyr::group_by(cluster)%>%
    dplyr::summarise_at(c(summarized_cols,"VV"), .funs = list(sum = ~ sum(.,na.rm=T)))
  
  #getting the mean (along with sd and standard error) vote for already counted clusters
  cluster_mean_vote = mydata_combined %>%
    dplyr::group_by(cluster)%>%
    dplyr::summarise_at(c(percentage_cols,"vv"),
                        .funs = list(mean =~ mean(.,na.rm=T),
                                     sd = ~ sd(.,na.rm=T),
                                     sterr = ~ sd(.,na.rm=T)/sqrt(sum(!is.na(.)))))
  
  runlist = list()
  for (i in 1:100){
    set.seed(i)
    runlist[[i]] = mydata_combined %>%
      dplyr::sample_frac(., 0.5)%>%
      dplyr::group_by(cluster)%>%
      dplyr::summarise_at(c(percentage_cols,"vv"),
                          .funs = list(mean =~ mean(.,na.rm=T),
                                       sd = ~ sd(.,na.rm=T),
                                       sterr = ~ sd(.,na.rm=T)/sqrt(sum(!is.na(.)))))
  }
  uncertainty_frame = do.call("rbind", runlist)%>%
    dplyr::group_by(cluster)%>%
    dplyr::summarise_all(sd)
  
  #help functions
  predict_from_percentage = function(clusterperc, total){
    return(clusterperc/100*total)
  }
  
  
  #merging
  myframe = dplyr::full_join(total_by_cluster,cluster_mean_vote,by="cluster")
  #getting total predicted valid votes
  total_predicted_VV = sum(myframe$HAB * myframe$vv_mean/100,na.rm=T)
  
  #end result prediction.
  myprediction_mean = myframe %>%
    na.omit()%>%
    mutate_at(vars(contains("mean")),
              .funs = list(pred = ~ predict_from_percentage(., vv_mean/100*HAB)))%>%
    dplyr::select(contains("mean_pred"))%>%
    dplyr::summarise_all(sum)
  
  #end result standard deviation prediction
  myprediction_sd = myframe %>%
    na.omit()%>%
    mutate_at(vars(contains("sd")),
              .funs = list(pred = ~ predict_from_percentage(., vv_mean/100*HAB)))%>%
    dplyr::select(contains("sd_pred"))%>%
    dplyr::summarise_all(sum)
  
  #end result standard error prediction
  myprediction_sterr = myframe %>%
    na.omit()%>%
    mutate_at(vars(contains("sterr")),
              .funs = list(pred = ~ predict_from_percentage(., vv_mean/100*HAB)))%>%
    dplyr::select(contains("sterr_pred"))%>%
    dplyr::summarise_all(sum)
  
  
  myprediction_mean = myprediction_mean/total_predicted_VV
  myprediction_sd = myprediction_sd/total_predicted_VV
  myprediction_sterr = myprediction_sterr/total_predicted_VV
  
  
  myprediction = cbind(myprediction_mean, myprediction_sd,myprediction_sterr)
  
  return(list(total_by_cluster, cluster_total_vote,
              cluster_mean_vote, myprediction, total_predicted_VV, uncertainty_frame))
}#predict_by_cluster



#importing the cluster mask
cluster_mask = read.csv(paste0(here::here(),"/../datos_1_intermedios/cluster_definition/2019_clustered_10.csv"), colClasses = "character")%>%
  dplyr::select(ID_MESA, cluster)

mesas_2020 = read.csv(paste0(here::here(),"/../datos_1_intermedios/2020/z010R_geopadron_mesas_2020_ALL.csv"),colClasses = "character")%>%
  mutate_at(c("HAB"),as.numeric)


mydata = read.csv(paste0(here::here(),"/../datos_1_intermedios/2020/comp/exportacion_EG2020_actual.csv"),colClasses = "character")

mydata = mydata %>%
  dplyr::filter(CANDIDATURA == "PRESIDENTE")%>%
  mutate_at(vars(!one_of("ID_MESA")),.funs = as.numeric)%>%
  {.}

testprediction = predict_by_cluster_2(mydata, mesas_2020, cluster_mask, "ID_MESA",
                                      c("BL","NU","MAS","CC","CREEMOS","FPV","PAN_BOL"))
testprediction[[1]]
testprediction[[2]]
testprediction[[3]]
testprediction[[4]]

helpvar = testprediction[[6]] 
