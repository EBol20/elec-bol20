library(tidyverse)
library(data.table)
library(readxl)

###----USER INPUT ONLY HERE #####
filename = "exportacion_EG2020_20201018_202655_8014546445166085676" # name of file to be translated
file_ext = ".csv" #either ".csv" or ".xlsx". 
filepath = paste0(here::here(),"/../datos_0_crudos/2020/comp/") #path to file to be translated
savepath = paste0(here::here(),"/../datos_1_intermedios/2020/comp/") #path to where the file is to be saved

#example for excel file
# filename = "exportacion_EG2020_20201018_191655_1997065378804403743"
# file_ext = ".xlsx"

###-------------------------#####

#function
translate_and_export_comp_dat = function(filename, file_ext,filepath, savepath){
  build_mesa_ID =function(pais, paisnum,ciunum, idloc, recnum, mesanum ){
    mystring = "1"
    mystring = ifelse(pais == "Bolivia", paste0(mystring,"0"), paste0(mystring,"1"))
    
    mystring =paste0(mystring, str_pad(paisnum, 3, pad = "0"))
    mystring = paste0(mystring, str_pad(ciunum, 2, pad = "0"))
    mystring = paste0(mystring, str_pad(idloc, 4, pad = "0"))
    mystring = paste0(mystring, str_pad(recnum, 5, pad = "0"))
    mystring = paste0(mystring, str_pad(mesanum, 2, pad = "0"))
    return(mystring)
  }
  
  filename = paste0(filename, file_ext)
  archive_name = paste0(substr(filename,1,34),".csv")
  name_active = paste0(substr(filename,1,18),"_actual.csv")
  
  translator_vector = c("CODIGO_MESA" = "CODIGO_MESA",
                        "PAIS" = "PAIS",
                        "DEPARTAMENTO" = "DEP",
                        "PROVINCIA" = "PROV",
                        "MUNICIPIO" = "MUN",
                        "ID_RECINTO" = "ID_RECI",
                        "INSCRITOS_HABILITADOS" = "HAB",
                        "CREEMOS" = "CREEMOS",
                        "ADN" = "ADN",
                        "MAS_IPSP" = "MAS",
                        "FPV" = "FPV",
                        "PAN_BOL" = "PAN_BOL",
                        "LIBRE_21" = "LIBRE_21",
                        "CC" = "CC",
                        "JUNTOS"  = "JUNTOS",
                        "VOTO_VALIDO" = "VV",
                        "VOTO_BLANCO" = "BL",
                        "VOTO_NULO" = "NU")
  
  if (file_ext == ".csv"){
    mydata = read.csv(paste0(filepath, filename),
                      colClasses = "character")
  } else if (file_ext == ".xlsx"){
    mydata = readxl::read_xlsx(paste0(filepath, filename))
  } else {warning("Unsupported file extension. Aborting."); return()}

  names(mydata) = plyr::revalue(names(mydata), translator_vector)
  
  mydata = mydata %>%
    dplyr::mutate_at(c("CREEMOS","ADN","MAS","FPV","PAN_BOL","LIBRE_21","CC","JUNTOS"),as.numeric)%>%
    dplyr::mutate(NUA = ADN + LIBRE_21 + JUNTOS)%>%
    mutate(ADN = NULL, LIBRE_21 = NULL, JUNTOS = NULL)%>%
    dplyr::mutate(ID_MESA = build_mesa_ID(PAIS,ID_PAIS, ID_DEPARTAMENTO, ID_LOCALIDAD,
                                          ID_RECI, NUMERO_MESA))
  
  #ARCHIVE DATA
  write.csv(mydata , file = paste0(savepath,archive_name),
            row.names = FALSE, quote = TRUE)
  
  #ACTUAL DATA
  write.csv(mydata , file = paste0(savepath,name_active),
            row.names = FALSE, quote = TRUE)
  
  return(mydata)
}#translate_and_export_comp_dat



#running the function
controldata = translate_and_export_comp_dat(filename, file_ext, filepath, savepath)
