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
# ##### código

# %%
from elec_bol20 import *
import elec_bol20.util as ebu

# %%

df = ebu.open_combine_2019()
df_full = df[df['VV']>0]
# %%
path = os.path.join(ebu.DATA_PATH0, '2019', 'percentil_comp.csv')
df_comp = ebu.traductor_df(path,ebu.TRAD_2019_PER_COMP).set_index('ID_MESA')
df_comp = df_comp[~df_comp.index.duplicated()]
# %%
df = pd.merge(df_full,df_comp,right_index=True,left_index=True,how='inner')


# %%
['ID_RECI', 'HAB', 'CC', 'MAS', '21F', 'PDC', 'VV', 'BL', 'NL', 'X', 'Y',
       'PAIS', 'LAT', 'LON', 'DEN', 'REC', 'MUN', 'BOL', 'P_COMP']
df.columns

# %%
df_.iloc[[]]

# %% [markdown]
#

# %%
l = len(df)
df['x'] = df['X'] + np.random.rand(l) * .3
df['y'] = df['Y'] + np.random.rand(l) * .3
# df['L_DEN'] = np.log(df['DEN'])
# df['L_DEN'] = np.log(df['DEN'])
df_ = df[['x','y','P_COMP','DEN']]



bokeh.plotting.output_notebook()
p = bokeh.plotting.Figure(output_backend="webgl")
src = bokeh.plotting.ColumnDataSource(df_)
src1 = bokeh.plotting.ColumnDataSource({'x':[],'y':[]})


code_slider = """
    var data = source.data
    var f = cb_obj.value
    const data_new = {'x': [], 'y': []}
    var x = data['x']
    var y = data['y']
    var p = data['P_COMP']
    
    for (var i = 0; i < x.length; i++) {
        if (p[i] < f) {
            data_new['x'].push(x[i])
            data_new['y'].push(y[i])
        }
    }
    source1.data = data_new
"""
import bokeh.models.callbacks
# slider
_arg = {'source':src,'source1':src1}
callback_slider = bokeh.models.callbacks.CustomJS(
    args=_arg,
    code=code_slider
)

slider = bokeh.models.Slider(start=5, end=100, value=0, step=1, title="% COMP")
slider.js_on_change('value', callback_slider)

from bokeh.transform import log_cmap

cm = log_cmap('DEN', palette=bokeh.palettes.Viridis11, low=1, high=10000)

p.scatter('x','y',source=src,radius=.05,alpha=1, legend_label='Faltantes')
p.scatter('x','y',source=src,radius=.05,alpha=1,color=cm, legend_label='Densidad')
p.scatter('x','y',source=src1,radius=.05,alpha=1,color='red', legend_label='Reportadas')

p.x_range.start = -80
p.x_range.end   = -50
p.y_range.start = -30
p.y_range.end   = -5

p.legend.click_policy="hide"

layout = p
import bokeh.layouts
layout = bokeh.layouts.column(slider,p)

# %% [markdown]
# #### grágica

# %% [markdown]
# ###### tutorial

# %% [markdown]
# tutorial

# %% [markdown]
# <img src="gifs/2020-10-16 16-25-49.2020-10-16 16_29_50.gif" width="500" align="center">

# %% [markdown]
# ###### interacción

# %%
bokeh.plotting.show(layout)
