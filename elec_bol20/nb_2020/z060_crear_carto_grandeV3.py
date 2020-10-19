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
from bokeh.plotting import Figure, output_file, show
import bokeh.tile_providers

# %% [markdown]
# ###### abrir los datos
# abrimos los datos del padrón de votación del 2019

# %%

# %%

# %%
df2= ebu.get_dataframe_2020()



# %%

# %%
#DEFINICIONES
MYE = -5
MYS = -25
MXE = -50
MXS = -75
CYE = -5
CYS = -25
CXE = -50
CXS = -75

# MYE = 70
# MYS = -70
# MXE = -120
# MXS = 150
# CYE = -0
# CYS = -35
# CXE = -40
# CXS = -85



BAR_TITLE = "CC  < diferencia [%] >  MAS"
# PIXELS
FIG_WIDTH = 700
C_BAR_HIGH = 80
C_BAR_LOW = -80
PALETTE = ebu.P_DIF
CART_SLIDER_INIT = .90
FILE_OUT = ebu.DIR+'/htlml_1_intermedios/2020/z060_carto_map_mas_c0_2020c.html'

MAP_CIRCLE_SIZE_OFFSET = 5
RATIO_CIRCLE_MAP = 7
RATIO_CIRCLE_CARTO = 300
TOOL_TIP = [
    ('Inscritos', '@HAB'),
    ('PAIS, Municipalidad', '@PAIS, @MUN'),
    ('Recinto', '@REC'),
    ('MAS [%]', '@mas{0.0}'),
    ('CC [%]','@cc{0.0}'),
    ('Diferencia [%]', '@ad_mas_cc{0.0} (@mas_o_cc)'),
    ('------','------')
    # ('DEN %', '@DEN')
    # ('PAIS', '@PAIS'),
]
#




_mean = ['X', 'Y', 'LAT', 'LON', 'DEN', ]
_sum = ['HAB', 'CC', 'MAS', 'VV']
_first = ['PAIS', 'REC', 'MUN', 'BOL']
# agrupamos por recinto
_gr = df2.groupby('ID_RECI')
rec_df = _gr[_mean].mean()
rec_df[_sum] = _gr[_sum].sum()
rec_df[_first] = _gr[_first].first()

rec_df['D_MAS_CC'] = rec_df['MAS'] - rec_df['CC']
rec_df['d_mas_cc'] = rec_df['D_MAS_CC'] / rec_df['VV'] * 100
rec_df['r'] = np.sqrt(rec_df['HAB']) / RATIO_CIRCLE_CARTO
rec_df['r2'] = np.sqrt(rec_df['HAB']) / RATIO_CIRCLE_MAP + MAP_CIRCLE_SIZE_OFFSET


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

# %%
# DATA
# bokeh.plotting.output_notebook()
bokeh.plotting.output_file(FILE_OUT)
cart_init_val = CART_SLIDER_INIT
data = rec_df_spl.copy()
data['x'] = data['LON'] * (1 - cart_init_val) + data['X'] * cart_init_val
data['y'] = data['LAT'] * (1 - cart_init_val) + data['Y'] * cart_init_val

# %%
# COLOR

from bokeh.transform import linear_cmap
from bokeh.transform import log_cmap

cm = linear_cmap('d_mas_cc', palette=PALETTE, low=C_BAR_LOW, high=C_BAR_HIGH)
# cm = log_cmap('DEN', palette=bokeh.palettes.Viridis11, low=1, high=10000)

# %%
# SOURCES
data['mas'] = data['MAS']/data['VV'] * 100
data['cc'] = data['CC']/data['VV'] * 100
data['ad_mas_cc'] = data['d_mas_cc'].abs()
data['mas_o_cc'] = 'n'
data.loc[data['d_mas_cc']>=0,'mas_o_cc'] = 'MAS'
data.loc[data['d_mas_cc']<0,'mas_o_cc'] = 'CC'

# %%

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
for (var i = 0; i < indices.length; i++ ) {
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
pw = FIG_WIDTH
cart_fig = Figure(plot_width=pw, plot_height=pw, output_backend="webgl")
map_fig = Figure(plot_width=pw, plot_height=pw,
                 x_axis_type='mercator',
                 y_axis_type='mercator',
                 output_backend="webgl",
                 )
cart_fig.background_fill_color = "grey"
cart_fig.background_fill_alpha = .5
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
    'GX', 'GY', source=source_master, size='r2',
    color=cm
)

#todo if we wont use map then we nee to delete the source
# cart_fig.line('lo', 'la', source=source_bol, color='black')
cart_fig.scatter('x', 'y', source=source_master, radius='r',
                 color=cm
                 )

red_scat_map = map_fig.circle_cross('gx', 'gy',
                                    source=source_red_map,
                                    #                                color='red',
                                    fill_color=None,
                                    #                                line_color='green',
                                    size=20,
                                    line_color="white",
                                    line_width=4
                                    )

red_scat_map = map_fig.circle_cross('gx', 'gy',
                                    source=source_red_map,
                                    #                                color='red',
                                    fill_color=None,
                                    #                                line_color='green',
                                    size=20,
                                    line_color="red",
                                    line_width=1
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



hover_cart = bokeh.models.HoverTool(
    tooltips=TOOL_TIP,
    callback=callback_red_map,
    # renderers = [red_scat_car]

)
cart_fig.add_tools(hover_cart, )

hover_map = bokeh.models.HoverTool(
    tooltips=TOOL_TIP,
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
ml = {int(i):str(np.abs(i)) for i in np.arange(-80,81,20)}
cb = bokeh.models.ColorBar(
    color_mapper=cm['transform'],
    # width=int(.9*FIG_WIDTH),
    location=(0, 0),
    #     title="DEN (N/km^2)",
    # title=(BAR_TITLE),
    # margin=0,padding=0,
    title_standoff=10,
    # ticker=bokeh.models.LogTicker(),
    orientation='horizontal',
    major_label_overrides=ml


)

cart_fig.add_layout(cb, 'above')
# cb.title_text_align = 'left'
cart_fig.title.text=BAR_TITLE
cart_fig.title.align='center'

# layout = row(column(slider, cart_f),map_f)
layout = bokeh.layouts.gridplot(
    [[slider, None], [cart_fig, map_fig]]
    , merge_tools=False,
    sizing_mode='scale_width'
)
layout.max_width = 700
# layout = bokeh.layouts.column([slider, cart_fig])

cart_fig.x_range.start = CXS
cart_fig.x_range.end = CXE
cart_fig.y_range.start = CYS
cart_fig.y_range.end = CYE

_ll = ebu.lola_to_cart(lo=[MXS, MXE], la=[MYS, MYE])
map_fig.x_range.start = _ll[0][0]
map_fig.x_range.end = _ll[0][1]
map_fig.y_range.start = _ll[1][0]
map_fig.y_range.end = _ll[1][1]

cart_fig.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
cart_fig.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
cart_fig.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
cart_fig.yaxis.minor_tick_line_color = None
cart_fig.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
cart_fig.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
# %% [markdown]
# ###### gráfica

# %% [markdown]
# Y también podemos hacer correspondencia entre el cartograma (derecha) y el mapa real(izquierda)

# %%
bokeh.plotting.show(layout)

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
