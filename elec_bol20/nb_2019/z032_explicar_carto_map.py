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

# %% [markdown]
# # Introducción
# En este notebook introducimos el cartograma de Bolivia basado en la cantidad de votantes. 
# Lo que esta transformación hace, es agrandar en al mapa los lugares con alta densidad y reducir los lugares
# con baja densidad de votantes

# %% [markdown]
# ###### abrir los datos
# abrimos los datos del padrón de votación del 2019

# %%
df = ebu.open_combine_2019()
_mean = ['X', 'Y', 'LAT', 'LON', 'DEN', ]
_sum = ['HAB', 'CC', 'MAS', 'PDC', 'VV']
_first = ['PAIS', 'REC', 'MUN', 'BOL']
_gr = df.groupby('ID_RECI')
rec_df = _gr[_mean].mean()
rec_df[_sum] = _gr[_sum].sum()
rec_df[_first] = _gr[_first].first()

rec_df['D_MAS_CC'] = rec_df['MAS'] - rec_df['CC']
rec_df['d_mas_cc'] = rec_df['D_MAS_CC'] / rec_df['VV'] * 100
rec_df['r'] = np.sqrt(rec_df['HAB']) / 10

res = ebu.lola_to_cart(rec_df['LON'].values, rec_df['LAT'].values)
rec_df['GX'] = res[0]
rec_df['GY'] = res[1]

needed_cols = ['X', 'Y', 'd_mas_cc', 'r', 'LAT', 'LON', 'PAIS', 'REC', 'MUN', 'DEN'
                                                                              'GX', 'GY']

# %%
# order by density
rec_df = rec_df.sort_values('DEN', axis=0, ascending=True)

# %%
# remove nans
rec_df = rec_df.dropna(axis=0)
assert rec_df.isna().sum().sum() == 0

# %%
# cut = pd.IntervalIndex.from_tuples([(0, 50), (50, 500), (500, 1500),(1500,3000),(3000,4000),(4000,7000)])

# %%
# lab = ['B','M','X','A']
lab = [0, 1, 2, 3]
lims = [0, 50, 500, 1500, 10000]
NL = len(lims)
c = pd.cut(rec_df['DEN'], lims,
           labels=lab,
           #              retbins=True
           )

# %%
rec_df['DEN_CUT'] = c.astype(int)

# %%

# %% [markdown]
# ## Carto Densidad

# %% [markdown]
# ###### código

# %%

# output_file(os.path.join(ebu.DATA_FIG_OUT, "carto_map_mas_cc.html"))

# %%
# rec_df_spl = rec_df.sample(200).copy()
rec_df_spl = rec_df.copy()

# %%
# DATA
bokeh.plotting.output_notebook()
cart_init_val = .0
data = rec_df_spl.copy()
data['x'] = data['LON'] * (1 - cart_init_val) + data['X'] * cart_init_val
data['y'] = data['LAT'] * (1 - cart_init_val) + data['Y'] * cart_init_val

# %%
# COLOR
from bokeh.transform import linear_cmap
from bokeh.transform import log_cmap

# cm = linear_cmap('d_mas_cc', palette=ebu.P_DIF[::-1], low=-80, high=80)
# cm = log_cmap('DEN', palette=bokeh.palettes.Viridis11, low=1, high=10000)
cm = linear_cmap('DEN_CUT', palette=bokeh.palettes.Viridis[NL], low=0, high=NL)

# %%
# SOURCES
source_master = ColumnDataSource(data)
source_red_map = ColumnDataSource({'gx': [], 'gy': []})
la, lo = ebu.get_la_lo_bolivia()
source_bol = ColumnDataSource({'la': la, 'lo': lo})
# source_red_car = ColumnDataSource({'lo': [], 'la': []})

# %%
# JS CODE
code_draw_red_map = """
const data = {'gx': [], 'gy': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data['gx'].push(source_master.data.GX[indices[i]])
        data['gy'].push(source_master.data.GY[indices[i]])
}
source_red_map.data = data
"""

code_draw_red_car = """
const data = {'lo': [], 'la': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data['lo'].push(source_master.data.x[indices[i]])
        data['la'].push(source_master.data.y[indices[i]])
}
source_red_car.data = data
"""

code_merged = """
const data_map = {'lo': [], 'la': []}
const data_car = {'gx': [], 'gy': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data_map['lo'].push(source_master.data.x[indices[i]])
        data_map['la'].push(source_master.data.y[indices[i]])
        data_car['gx'].push(source_master.data.GX[indices[i]])
        data_car['gy'].push(source_master.data.GY[indices[i]])
}
source_red_car.data = data_car
source_red_map.data = data_map
"""

code_slider = """
    var data = source.data;
    var f = cb_obj.value
    var x = data['x']
    var y = data['y']
    var Y = data['Y']
    var X = data['X']
    var lat = data['LAT']
    var lon = data['LON']
    for (var i = 0; i < x.length; i++) {
        y[i] = (1-f)*lat[i] + f*Y[i]
        x[i] = (1-f)*lon[i] + f*X[i]
    }
    source.change.emit();
"""

# %%
# FIGURES
pw = 700
cart_fig = Figure(plot_width=pw + int(.2 * pw), plot_height=pw, output_backend="webgl")
map_fig = Figure(plot_width=pw, plot_height=pw,
                 x_axis_type='mercator',
                 y_axis_type='mercator',
                 output_backend="webgl",
                 )
# cb_fig = bokeh.plotting.Figure(plot_height=pw,plot_width=)
# cb_fig.toolbar.logo = None
# cb_fig.toolbar_location = None

# %%
# SCATTER

# noinspection PyUnresolvedReferences
# add tiles
tile_provider = bokeh.tile_providers.get_provider(
    bokeh.tile_providers.Vendors.CARTODBPOSITRON)
map_fig.add_tile(tile_provider)

# scatter in map
map_fig.scatter(
    'GX', 'GY', source=source_master, size='r',
    color=cm
)

cart_fig.line('lo', 'la', source=source_bol, color='black')
cart_fig.scatter('x', 'y', source=source_master, size='r',
                 color=cm
                 )

red_scat_map = map_fig.scatter('gx', 'gy',
                               source=source_red_map, color='red',
                               line_color='green',
                               size=10
                               )
# red_scat_car = cart_fig.scatter('lo', 'la',
# source=source_red_car, color='green')

# add a hover tool that sets the link data for a hovered circle

# callbacks
callback_red_map = CustomJS(
    args={'source_master': source_master,
          'source_red_map': source_red_map,
          # 'source_red_car':source_red_car
          },
    code=code_draw_red_map)
# code = code_merged)

# callback_red_car = CustomJS(
#     args={'source_master': source_master, 'source_red_car': source_red_car},
#     code=code_draw_red_car)

# tools

ebu.TOOL_TIPS1 = [
    ('INS', '@HAB'),
    ('PAIS', '@PAIS'),
    ('MUN', '@MUN'),
    ('REC', '@REC'),
    ('DEN %', '@DEN')
    # ('PAIS', '@PAIS'),
]

hover_cart = bokeh.models.HoverTool(
    tooltips=ebu.TOOL_TIPS1,
    callback=callback_red_map,
    # renderers = [red_scat_car]

)
cart_fig.add_tools(hover_cart, )

hover_map = bokeh.models.HoverTool(
    tooltips=ebu.TOOL_TIPS1,
    # callback=callback_red_car,
    # renderers = [red_scat_map]
)
map_fig.add_tools(hover_map, )

# slider
callback_slider = CustomJS(args=dict(source=source_master),
                           code=code_slider)

slider = Slider(start=0, end=1, value=cart_init_val, step=.01, title="carto")
slider.js_on_change('value', callback_slider)

# %%
# COLOR BAR

cb = bokeh.models.ColorBar(
    color_mapper=cm['transform'], width=30,
    location=(0, 0),
    title="DEN (N/km^2)",
    # margin=0,padding=0,
    title_standoff=10,
    #     ticker=bokeh.models.LogTicker(),
    major_label_overrides={0: "0", 1: "50", 2: "500", 3: "1500", 4: "3000", 5: "4000", 6: "7000"}
)

cart_fig.add_layout(cb, 'left')

# layout = row(column(slider, cart_f),map_f)
# layout = bokeh.layouts.gridplot(
#     [[slider, None], [cart_fig, map_fig]]
#     , merge_tools=False
# )
layout = bokeh.layouts.column([slider, cart_fig])

cart_fig.x_range.start = -80
cart_fig.x_range.end = -45
cart_fig.y_range.start = -30
cart_fig.y_range.end = 0

_ll = ebu.lola_to_cart(lo=[-80, -45], la=[-30, 0])
map_fig.x_range.start = _ll[0][0]
map_fig.x_range.end = _ll[0][1]
map_fig.y_range.start = _ll[1][0]
map_fig.y_range.end = _ll[1][1]

# %% [markdown]
# ###### gráfica

# %% [markdown]
# En el mapa de abajo, cada punto corresponde un recinto electoral, su color está relacionado con la densidad de votantes, y su tamaño con la cantidad de votos.
# Mueve el slider (carto) para ver la deformación. 

# %%


# %%
bokeh.plotting.show(layout)

# %% [markdown]
# ## Carto MAS - CC

# %% [markdown]
# ###### código

# %%

# output_file(os.path.join(ebu.DATA_FIG_OUT, "carto_map_mas_cc.html"))

# %%
# rec_df_spl = rec_df.sample(200).copy()
rec_df_spl = rec_df.copy()

# %%
# DATA
bokeh.plotting.output_notebook()
cart_init_val = .5
data = rec_df_spl.copy()
data['x'] = data['LON'] * (1 - cart_init_val) + data['X'] * cart_init_val
data['y'] = data['LAT'] * (1 - cart_init_val) + data['Y'] * cart_init_val

# %%
# COLOR
from bokeh.transform import linear_cmap

# from bokeh.transform import log_cmap

cm = linear_cmap('d_mas_cc', palette=ebu.P_DIF[::-1], low=-80, high=80)
# cm = log_cmap('DEN', palette=bokeh.palettes.Viridis11, low=1, high=10000)

# %%
# SOURCES
source_master = ColumnDataSource(data)
source_red_map = ColumnDataSource({'gx': [], 'gy': []})
la, lo = ebu.get_la_lo_bolivia()
source_bol = ColumnDataSource({'la': la, 'lo': lo})
# source_red_car = ColumnDataSource({'lo': [], 'la': []})

# %%
# JS CODE
code_draw_red_map = """
const data = {'gx': [], 'gy': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data['gx'].push(source_master.data.GX[indices[i]])
        data['gy'].push(source_master.data.GY[indices[i]])
}
source_red_map.data = data
"""

code_draw_red_car = """
const data = {'lo': [], 'la': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data['lo'].push(source_master.data.x[indices[i]])
        data['la'].push(source_master.data.y[indices[i]])
}
source_red_car.data = data
"""

code_merged = """
const data_map = {'lo': [], 'la': []}
const data_car = {'gx': [], 'gy': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data_map['lo'].push(source_master.data.x[indices[i]])
        data_map['la'].push(source_master.data.y[indices[i]])
        data_car['gx'].push(source_master.data.GX[indices[i]])
        data_car['gy'].push(source_master.data.GY[indices[i]])
}
source_red_car.data = data_car
source_red_map.data = data_map
"""

code_slider = """
    var data = source.data;
    var f = cb_obj.value
    var x = data['x']
    var y = data['y']
    var Y = data['Y']
    var X = data['X']
    var lat = data['LAT']
    var lon = data['LON']
    for (var i = 0; i < x.length; i++) {
        y[i] = (1-f)*lat[i] + f*Y[i]
        x[i] = (1-f)*lon[i] + f*X[i]
    }
    source.change.emit();
"""

# FIGURES
pw = 700
cart_fig = Figure(plot_width=pw + int(.2 * pw), plot_height=pw, output_backend="webgl")
map_fig = Figure(plot_width=pw, plot_height=pw,
                 x_axis_type='mercator',
                 y_axis_type='mercator',
                 output_backend="webgl",
                 )
# cb_fig = bokeh.plotting.Figure(plot_height=pw,plot_width=)
# cb_fig.toolbar.logo = None
# cb_fig.toolbar_location = None

# %%
# SCATTER

# noinspection PyUnresolvedReferences
# add tiles
tile_provider = bokeh.tile_providers.get_provider(
    bokeh.tile_providers.Vendors.CARTODBPOSITRON)
map_fig.add_tile(tile_provider)

# scatter in map
map_fig.scatter(
    'GX', 'GY', source=source_master, size='r',
    color=cm
)

cart_fig.line('lo', 'la', source=source_bol, color='black')
cart_fig.scatter('x', 'y', source=source_master, size='r',
                 color=cm
                 )

red_scat_map = map_fig.scatter('gx', 'gy',
                               source=source_red_map, color='red',
                               line_color='green',
                               size=10
                               )
# red_scat_car = cart_fig.scatter('lo', 'la',
# source=source_red_car, color='green')

# add a hover tool that sets the link data for a hovered circle

# callbacks
callback_red_map = CustomJS(
    args={'source_master': source_master,
          'source_red_map': source_red_map,
          # 'source_red_car':source_red_car
          },
    code=code_draw_red_map)
# code = code_merged)

# callback_red_car = CustomJS(
#     args={'source_master': source_master, 'source_red_car': source_red_car},
#     code=code_draw_red_car)

# tools

ebu.TOOL_TIPS1 = [
    ('INS', '@HAB'),
    ('PAIS', '@PAIS'),
    ('MUN', '@MUN'),
    ('REC', '@REC'),
    #     ('DEN %', '@DEN')
    ('MAS-CC', '@d_mas_cc')
    # ('PAIS', '@PAIS'),
]

hover_cart = bokeh.models.HoverTool(
    tooltips=ebu.TOOL_TIPS1,
    callback=callback_red_map,
    # renderers = [red_scat_car]

)
cart_fig.add_tools(hover_cart, )

hover_map = bokeh.models.HoverTool(
    tooltips=ebu.TOOL_TIPS1,
    # callback=callback_red_car,
    # renderers = [red_scat_map]
)
map_fig.add_tools(hover_map, )

# slider
callback_slider = CustomJS(args=dict(source=source_master),
                           code=code_slider)

slider = Slider(start=0, end=1, value=cart_init_val, step=.01, title="carto")
slider.js_on_change('value', callback_slider)

# %%
# COLOR BAR

cb = bokeh.models.ColorBar(
    color_mapper=cm['transform'], width=30,
    location=(0, 0),
    #     title="DEN (N/km^2)",
    title="MAS-CC%",
    # margin=0,padding=0,
    title_standoff=10,
    #     ticker=bokeh.models.LogTicker()
)

cart_fig.add_layout(cb, 'left')

# layout = row(column(slider, cart_f),map_f)
# layout = bokeh.layouts.gridplot(
#     [[slider, None], [cart_fig, map_fig]]
#     , merge_tools=False
# )
layout = bokeh.layouts.column([slider, cart_fig])

cart_fig.x_range.start = -80
cart_fig.x_range.end = -45
cart_fig.y_range.start = -30
cart_fig.y_range.end = 0

_ll = ebu.lola_to_cart(lo=[-80, -45], la=[-30, 0])
map_fig.x_range.start = _ll[0][0]
map_fig.x_range.end = _ll[0][1]
map_fig.y_range.start = _ll[1][0]
map_fig.y_range.end = _ll[1][1]

# %% [markdown]
# ###### gráfica

# %% [markdown]
# En el mismo mapa podemos mostrar la diferencia de MAS con CC 

# %%
bokeh.plotting.show(layout)

# %% [markdown]
# ## Carto MAS - CC

# %% [markdown]
# ###### código

# %%

# output_file(os.path.join(ebu.DATA_FIG_OUT, "carto_map_mas_cc.html"))

# %%
# rec_df_spl = rec_df.sample(200).copy()
rec_df_spl = rec_df.copy()

# %%
# DATA
bokeh.plotting.output_notebook()
cart_init_val = .5
data = rec_df_spl.copy()
data['x'] = data['LON'] * (1 - cart_init_val) + data['X'] * cart_init_val
data['y'] = data['LAT'] * (1 - cart_init_val) + data['Y'] * cart_init_val

# %%
# COLOR
from bokeh.transform import linear_cmap
from bokeh.transform import log_cmap

cm = linear_cmap('d_mas_cc', palette=ebu.P_DIF[::-1], low=-80, high=80)
# cm = log_cmap('DEN', palette=bokeh.palettes.Viridis11, low=1, high=10000)

# %%
# SOURCES
source_master = ColumnDataSource(data)
source_red_map = ColumnDataSource({'gx': [], 'gy': []})
la, lo = ebu.get_la_lo_bolivia()
source_bol = ColumnDataSource({'la': la, 'lo': lo})
# source_red_car = ColumnDataSource({'lo': [], 'la': []})

# %%
# JS CODE
code_draw_red_map = """
const data = {'gx': [], 'gy': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data['gx'].push(source_master.data.GX[indices[i]])
        data['gy'].push(source_master.data.GY[indices[i]])
}
source_red_map.data = data
"""

code_draw_red_car = """
const data = {'lo': [], 'la': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data['lo'].push(source_master.data.x[indices[i]])
        data['la'].push(source_master.data.y[indices[i]])
}
source_red_car.data = data
"""

code_merged = """
const data_map = {'lo': [], 'la': []}
const data_car = {'gx': [], 'gy': []}
const indices = cb_data.index.indices
for (var i = 0; i < indices.length; i++) {
        data_map['lo'].push(source_master.data.x[indices[i]])
        data_map['la'].push(source_master.data.y[indices[i]])
        data_car['gx'].push(source_master.data.GX[indices[i]])
        data_car['gy'].push(source_master.data.GY[indices[i]])
}
source_red_car.data = data_car
source_red_map.data = data_map
"""

code_slider = """
    var data = source.data;
    var f = cb_obj.value
    var x = data['x']
    var y = data['y']
    var Y = data['Y']
    var X = data['X']
    var lat = data['LAT']
    var lon = data['LON']
    for (var i = 0; i < x.length; i++) {
        y[i] = (1-f)*lat[i] + f*Y[i]
        x[i] = (1-f)*lon[i] + f*X[i]
    }
    source.change.emit();
"""

# FIGURES
pw = 400
cart_fig = Figure(plot_width=pw + int(.2 * pw), plot_height=pw, output_backend="webgl")
map_fig = Figure(plot_width=pw, plot_height=pw,
                 x_axis_type='mercator',
                 y_axis_type='mercator',
                 output_backend="webgl",
                 )
# cb_fig = bokeh.plotting.Figure(plot_height=pw,plot_width=)
# cb_fig.toolbar.logo = None
# cb_fig.toolbar_location = None

# %%
# SCATTER

# noinspection PyUnresolvedReferences
# add tiles
tile_provider = bokeh.tile_providers.get_provider(
    bokeh.tile_providers.Vendors.CARTODBPOSITRON)
map_fig.add_tile(tile_provider)

# scatter in map
map_fig.scatter(
    'GX', 'GY', source=source_master, size='r',
    color=cm
)

cart_fig.line('lo', 'la', source=source_bol, color='black')
cart_fig.scatter('x', 'y', source=source_master, size='r',
                 color=cm
                 )

red_scat_map = map_fig.scatter('gx', 'gy',
                               source=source_red_map, color='red',
                               line_color='green',
                               size=10
                               )
# red_scat_car = cart_fig.scatter('lo', 'la',
# source=source_red_car, color='green')

# add a hover tool that sets the link data for a hovered circle

# callbacks
callback_red_map = CustomJS(
    args={'source_master': source_master,
          'source_red_map': source_red_map,
          # 'source_red_car':source_red_car
          },
    code=code_draw_red_map)
# code = code_merged)

# callback_red_car = CustomJS(
#     args={'source_master': source_master, 'source_red_car': source_red_car},
#     code=code_draw_red_car)

# tools

ebu.TOOL_TIPS1 = [
    ('INS', '@HAB'),
    ('PAIS', '@PAIS'),
    ('MUN', '@MUN'),
    ('REC', '@REC'),
    ('MAS-CC%', '@d_mas_cc')
    # ('DEN %', '@DEN')
    # ('PAIS', '@PAIS'),
]

hover_cart = bokeh.models.HoverTool(
    tooltips=ebu.TOOL_TIPS1,
    callback=callback_red_map,
    # renderers = [red_scat_car]

)
cart_fig.add_tools(hover_cart, )

hover_map = bokeh.models.HoverTool(
    tooltips=ebu.TOOL_TIPS1,
    # callback=callback_red_car,
    # renderers = [red_scat_map]
)
map_fig.add_tools(hover_map, )

# slider
callback_slider = CustomJS(args=dict(source=source_master),
                           code=code_slider)

slider = Slider(start=0, end=1, value=cart_init_val, step=.01, title="carto")
slider.js_on_change('value', callback_slider)

# %%
# COLOR BAR

cb = bokeh.models.ColorBar(
    color_mapper=cm['transform'], width=30,
    location=(0, 0),
    #     title="DEN (N/km^2)",
    title="MAS-CC%",
    # margin=0,padding=0,
    title_standoff=10,
    # ticker=bokeh.models.LogTicker()
)

cart_fig.add_layout(cb, 'left')

# layout = row(column(slider, cart_f),map_f)
layout = bokeh.layouts.gridplot(
    [[slider, None], [cart_fig, map_fig]]
    , merge_tools=False
)
# layout = bokeh.layouts.column([slider, cart_fig])

cart_fig.x_range.start = -75
cart_fig.x_range.end = -50
cart_fig.y_range.start = -25
cart_fig.y_range.end = -5

_ll = ebu.lola_to_cart(lo=[-75, -50], la=[-25, -5])
map_fig.x_range.start = _ll[0][0]
map_fig.x_range.end = _ll[0][1]
map_fig.y_range.start = _ll[1][0]
map_fig.y_range.end = _ll[1][1]

# %% [markdown]
# ###### gráfica

# %% [markdown]
# Y también podemos hacer correspondencia entre el cartograma (izquierda) y el mapa real(derecha)

# %%
bokeh.plotting.show(layout)

# %%

# %%
