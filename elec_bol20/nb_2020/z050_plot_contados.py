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
df2['COUNT'].sum()

# %%
df2['HAB']

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
f.scatter(x='xj',y='yj',source = sr2,color=COL_FALTA,radius=.05, alpha=1, legend_label='Mesas faltantes (haz click)')
f.scatter(x='xj',y='yj',source = sr1,color=COL_LLEGO,radius=.05, alpha=1, legend_label='Mesas computadas (haz click)')
f.legend.click_policy="hide"




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
dfn['HAB']

# %%
den1['counted'] = den2['HAB'].astype(np.int64)

# %%
den1['top_c'] =den1['counted']/den1['HAB']*100

# %%
den1.loc[-1,'mid'] = den1.loc[-1,'mid'] - 1000000

# %%
df2[df2['COUNT']]['HAB'].sum()

def _t(s): 
    if np.isnan(s): s=0
    return f'{s:0.1f}'

def _t1(s): 
    if np.isnan(s): s=0
    return f'{s:0.0f}'

def _t2(r):
#     return f'{r["tv"]} ({r["tc"]} %)'
    return f'{r["tc"]}%'

den1['tc']=den1['top_c'].apply(_t)
den1['tv']=den1['counted'].apply(_t1)
den1['text'] = den1.apply(_t2,axis=1)

# %%


p = bokeh.plotting.figure(height=400)
# fi = bokeh.plotting.figure()
p.vbar(x=den1['mid'],width=den1['width'],top=den1['top'],color=COL_FALTA)
p.vbar(x=den1['mid'],width=den1['width'],top=den1['top_c'],color=COL_LLEGO)
p.title.text = ''

x = den1[den1.index>=0]['mid'].mean()
p.text(x=[x],y=[120],text=['Nacional'])

an = .4
x = den1[den1.index==0]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad baja'],angle=an, text_font_size="8pt")

x = den1[den1.index==1]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad media'],angle=an, text_font_size="8pt")

x = den1[den1.index==2]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad moderada'],angle=an, text_font_size="8pt")

x = den1[den1.index==3]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad alta'],angle=an, text_font_size="8pt")

x = den1[den1.index<0]['mid'].mean()
p.text(x=[x],y=[110],text=['Exterior'],text_align='center')
p.xaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
f.yaxis.visible = False
f.yaxis.visible = False
p.y_range.start=0
p.y_range.end=130
p.yaxis.axis_label="Porcentage"
ppp=den1['counted'].sum()/den1['HAB'].sum() * 100
p.title.text = f'Porcentage de votos computados divididos por densidad (total computado={ppp:0.1f}%)'
p.xaxis.axis_label=f'Porcentage total de votos computados = ({ppp:0.1f}%)'
p.toolbar.logo = None
p.toolbar_location = None

f.title.text = "Cartolocación de las mesas"

for l,r in den1.iterrows():
    if l ==-1:
        x = r['mid'] + 400000
    else:
        x = r['mid']
    
    p.text(x=x,y=[r['tc']],text=[r['text']],text_align='center',text_font_size="8pt")

lay = bokeh.layouts.row([p,f])
# lay = p 
bokeh.plotting.show(lay)
# %%
_c = ['CREEMOS',	'MAS',	'FPV',	'PAN_BOL',	'CC']
dd= df2[[*_c,'VV']].copy()
res = dd[_c].sum()/dd['VV'].sum()*100
res.name = 'per'
res.index.name ='party'
res= res.reset_index()
res



# %%
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

# output_file("bar_colormapped.html")

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

source = ColumnDataSource(res)

p = figure(x_range=fruits, plot_height=350, toolbar_location=None, title="Fruit Counts")
p.vbar(x='index', top='per', width=0.9, source=source, legend_field="party",
       line_color='white', fill_color=factor_cmap('party', palette=Spectral6, factors=res['party']))

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 9
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

# %%
den1['tc']=den1['top_c'].apply(_t)
den1['tv']=den1['counted'].apply(_t1)
den1['text'] = den1.apply(_t2,axis=1)

# %%

# %%

# %%
