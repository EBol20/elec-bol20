# columnas que cada file debería tener para entrar al predictor
COL_STANDARD = [
    "LAT", "LON",
    "ID_MESA", # id mesa  e.g 11111
    "ID_RECINTO", # id recinto e.g 111
    "HAB", # n. de inscritos habilitados
    "VV", # votos validos
    "MAS", "CC", "CRE", "PDV", # partidos políticos (en valor absoluto)
    "D_MAS_CC", # diferencia mas cc
    "mas", "cc","cre","pdv", # absoluto/VV * 100
    "d_mas_cc" ,
    "X", "Y", # coordinadas cartograma
    "BOL", #true bolivia, False mundo
    "BL", #blancos
    "NU", # nulos,m
    "NUA", # nulos agregado con partidos descalificados

]

#diccionario traductor
DIC_TRADUCTOR = {
    'latitud' : 'LAT',
    'Votos Válidos' : 'VV',
}

#aplicar diccionario traductor: df.rename(DIC_TRADUCTOR)

