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

# %% [markdown]
# ###### init

# %%
# de los resultados generales crea silmulaciones con % de
# datos para que luego sean procesados

# %%
# import
from elec_bol20 import *
import elec_bol20.util as ebu
import bokeh.layouts
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure
# output_file, show
import bokeh.tile_providers



# %%
p = os.path.join(ebu.DATA_PATH1_2020,'z050R_dummy_votearrival_20.csv')
df_comp = pd.read_csv(p).set_index('ID_MESA')
['ID_MESA', 'HAB', 'INHAB', 'VV']

df_comp['ID_RECI'] = df_comp.index/100
df_comp['COUNT'] = True

p = os.path.join(ebu.DATA_PATH1_2020,'z010R_geopadron_mesas_2020_ALL.csv')
df_all = pd.read_csv(p).set_index('ID_MESA')
['ID_RECI', 'ID_MESA', 'HAB', 'INHAB']

df_all['VV'] = 0
df_all['COUNT'] = False
#%%
p = os.path.join(ebu.DATA_PATH1_2020,'z020_geopadron_recintos_2020_ALL_DEN.csv')
df_den = pd.read_csv(p)
['ID_RECI', 'LAT', 'LON', 'HAB', 'INHAB', 'PAIS', 'N_MESAS', 'REC',
 'MUN', 'BOL', 'CIU', 'PROV', 'DEP', 'URB', 'DEN_C', 'DEN']


#%%

#%%
