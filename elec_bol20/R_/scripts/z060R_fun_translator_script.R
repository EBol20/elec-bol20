library(tidyverse)
library(data.table)

folder_and_filename = "2020_10_19_00_25/exportacion_EG2020_20201018_181655_4462622834299457053.csv"

translator_vector = c("CODIGO_MESA" = "ID_MESA",
                      "PAIS" = "PAIS",
                      "DEPARTAMENTO" = "DEP",
                      "PROVINCIA" = "PROV",
                      "MUNICIPIO" = "MUN",
                      "ID_RECINTO" = "ID_RECI",
                      "INSCRITOS_HABILITADOS" = "HAB",
                      "CREEMOS" = "Creemos",
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

#NUA = #ADN #libre21 #Juntos
mydata = read.csv(paste0(here::here(),
                         "/../datos_0_crudos/2020/comp/",
                         folder_and_filename),colClasses = "character")
names(mydata) = plyr::revalue(names(mydata), translator_vector)

mydata = mydata %>%
  dplyr::mutate_at(c("Creemos","ADN","MAS","FPV","PAN_BOL","LIBRE_21","CC","JUNTOS"),as.numeric)%>%
  dplyr::mutate(NUA = ADN + LIBRE_21 + JUNTOS)%>%
  mutate(ADN = NULL, LIBRE_21 = NULL, JUNTOS = NULL)


write.csv(mydata , file = paste0(here::here(),"/../datos_1_intermedios/2020/",folder_and_filename),
          row.names = FALSE, quote = TRUE)
