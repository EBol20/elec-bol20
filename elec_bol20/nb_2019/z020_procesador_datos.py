# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: ebol20
#     language: python
#     name: ebol20
# ---

# %%
from elec_bol20 import *
import elec_bol20.util as ebu
# %%



#diccionario traductor
DIC_TRADUCTOR = {
    'latitud' : 'LAT',
    'Votos Válidos' : 'VV',
}

#aplicar diccionario traductor: df.rename(DIC_TRADUCTOR)

# %%
path = os.path.join(ebu.DATA_PATH0, '2019', 'estad_nac.csv')
path = os.path.join(ebu.DATA_PATH0, '2019', 'estad_ext.csv')

ebu.traductor_df(path, ebu.TRAD_2019_ESTAD_NAC)
# %%
# %%
# %%
# %%
# %%
# %%
