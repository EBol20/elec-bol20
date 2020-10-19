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
df2= ebu.get_dataframe_2020()

# %%



# %%

# %%
bokeh.plotting.output_notebook()
COL_LLEGO = '#aaaaaa'
COL_FALTA = '#db2879'


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
df2

# %%
dfn = df2.copy()
dfn.loc[~dfn['BOL'],'DEN_CODES'] = -1

# %%
_df = dfn
gr = _df.groupby('DEN_CODES')
den = gr[['HAB']].sum()
den['cum'] = den['HAB'].cumsum()
tot = den['HAB'].sum()
den['mid'] = den['cum'] - den['HAB']/2
den['top'] = 100
den['width'] = den['HAB']-(tot*.01)
den1 = den.copy()

# %%
_df = dfn[dfn['COUNT']]
gr = _df.groupby('DEN_CODES')
den = gr[['HAB']].sum()
den['cum'] = den['HAB'].cumsum()
tot = den['HAB'].sum()
den['mid'] = den['cum'] - den['HAB']/2
den['top'] = 1 
den['width'] = den['HAB']-(tot*.01)
den2 = den.copy()

# %%
den1['counted'] = den['HAB']

# %%
den1['top_c'] =den1['counted']/den1['HAB']*100

# %%
den1.loc[-1,'mid'] = den1.loc[-1,'mid'] - 1000000

# %%
df2[df2['COUNT']]['HAB'].sum()

# %%


p = bokeh.plotting.figure(height=400)
# fi = bokeh.plotting.figure()
p.vbar(x=den1['mid'],width=den1['width'],top=den1['top'],color=COL_FALTA)
p.vbar(x=den1['mid'],width=den1['width'],top=den1['top_c'],color=COL_LLEGO)
p.title.text = ''

x = den1[den1.index>=0]['mid'].mean()
p.text(x=[x],y=[120],text=['Nacional'])

x = den1[den1.index==0]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad baja'],angle=.5, text_font_size="8pt")

x = den1[den1.index==1]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad media'],angle=.5, text_font_size="8pt")

x = den1[den1.index==2]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad moderada'],angle=.5, text_font_size="8pt")

x = den1[den1.index==3]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad alta'],angle=.5, text_font_size="8pt")

x = den1[den1.index<0]['mid'].mean()
p.text(x=[x],y=[110],text=['Exterior'],text_align='center')

# lay = bokeh.layouts.row([fi,p])
lay = p 
bokeh.plotting.show(lay)
# %%
den1[den1.index>=0]['mid'].mean()

# %%
x

# %%

# %%
