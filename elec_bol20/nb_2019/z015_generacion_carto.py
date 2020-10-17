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
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: ebol20
#     language: python
#     name: ebol20
# ---

# %%
from elec_bol20 import *
import elec_bol20.util as ebu

# %% [markdown]
# Crea la transformación de cartograma para el modelo de predicciones
# %% [markdown]
# ## abrimos los datos

# %%
#abrimos los datos
data = ebu.open_concat_est_2019()
data

# %%
# añadmios un pequeño jitter a los recintos que lat lon repetidos
lalo = ['LAT', 'LON']
data.groupby(lalo)
n = data.groupby(lalo)['LAT'].count()
n.name = 'repete'
_d = data.reset_index().set_index(lalo)
_d['repete'] = n
_d = _d.reset_index().set_index('ID_RECI')
repete_ = _d['repete']>1
len_rep = len(_d[repete_])
_d.loc[repete_,'LAT'] = _d[repete_]['LAT'] +\
                                   (np.random.random(len_rep)-.5) * .05
_d.loc[repete_,'LON'] = _d[repete_]['LON'] + \
                                   (np.random.random(len_rep)-.5) * .05
data = _d


# %%
# visualicemos las lat y lon resultantes
bokeh.plotting.output_notebook()
p = bokeh.plotting.figure()
p.scatter(x=data['LON'],y=data['LAT'])
bokeh.plotting.show(p)
# %%
# aplicamos un transformacion lineal al radio para acercar a los recintos muy lejanos e.g. china 
st = matplotlib.scale.SymmetricalLogTransform(10,7,1).transform
l = np.linspace(0,200,1000)
plt.scatter(x=l,y=st(l))
plt.show()
x_med = (data['LON'] * data['HAB']).sum() / data['HAB'].sum()
y_med = (data['LAT'] * data['HAB']).sum() / data['HAB'].sum()
y = data['LAT'] - y_med
x = data['LON'] - x_med
r = (x**2 + y**2)**(1/2)
p = bokeh.plotting.figure()
rat = st(r)/r
xrat = x * rat
yrat = y * rat
p.scatter(x=xrat, y=yrat)
bokeh.plotting.show(p, browser='safari')
data['x0'] = xrat
data['y0'] = yrat


# %% [markdown]
# ## Primera pasada de cart

# %%
N = ebu.HAB
x0, y0 = 'x0', 'y0'
x1, y1 = 'x1', 'y1'
_r = .3
sigma_gauss = .5
data0 = data.copy()
x_range = 21
y_range = 20
fun = lambda ds: ds**(1/2)+25

ndf = ebu.get_carto_df(
    N, _r, data0, sigma_gauss,
    x0, x1, x_range,
    y0, y1, y_range,
    fun
)
# %% [markdown]
# ## segunda padada cart

# %%
x0, y0 = 'x1', 'y1'
x1, y1 = 'x2', 'y2'
_r = .2
sigma_gauss = .4
data0 = ndf.copy()
x_range =70
y_range = 65
fun = lambda ds: ds+100

ndf1 = ebu.get_carto_df(
    N, _r, data0, sigma_gauss,
    x0, x1, x_range,
    y0, y1, y_range,
    fun
)
# %% [markdown]
# ## tercera pasada
# %% [markdown]
# acá aplicamos la tercera pasada
# la cual nos da una buena separación de mesas aledañas. 

# %%
#code
x0, y0 = 'x2', 'y2'
x1, y1 = 'x3', 'y3'
_r = 3
sigma_gauss = 1.5
data0 = ndf1.copy()
x_range = 410
y_range = 400
fun = lambda ds: ds+300

ndf2 = ebu.get_carto_df(
    N, _r, data0, sigma_gauss,
    x0, x1, x_range,
    y0, y1, y_range,
    fun, rad = 15
)
# %% [markdown]
# ## empujemos al exterior para que no se mexcle con el pais

# %%
# empujamos los datos que no son bolivia para que la división sea clara
x_med = (ndf2['x3'] * ndf2['HAB']).sum() / ndf2['HAB'].sum()
y_med = (ndf2['y3'] * ndf2['HAB']).sum() / ndf2['HAB'].sum()

ndf2['rat'] = 1
ndf2.loc[~ndf2['BOL'],'rat'] = 1.5

x = ndf2['x3'] - x_med
y = ndf2['y3'] - y_med
r = (x**2 + y**2)**(1/2)
p = bokeh.plotting.figure()
rat = ndf2['rat']
xrat = x * rat
yrat = y * rat
p.scatter(x=xrat, y=yrat)
bokeh.plotting.show(p, browser='safari')
ndf2['x4'] = xrat
ndf2['y4'] = yrat


# %%
ndf3 = ebu.rescale_xy(ndf2, x0='LON', y0='LAT', x3='x4', y3='y4', X='X', Y='Y',
                     fx=1/2,fy=.6
                     )
plt.scatter(ndf3['X'],ndf3['Y'],alpha=.1)
plt.scatter(ndf3['LON'],ndf3['LAT'],alpha=.1)
plt.show()
# %% [markdown]
# ## guardamos los datos

# %%
dfout:pd.DataFrame = ndf3[['X','Y']]
# %%
# save the file
dfout.index.name='ID_RECI'
dfout.reset_index().to_csv(
    ebu.CSV_CART_2019,
    index=False
)
# %%


# %%
# %%
# %%

# %%
