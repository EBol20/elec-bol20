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
# import
from elec_bol20 import *
import elec_bol20.util as ebu
import bokeh.layouts
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure
# output_file, show
import bokeh.tile_providers

# %%
# p = os.path.pardir(ebu.DIR)


# %%
W_CARTO = 400
H_CARTO = 400
ANGLE_DENS = .35
SIZE_DENS = "8pt"
HEIGHT_BDENS = 250
H_FIG_PARTY = 250
WW = W_CARTO
BROWSER = 'safari'
MIN_WITH = 700
MAX_WITH = 800
PATH_OUT = 'docs/Ejemplos/z050_panel.html'
FILE_OUT = os.path.join(os.path.dirname(ebu.DIR),
                                        PATH_OUT)

COL_LLEGO = '#aaaaaa'
COL_FALTA = '#db2879'

# bokeh.plotting.output_file(os.path.join(os.path.dirname(ebu.DIR),
#                                         PATH_OUT))
# bokeh.plotting.output_notebook()

# %% [markdown]
# ## code

# %%
df2 = ebu.get_dataframe_2020()


# %%


# %%


# %%
bokeh.plotting.output_notebook()

ll = len(df2)
np.random.seed(100)
df2['xj'] = df2['X'] + np.random.rand(ll) * .5
np.random.seed(200)
df2['yj'] = df2['Y'] + np.random.rand(ll) * .5
cols = ['yj', 'xj', 'PAIS', 'MUN', 'REC', 'HAB', 'COU']

df2['COU'] = 'No'
df2.loc[df2['COUNT'], 'COU'] = 'Sí'

s1 = df2[df2['COUNT']][cols]
s2 = df2[~df2['COUNT']][cols]
sr1 = bokeh.models.ColumnDataSource(s1)
sr2 = bokeh.models.ColumnDataSource(s2)

fig_carto = bokeh.plotting.figure(output_backend="webgl", height=H_CARTO, width=W_CARTO)
fig_carto.scatter(x='xj', y='yj', source=sr2, color=COL_FALTA, radius=.05,
                  alpha=1,
                  legend_label='Mesas por computar (haz click)')
fig_carto.scatter(x='xj', y='yj', source=sr1, color=COL_LLEGO, radius=.05,
                  alpha=1,
                  legend_label='Mesas computadas (haz click)')
fig_carto.legend.click_policy = "hide"

# %%
dfn = df2.copy()
dfn.loc[~dfn['BOL'], 'DEN_CODES'] = -1

# %%
_df = dfn
gr = _df.groupby('DEN_CODES')
den = gr[['HAB']].sum()
den['cum'] = den['HAB'].cumsum()
tot = den['HAB'].sum()
den['mid'] = den['cum'] - den['HAB'] / 2
den['top'] = 100
den['width'] = den['HAB'] - (tot * .01)
den1 = den.copy()

# %%
_df = dfn[dfn['COUNT']]
gr = _df.groupby('DEN_CODES')
den = gr[['HAB']].sum()
den['cum'] = den['HAB'].cumsum()
tot = den['HAB'].sum()
den['mid'] = den['cum'] - den['HAB'] / 2
den['top'] = 1
den['width'] = den['HAB'] - (tot * .01)
den2 = den.copy()

# %%
dfn['HAB']

# %%
den1['counted'] = den2['HAB'].astype(np.int64)

# %%
den1['top_c'] = den1['counted'] / den1['HAB'] * 100

# %%
den1.loc[-1, 'mid'] = den1.loc[-1, 'mid'] - 1000000

# %%

# %%

# %%
df2[df2['COUNT']]['HAB'].sum()


def _t(s):
    if np.isnan(s): s = 0
    return f'{s:0.1f}'


def _t1(s):
    if np.isnan(s): s = 0
    return f'{s:0.0f}'


def _t2(r):
    #     return f'{r["tv"]} ({r["tc"]} %)'
    return f'{r["tc"]}%'


den1['tc'] = den1['top_c'].apply(_t)
den1['tv'] = den1['counted'].apply(_t1)
den1['text'] = den1.apply(_t2, axis=1)

# %%

# %%


fig_bar_dens = bokeh.plotting.figure(height=HEIGHT_BDENS, width=WW)
# fi = bokeh.plotting.figure()
fig_bar_dens.vbar(x=den1['mid'], width=den1['width'], top=den1['top'],
                  color=COL_FALTA)
fig_bar_dens.vbar(x=den1['mid'], width=den1['width'], top=den1['top_c'],
                  color=COL_LLEGO)
fig_bar_dens.title.text = ''

x = den1[den1.index >= 0]['mid'].mean()
fig_bar_dens.text(x=[x], y=[140], text=['Nacional'])

an = ANGLE_DENS
x = den1[den1.index == 0]['mid'].mean()
fig_bar_dens.text(x=[x], y=[101], text=['Densidad baja (0-50)'], angle=an,
                  text_font_size=SIZE_DENS)

x = den1[den1.index == 1]['mid'].mean()
fig_bar_dens.text(x=[x], y=[101], text=['Densidad media (50-500)'], angle=an,
                  text_font_size=SIZE_DENS)

x = den1[den1.index == 2]['mid'].mean()
fig_bar_dens.text(x=[x], y=[101], text=['Densidad moderada (500-1500)'],
                  angle=an, text_font_size=SIZE_DENS)

x = den1[den1.index == 3]['mid'].mean()
fig_bar_dens.text(x=[x], y=[101], text=['Densidad alta > 1500'], angle=an,
                  text_font_size=SIZE_DENS)

x = den1[den1.index < 0]['mid'].mean()
fig_bar_dens.text(x=[x], y=[110], text=['Exterior'], text_align='center')
fig_bar_dens.xaxis.visible = False
fig_bar_dens.xgrid.visible = False
fig_bar_dens.ygrid.visible = False
fig_carto.yaxis.visible = False
fig_carto.yaxis.visible = False
fig_bar_dens.y_range.start = 0
fig_bar_dens.y_range.end = 160
fig_bar_dens.yaxis.axis_label = "Porcentaje"
ppp = den1['counted'].sum() / den1['HAB'].sum() * 100
fig_bar_dens.title.text = f'Porcentaje de votos computados por densidad (total computado={ppp:0.1f}%)'
fig_bar_dens.xaxis.axis_label = f'Porcentaje total de votos computados = ({ppp:0.1f}%)'
fig_bar_dens.toolbar.logo = None
fig_bar_dens.toolbar_location = None

fig_carto.title.text = "Cartolocación de las mesas"

for l, fig_party in den1.iterrows():
    if l == -1:
        x = fig_party['mid'] + 400000
    else:
        x = fig_party['mid']

    fig_bar_dens.text(x=x, y=[fig_party['tc']], text=[fig_party['text']],
                      text_align='center', text_font_size="8pt",
                      color=[COL_LLEGO])

_c = ['CREEMOS', 'MAS', 'FPV', 'PAN_BOL', 'CC']
dd = df2[[*_c, 'VV']].copy()
res = dd[_c].sum() / dd['VV'].sum() * 100
res.name = 'per'
res.index.name = 'party'
res = res.reset_index()
res['i'] = res.index + .5
se = pd.Series(ebu.C_DIC)
se.name = 'colors'
res = pd.merge(res, se, left_on='party', right_index=True)

source = ColumnDataSource(res)

fig_party = bokeh.plotting.figure(x_range=res['party'], toolbar_location=None,
                                  height=H_FIG_PARTY, width=WW)
fig_party.vbar(x='i', top='per', width=0.9, source=source,
               line_color='white',
               fill_color=bokeh.transform.factor_cmap('party',
                                                      palette=res['colors'],
                                                      factors=res['party']))


def _f(p): return f'{p:0.1f}%'


res['t'] = res['per'].apply(_f)

fig_party.text(x=res['i'], y=res['per'], text=res['t'], text_align='center')

fig_party.xgrid.grid_line_color = None
fig_party.y_range.start = 0
fig_party.y_range.end = np.ceil(res['per'].max() / 20) * 20
fig_party.title.text =\
    f'Porcentaje sobre el total de votos válidos computados ({ppp:0.1f}%)'

TOOL_TIP = [
    ('Inscritos', '@HAB'),
    ('PAIS, Municipalidad', '@PAIS, @MUN'),
    ('Recinto', '@REC'),
    ('Computada', '@COU'),
    # ('MAS [%]', '@mas{0.0}'),
    # ('CC [%]','@cc{0.0}'),
    # ('Diferencia [%]', '@ad_mas_cc{0.0} (@mas_o_cc)'),
    ('------', '------')
    # ('DEN %', '@DEN')
    # ('PAIS', '@PAIS'),
]

hover_map = bokeh.models.HoverTool(
    tooltips=TOOL_TIP,
    # callback=callback_red_car,
    # renderers = [red_scat_map]
)
fig_carto.add_tools(hover_map)

l0 = bokeh.layouts.column([fig_party, fig_bar_dens,fig_carto],sizing_mode='scale_width')
# l0 = bokeh.layouts.row([row, fig_carto],
#                           sizing_mode='scale_width')

fig_party.y_range.end = 70
lay = l0
l0.max_width = MAX_WITH
l0.min_width = MIN_WITH
# lay = bokeh.layouts.row([l0,f])
# lay = p
# %% [markdown]
# ## graph

# %%

# %%
bokeh.plotting.show(lay, browser=BROWSER)


# %% [markdown]
# ## save

# %%
bokeh.plotting.save(l0,FILE_OUT)

# %%
ebu.get_bolivian_time(0)

# %%

# %%

# %%
