#clustermodel function

#' predict_by_cluster
#'
#' @param vote_data Dataframe containing the counted votes. Must contain the columns given in the "summarized_cols" arguments. Must imparatively contain one column giving the percentage of valid votes (valid votes/total habilitados*100), named "vv". Must also contain an identifier column given in the "identifier" argument.
# mesa_info : this has to contain the number of "habilitados" per identifier (given in the identifier argument), under the name of "HAB" @param mesa_info 
#' @param cluster_def this has to contain the cluster assignation of the "mesas". Has to contain  a "cluster"" column and an identifier column, normally "ID_MESA"
#' @param identifier by which identifier should the above frames be merged? Usually "ID_MESA"
#' @param summarized_cols at which columns should be summarized? Usually, enter here the names of the PERCENTAGE columns for the different parties, for example "cc", "mas", etc.
#'
#' @return A list of 4 elements:
#First element: Total habilitados by cluster
#Second element: mean votes per cluster for the parties given in "summarized_cols"
#Third element: The prediction of the end result, as one row of a dataframe, coming with standard deviation and standard error. CARE: Those measures of uncertainty seem to be not suitable to correctly assess the uncertainty of the final result estimation. 
#Fourth element: The predicted total number of valid votes, at a count of 100% (this will be lower than the total number of "habilitados")
#In most of the cases, you will be interested in the third element.
#' @export
#'
#' @examples #For the prediction only: predict_by_cluster(mydata, dat_2019_final, cluster_mask, "ID_MESA",c("cc","mas","pdc"))[[3]]
predict_by_cluster = function(vote_data, mesa_info, cluster_def, identifier, summarized_cols){

  #getting total habilitados by cluster
  total_by_cluster = dplyr::full_join(mesa_info, cluster_def, by = identifier) %>%
    dplyr::group_by(cluster)%>%
    dplyr::summarise_at(c("HAB"),.funs = sum)%>%
    na.omit()
  
  #allvalid = sum(total_by_cluster$VV) # usually not used. We use the estimated total VV instead
  allvotes = sum(total_by_cluster$HAB) # usually not used. We use the estimated total VV instead
  
  #combining
  mydata_combined = dplyr::full_join(vote_data, cluster_def, by = identifier)
  
  #getting the mean (along with sd and standard error) vote for already counted clusters
  cluster_mean_vote = mydata_combined %>%
    dplyr::group_by(cluster)%>%
    dplyr::summarise_at(c(summarized_cols,"vv"),
                        .funs = list(mean =~ mean(.,na.rm=T),
                                     sd = ~ sd(.,na.rm=T),
                                     sterr = ~ sd(.,na.rm=T)/sqrt(sum(!is.na(.)))))%>%
    na.omit()
  
  #help functions
  predict_from_percentage = function(clusterperc, total){
    return(clusterperc/100*total)
  }
  error_propagation = function(vec){
    return(sqrt(sum(vec^2)))
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
  
  return(list(total_by_cluster, cluster_mean_vote, myprediction, total_predicted_VV))
}#predict_by_cluster
