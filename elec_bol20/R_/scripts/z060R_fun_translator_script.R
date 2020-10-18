library(tidyverse)
library(data.table)

filename = "exportacion_EG2020_20201018_184655_6036973977742226983.csv"
archive_name = paste0(substr(filename,1,34),".csv")
name_active = paste0(substr(filename,1,18),"_actual.csv")

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
                         "/../datos_0_crudos/2020/comp/", filename),
                  colClasses = "character")
names(mydata) = plyr::revalue(names(mydata), translator_vector)

mydata = mydata %>%
  dplyr::mutate_at(c("Creemos","ADN","MAS","FPV","PAN_BOL","LIBRE_21","CC","JUNTOS"),as.numeric)%>%
  dplyr::mutate(NUA = ADN + LIBRE_21 + JUNTOS)%>%
  mutate(ADN = NULL, LIBRE_21 = NULL, JUNTOS = NULL)

#ARCHIVE DATA
write.csv(mydata , file = paste0(here::here(),"/../datos_1_intermedios/2020/comp/",
                                 archive_name),
          row.names = FALSE, quote = TRUE)

#ACTUAL DATA
write.csv(mydata , file = paste0(here::here(),"/../datos_1_intermedios/2020/comp/",
                                 name_active),
          row.names = FALSE, quote = TRUE)
