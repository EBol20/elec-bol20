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

df_comp['ID_RECI'] = (df_comp.index/100).astype(np.int64)
df_comp['COUNT'] = True

p = os.path.join(ebu.DATA_PATH1_2020,'z010R_geopadron_mesas_2020_ALL.csv')
df_all = pd.read_csv(p).set_index('ID_MESA')
['ID_RECI', 'ID_MESA', 'HAB', 'INHAB']

df_all['VV'] = 0
df_all['COUNT'] = False
# %%
p = os.path.join(ebu.DATA_PATH1_2020,'z020_geopadron_recintos_2020_ALL_DEN.csv')
df_den = pd.read_csv(p).set_index('ID_RECI')
['ID_RECI', 'LAT', 'LON', 'HAB', 'INHAB', 'PAIS', 'N_MESAS', 'REC',
 'MUN', 'BOL', 'CIU', 'PROV', 'DEP', 'URB', 'DEN_C', 'DEN']

df_den = df_den[['LAT', 'LON', 'PAIS', 'N_MESAS', 'REC',
                 'MUN', 'BOL', 'CIU', 'PROV', 'DEP', 'URB', 'DEN_C', 'DEN']]

# %%
_s  = df_comp.index.isin(df_all.index)
assert (~_s).sum() == 0
# %%
b = ~df_all.index.isin(df_comp.index)
df_trim = df_all[b]
assert len(df_all) - len(df_comp) == len(df_trim)
# %%
df_concat = pd.concat([df_comp,df_trim])

# %%
df_full = df_concat.join(df_den,how='left',on='ID_RECI')
# %%
p = os.path.join(ebu.DATA_PATH1_2020,'z030_carto_xy.csv')
df_xy = pd.read_csv(p).set_index('ID_RECI')
# %%
bokeh.plotting.output_notebook()
COL_LLEGO = '#aaaaaa'
COL_FALTA = '#db2879'

df2 = df_full.join(df_xy,on='ID_RECI',how='left')
ll = len(df2)
np.random.seed(100)
df2['xj'] = df2['X'] + np.random.rand(ll) * .5
np.random.seed(200)
df2['yj'] = df2['Y'] + np.random.rand(ll) * .5
cols = ['yj','xj']

s1 = df2[df2['COUNT']][cols]
s2 = df2[~df2['COUNT']][cols]
sr1 = bokeh.models.ColumnDataSource(s1)
sr2 = bokeh.models.ColumnDataSource(s2)


f = bokeh.plotting.figure(output_backend="webgl")
f.scatter(x='xj',y='yj',source = sr2,color=COL_FALTA,radius=.05, alpha=1, legend_label='Mesas faltantes')
f.scatter(x='xj',y='yj',source = sr1,color=COL_LLEGO,radius=.05, alpha=1, legend_label='Mesas computadas')
f.legend.click_policy="hide"
bokeh.plotting.show(f)
# %%
COL_LLEGO = '#7734eb'
COL_FALTA = '#e5eb34'
# %%
len(s1)

# %%
len(s2)
# %%
# %%
