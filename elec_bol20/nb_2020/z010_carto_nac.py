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
# ---

# %%

from elec_bol20 import *
import elec_bol20.util as ebu



# %%
# def main():
# %%

data = pd.read_excel(ebu.GEO_PATH_V1)
lalo = ['latitud', 'longitud']
data.groupby(lalo)
n = data.groupby(lalo)['latitud'].count()
n.name = 'repete'
_d = data.reset_index().set_index(lalo)
_d['repete'] = n
_d = _d.reset_index().set_index('index')
_d.loc[_d['repete']>1,'latitud'] = _d[_d['repete']>1]['latitud'] +\
                                   (np.random.random(1)-.5) * .05
_d.loc[_d['repete']>1,'longitud'] = _d[_d['repete']>1]['longitud'] + \
                                   (np.random.random(1)-.5) * .05
data = _d


# %%
data = data[data['NombrePais'] == 'Bolivia']
data = data.rename({'latitud': 'y0', 'longitud': 'x0'}, axis=1)

N = ebu.HAB
x0, y0 = 'x0', 'y0'
x1, y1 = 'x1', 'y1'
_r = .05
sigma_gauss = 1
data0 = data.copy()
x_range = 11
y_range = 10
fun = lambda ds: ds**(1/2)+3

ndf = ebu.get_carto_df(
    N, _r, data0, sigma_gauss,
    x0, x1, x_range,
    y0, y1, y_range,
    fun
)
# %%
x0, y0 = 'x1', 'y1'
x1, y1 = 'x2', 'y2'
_r = 1
sigma_gauss = .5
data0 = ndf.copy()
x_range =200
y_range = 200
fun = lambda ds: ds+1000

ndf1 = ebu.get_carto_df(
    N, _r, data0, sigma_gauss,
    x0, x1, x_range,
    y0, y1, y_range,
    fun
)
# %%
# %%
x0, y0 = 'x2', 'y2'
x1, y1 = 'x3', 'y3'
_r = 2
sigma_gauss = .5
data0 = ndf1.copy()
x_range = 510
y_range = 500
fun = lambda ds: ds+200

ndf2 = ebu.get_carto_df(
    N, _r, data0, sigma_gauss,
    x0, x1, x_range,
    y0, y1, y_range,
    fun
)

# if __name__ == '__main__':
#     main()

