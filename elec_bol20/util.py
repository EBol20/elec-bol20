import elec_bol20 as eb
from elec_bol20 import *
from scipy.ndimage import gaussian_filter
import datetime
# %%
# CONSTANTS

DIR = eb.__path__[0]

HAB = 'HAB'
# lon = 'longitud'
# lat = 'latitud'

CART_PATH = os.path.join(DIR, 'cart')
CART_CMD = os.path.join(CART_PATH, 'cart')
# %%
DATA_PATH0 = os.path.join(DIR, 'datos_0_crudos')
DATA_PATH1 = os.path.join(DIR, 'datos_1_intermedios')
DATA_PATH2 = os.path.join(DIR, 'datos_2_finales')
DATA_FIG_OUT = os.path.join(DIR, 'figuras_out')

DATA_PATH0_2020 = os.path.join(DATA_PATH0,'2020')
DATA_PATH1_2020 = os.path.join(DATA_PATH1,'2020')
DATA_PATH2_2020 = os.path.join(DATA_PATH2,'2020')

CSV_EST_NAC_2019 = os.path.join(DATA_PATH0, '2019', 'estad_nac.csv')
CSV_EST_EXT_2019 = os.path.join(DATA_PATH0, '2019', 'estad_ext.csv')
GEO_PATH_V1 = os.path.join(DATA_PATH0, '2020', 'geo2020.xlsx')

# CSV_CART_NAC_2019 = os.path.join(DATA_PATH1,'2019','cart_reci_nac.csv')
# CSV_CART_EXT_2019 = os.path.join(DATA_PATH1,'2019','cart_reci_ext.csv')
CSV_CART_2019 = os.path.join(DATA_PATH1, '2019', 'cart_reci.csv')
CSV_RES_2019_COMP = os.path.join(DATA_PATH0, '2019', 'final_comp.csv')

DEN_LIMS  = [0, 50, 500, 1500, 10000]
DEN_CODES = [0,1,2,3]

COL_STANDARD = [
    "LAT", "LON",
    "ID_MESA",  # id mesa  e.g 11111
    "ID_RECI",  # id recinto e.g 111
    "HAB",  # n. de inscritos habilitados
    "VV",  # votos validos
    'VT',  # votos totales VV + BL + NU
    "MAS", "CC", "CRE", "PDV",  # partidos políticos (en valor absoluto)
    "D_MAS_CC",  # diferencia mas cc
    "mas", "cc", "cre", "pdv",  # absoluto/VV * 100 [i.e. %]
    "d_mas_cc",  # diferencia mas cc
    "X", "Y",  # coordinadas cartograma
    "GX", "GY",  # coordinadas cartograma en tile format
    "BOL",  # true bolivia, False mundo
    "BL",  # blancos
    "NU",  # nulos,m
    "NUA",  # nulos agregado con partidos descalificados
    "PAIS",  # país
    "DEN",  # densidad n/km^2
    "N_MESAS",  # numero de mesas,
    "REC",  # nombre recinto
    "MUN",  # nombre municipio,
    "_p",  # prediccion
    "_r",  # residual,
    "P_COMP", # percentil de llegafa COMP
    "P_TREP", # percentil de llegafa TREP
]


TRAD_2019_PER_COMP = {
    'Código Mesa':'ID_MESA',
    # 'p1',
    # 'p2',
    'pm':'P_COMP',
    # pj'
}
TRAD_2019_PER_TREP = {
    'Código Mesa':'ID_MESA',
    # 'p1',
    # 'p2',
    'pm':'P_TREP',
    'pj':'PJ_TREP'
}
TRAD_2019_ESTAD_NAC = {
    # 'RECI' : ,
    # 'idloc' : ,
    'id_rec': 'ID_RECI',
    # 'dep' : ,
    # 'nomdep' : ,
    # 'PROV' : ,
    # 'nomprov' : ,
    # 'sec' : ,
    # 'nombremunicipio' : ,
    # 'AsientoElectoral' : ,
    # 'dist' : ,
    # 'nomdist' : ,
    # 'zona' : ,
    # 'nomzona' : ,
    # 'CIRCUNDIST' : ,
    # 'nombrerecinto' : ,
    'Habilitados': 'HAB',
    # 'Inhabilitados' : ,
    # 'Depurados' : ,
    # 'NombreReci' : ,
    # 'NombreMuni' : ,
    # 'AsientoEle' : ,
    'latitud': 'LAT',
    'longitud': 'LON',
    'density': 'DEN',
    'CANTIDAD DE MESAS': 'N_MESAS',
    'NombreReci': 'REC',
    'NombreMuni': 'MUN',
    # 'x': 'X',
    # 'y': 'Y',
}

TRAD_2019_ESTAD_EXT = {
    'País': 'PAIS',
    # 'RECI' : ,
    # 'idloc' : ,
    'id_rec': 'ID_RECI',
    # 'dep' : ,
    # 'nomdep' : ,
    # 'PROV' : ,
    # 'nomprov' : ,
    # 'sec' : ,
    # 'nombremunicipio' : ,
    # 'AsientoElectoral' : ,
    # 'dist' : ,
    # 'nomdist' : ,
    # 'zona' : ,
    # 'nomzona' : ,
    # 'CIRCUNDIST' : ,
    # 'nombrerecinto' : ,
    'Habilitados': 'HAB',
    # 'Inhabilitados' : ,
    # 'Depurados' : ,
    # 'NombreReci' : ,
    # 'NombreMuni' : ,
    # 'AsientoEle' : ,
    'latitud': 'LAT',
    'longitud': 'LON',
    'density': 'DEN',
    'CANTIDAD DE MESAS': 'N_MESAS',
    'nombrerecinto': 'REC',
    'nombremunicipio': 'MUN',
    # 'x': 'X',
    # 'y': 'Y',
}

TRAD_2019_COMP = {
    'id_rec': 'ID_RECI',
    # 'País',
    # 'Número departamento',
    # 'Departamento',
    # 'Provincia',
    # 'Número municipio',
    # 'Municipio',
    # 'Circunscripción',
    # 'Localidad',
    # 'Recinto',
    # 'Número Mesa',
    'Código Mesa': 'ID_MESA',
    # 'Elección',
    'Inscritos': 'HAB',
    'CC': 'CC',
    # 'FPV',
    # 'MTS',
    # 'UCS',
    'MAS - IPSP': 'MAS',
    '21F':'21F',
    'PDC': 'PDC',
    # 'MNR',
    # 'PAN-BOL',
    'Votos Válidos': 'VV',
    'Blancos':'BL',
    'Nulos':'NU'
    # 'id_rec',
    # 'check_validos',
    # 'total_votes',
    # 'valid',
    # 'dif_mas_cc',
    # 'dmcp',
    # 'per_votos'
}

TOOL_TIPS = [
    ('hab', '@HAB'),
    ('mas', '@mas'),
]

TOOL_TIPS1 = [
    ('INS', '@HAB'),
    ('PAIS', '@PAIS'),
    ('MUN', '@MUN'),
    ('REC', '@REC'),
    ('MAS - CC %' , '@d_mas_cc')
    # ('PAIS', '@PAIS'),
]

import bokeh.palettes

P_MAS = bokeh.palettes.PuBu9[::-1]
# P_DIF = bokeh.palettes.RdYlBu11
P_DIF = [*bokeh.palettes.Oranges7[1:],
         *bokeh.palettes.Blues6[::-1]]
P_DIF_MAS_CREEMOS = [*bokeh.palettes.Reds8[1:],
                     *bokeh.palettes.Blues6[::-1]]
P_GRAD_CC = [*bokeh.palettes.Oranges7[::-1]]
P_GRAD_FPV = [*bokeh.palettes.YlGn7[::-1]]
P_GRAD_MAS = [*bokeh.palettes.Blues7[::-1]]
P_GRAD_CREEMOS = [*bokeh.palettes.Reds8[::-1]]
P_GRAD_PANBOL = [*bokeh.palettes.YlOrRd8[::-1]]

C_DIC = {
    'CC':P_GRAD_CC[-2],
    'FPV':P_GRAD_FPV[-2],
    'MAS':P_GRAD_MAS[-1],
    'CREEMOS':P_GRAD_CREEMOS[-1],
    'PAN_BOL':P_GRAD_PANBOL[-1],
}

P_DIC = {
    'CC':P_GRAD_CC,
    'FPV':P_GRAD_FPV,
    'MAS':P_GRAD_MAS,
    'CREEMOS':P_GRAD_CREEMOS,
    'PAN_BOL':P_GRAD_PANBOL,
}

# %%
# FUNCTIONS

def xround(data, r):
    return np.round(data / r) * r


def get_rec_hist(data, _r, x, y, lamMlomM=None):
    _gr = data[[HAB, x, y]]

    # %%
    if lamMlomM is None:
        lam = np.round(_gr[y].min() / _r) * _r - _r
        laM = np.round(_gr[y].max() / _r) * _r + _r
        lom = np.round(_gr[x].min() / _r) * _r - _r
        loM = np.round(_gr[x].max() / _r) * _r + _r

    else:
        lam, laM, lom, loM = lamMlomM

    # %%
    lo_range = np.arange(lom, loM + _r / 2, _r)
    la_range = np.arange(lam, laM + _r / 2, _r)
    dat, _x, _y = np.histogram2d(
        x=_gr[x], y=_gr[y],
        weights=_gr[HAB],
        bins=[
            lo_range,
            la_range
        ]
    )
    _x = _x[:-1] + _r / 2
    _y = _y[:-1] + _r / 2
    # %%
    ds = xr.DataArray(dat, dims=[x, y], coords=[_x, _y])
    return ds, lo_range, la_range


def run_cart(_ds, x, y, x_out, y_out):
    dat_in = os.path.join(CART_PATH, 'in.dat')
    dat_out = os.path.join(CART_PATH, 'out.dat')
    if os.path.isfile(dat_out):
        os.remove(dat_out)
    if os.path.isfile(dat_in):
        os.remove(dat_in)
    __ds = _ds.transpose(y, x)
    __ds.to_pandas().to_csv(dat_in, sep=' ', header=False, index=False)
    # %%
    _y, _x = __ds.shape
    # %%
    import subprocess
    cart_cmd = [CART_CMD,f'{_x}',f'{_y}',dat_in,dat_out]
    list_files = subprocess.run(cart_cmd,
        stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE

    )
    # print(cart_cmd)
    print(list_files.stderr)
    # %%
    npd = pd.read_csv(dat_out, names=[x_out, y_out], sep=' ')
    return npd


def get_transform(ds_g, npd, x, y, lo_range, la_range, x_out, y_out):
    _y, _x = ds_g.transpose(y, x).shape

    _dy = npd[y_out].values.reshape(_y + 1, _x + 1)
    # return _d
    y_da = xr.DataArray(
        _dy, dims=[y, x], coords=[la_range, lo_range], name=y_out)

    _dx = npd[x_out].values.reshape(_y + 1, _x + 1)
    x_da = xr.DataArray(
        _dx, dims=[y, x], coords=[la_range, lo_range], name=x_out)

    ds_transform = xr.merge([x_da, y_da])
    return ds_transform


def get_carto_df(N, _r, data0, sigma_gauss, x0, x1, x_range, y0, y1, y_range, fun,
                 rad=10):
    x_center, y_center = get_xy_center(data0, N, x0, y0)
    ds, xx_range, yy_range = get_rec_hist(
        data0, _r,
        lamMlomM=[y_center - y_range, y_center + y_range,
                  x_center - x_range, x_center + x_range],
        x=x0, y=y0
    )
    ds.plot(
        x=x0, y=y0,
        norm=matplotlib.colors.LogNorm(vmin=1, vmax=800000),
    )
    plt.show()
    # ds = ds.loc[{y0:slice(-25,-9),'lon':slice(-73,-55)}]
    # %%
    # GAUSSIAN
    ds_g = ds.copy()
    ds_g.values = gaussian_filter(ds_g.values, sigma=sigma_gauss, truncate=8)
    # import matplotlib.colors
    ds_g.plot(
        x=x0, y=y0,
        # norm = matplotlib.colors.LogNorm(vmin=1,vmax=ds_g.max())
    )
    plt.show()
    # %%
    # CARTO
    npd = run_cart(fun(ds_g), x=x0, y=y0, x_out=x1, y_out=y1)
    # %%
    # TRANS
    ds_transform = get_transform(ds_g, npd, x=x0, y=y0,
                                 lo_range=xx_range, la_range=yy_range,
                                 x_out=x1, y_out=y1)
    # INT
    _la = xr.DataArray(data0[y0], dims='index')
    _lo = xr.DataArray(data0[x0], dims='index')
    int = ds_transform.interp({y0: _la, x0: _lo})
    _int = int.to_dataframe()
    ndf = pd.merge(data0, _int[[x1, y1]], left_index=True, right_index=True)
    plt.scatter(x=ndf[x1], y=ndf[y1], s=np.sqrt(ndf[N]), alpha=.1)
    plt.show()
    # %%
    f = bokeh.plotting.figure()
    _df = ndf.copy()
    _df['s'] = np.sqrt(ndf[N]) / rad
    sc = bokeh.models.ColumnDataSource(_df)
    ho = bokeh.models.HoverTool(
        tooltips=[
            ('n', '@HAB'),
            ('rec', '@REC'),
            ('mun', '@MUN')
        ]
    )
    f.scatter(x=x1, y=y1, source=sc, size='s')
    f.add_tools(ho)
    bokeh.plotting.show(f, browser='safari')
    return ndf


def get_xy_center(data, N, x0, y0):
    x_center = (data[x0] * data[N]).sum() / data[N].sum()
    y_center = (data[y0] * data[N]).sum() / data[N].sum()
    return x_center, y_center


def traductor_df(path, _dic):
    # columnas que cada file debería tener para entrar al predictor

    df = pd.read_csv(path)
    df = df[_dic.keys()]
    df: pd.DataFrame
    df = df.rename(_dic, axis=1)
    return df


def rescale_xy(ndf2, x0='x0', y0='y0', x3='x3', y3='y3', X='X', Y='Y',
               fx = 1.5,
               fy = 1.5
               ):
    x_med = (ndf2[x0] * ndf2['HAB']).sum() / ndf2['HAB'].sum()
    x_std = ndf2[x0].std()
    y_med = (ndf2[y0] * ndf2['HAB']).sum() / ndf2['HAB'].sum()
    y_std = ndf2[y0].std()
    # x3 = 'x3'
    X_med = (ndf2[x3] * ndf2['HAB']).sum() / ndf2['HAB'].sum()
    X_std = ndf2[x3].std()
    Y_med = (ndf2[y3] * ndf2['HAB']).sum() / ndf2['HAB'].sum()
    Y_std = ndf2[y3].std()
    # %%
    ndf2[X] = (((ndf2[x3] - X_med) / X_std) * fx * x_std) + x_med
    ndf2[Y] = (((ndf2[y3] - Y_med) / Y_std) * fy * y_std) + y_med
    return ndf2


def predictor(
        train_df: pd.DataFrame,
        predict_df: pd.DataFrame,
        x, y, hab, v):
    """
    """
    t_df = train_df[[x, y, hab, v]].copy()
    p_df = predict_df[[x, y, hab]].copy()
    ts_df = t_df.groupby([x, y]).sum()
    v_hab = v + '_' + hab
    ts_df[v_hab] = (ts_df[v] / ts_df[hab])
    ts_df = ts_df.reset_index()
    from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
    v_p = v + '_p'
    lint = LinearNDInterpolator(ts_df[[x, y]], ts_df[v_hab])
    nint = NearestNDInterpolator(ts_df[[x, y]], ts_df[v_hab])
    p_df[v_hab+'l'] = lint(p_df[[x, y]])
    p_df[v_hab+'n'] = nint(p_df[[x, y]])
    p_df[v_hab] = p_df[v_hab+'l'].fillna(p_df[v_hab+'n'])
    v_p = v + '_' + 'p'
    p_df[v_p] = p_df[v_hab] * p_df[hab]
    # todo check what to do with the nans+
    n_nans = p_df[v_p].isnull().value_counts()
    # print(f'n nans: {n_nans}')
    return p_df[v_p]


def calculate_density():
    # todo
    pass

def open_combine_2020()-> pd.DataFrame:
    '''
    Combina estadistica nacional y exterior.
    :return: dataframe
    '''

def open_combine_2019() -> pd.DataFrame:
    '''
    combina estadística nacional y exterior con resultados finales y
    cartograma
    Returns
    -------
    dataframe

    '''
    df = traductor_df(
        CSV_RES_2019_COMP, TRAD_2019_COMP
    ).set_index('ID_RECI')
    # df
    car = pd.read_csv(CSV_CART_2019).set_index('ID_RECI')
    # car
    df[['X', 'Y']] = car[['X', 'Y']]
    assert len(df[df['X'].isnull()]) == 0
    assert len(df[df['Y'].isnull()]) == 0

    est_df = open_concat_est_2019()

    cols = ['PAIS', 'LAT', 'LON', 'DEN', 'REC', 'MUN', 'BOL']

    df[cols] = est_df[cols]

    df = df.reset_index().set_index('ID_MESA')
    return df

def partition_df(df, p, random_state=None):
    '''

    :param df:
    :param p: percentage e.g. .2 -> .2 train , .8 test
    :param random_state:
    :return:
    '''
    _index = df.index.name
    _df = df.reset_index()
    if random_state:
        rs = {'random_state': random_state}
    else:
        rs = {}
    tot = len(_df)
    n = int(p * tot)

    train = _df.sample(n=n, **rs).copy()
    _df['train'] = False
    _df.loc[train.index, 'train'] = True
    test = _df[~_df['train']].copy()
    test = test.set_index(_index)
    train = train.set_index(_index)
    # print(len(_df))
    assert len(test) + len(train) == len(_df)
    return test, train


def sanity_check(df, cols, col):
    '''checks if the math of the tble is ok'''
    # todo finish this one
    pass


def open_concat_est_2019():
    path = CSV_EST_EXT_2019
    data = traductor_df(path, TRAD_2019_ESTAD_EXT).set_index('ID_RECI')
    data['BOL'] = False
    path = CSV_EST_NAC_2019
    dataBol = traductor_df(path, TRAD_2019_ESTAD_NAC).set_index('ID_RECI')
    dataBol['BOL'] = True
    dataBol['PAIS'] = 'Bolivia'
    # gr = dataBol.reset_index().groupby('BOL')
    # d = gr.first()
    # d['HAB'] = gr[['HAB']].sum()
    # d = d.reset_index().set_index('ID_RECI')
    #
    #
    # data = pd.concat([data,d])
    data = pd.concat([data, dataBol])
    return data


dic_standard_ejemplo = dict(
    traductor_cos={},
    path={},
    funciones_proc={},

)


def lola_to_cart(lo, la):
    """
    transform lo,la to x,y
    Parameters
    ----------
    df

    Returns
    -------

    """
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857",
                                       always_xy=True)
    res = transformer.transform(
        lo, la
    )
    return res


def get_la_lo_bolivia():
    '''
    retorna la lat y lon para bolivia
    Returns
    -------

    '''
    import cartopy.io.shapereader as shpreader
    import geopandas
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')


    # %%
    gp = geopandas.read_file(shpfilename)
    pol_bo = gp[gp['NAME']=='Bolivia']['geometry'].iloc[0]

    # %%
    lo,la = pol_bo.boundary.xy
    lo = lo.tolist()
    la = la.tolist()
    return la, lo


def get_dens_from_hab(f: pd.DataFrame):

    lam = f['LAT'].min()
    laM = f['LAT'].max()
    lom = f['LON'].min()
    loM = f['LON'].max()

    R = .05
    lam = np.floor(lam/R)* R - R
    laM = np.ceil(laM/R)* R + R

    lom = np.floor(lom/R)* R - R
    loM = np.ceil(loM/R)* R + R

    # %%
    lo_range = np.arange(lom,loM+R/2,R)
    la_range = np.arange(lam,laM+R/2,R)
    lo_lab = lo_range[:-1] + R/2
    la_lab = la_range[:-1] + R/2

    # %%

    # %%
    d,_,_ = np.histogram2d(f['LON'],f['LAT'],bins=(lo_range,la_range),weights=f['HAB'])

    from scipy.ndimage import gaussian_filter as gf
    d1 = gf(d,sigma=.5)

    # %%
    ar = xr.DataArray(d1.T,dims= ['LAT','LON'] , coords={'LAT':la_lab,'LON':lo_lab})

    # %%
    de = ar/(R*R * 100 * 100)


    # %%
    LA = xr.DataArray(f['LAT'], dims=f.index.name)
    LO = xr.DataArray(f['LON'], dims=f.index.name)

    # %%
    de.name = 'DEN'
    res = de.interp({'LAT':LA,'LON':LO}).to_dataframe()
    f_out = f.copy()
    f_out['DEN'] = res['DEN']
    return f_out



###########################

def get_dataframe_2020(path='comp/exportacion_EG2020_actual.csv'):
    p = os.path.join(DATA_PATH1_2020, path)
    df_comp = pd.read_csv(p).set_index('ID_MESA')
    b_ = df_comp["CANDIDATURA"] == "PRESIDENTE"
    df_comp = df_comp[b_]
    co = ['VV', 'BL', 'NU', 'VOTO_EMITIDO','CREEMOS', 'MAS', 'FPV',
          'PAN_BOL', 'CC','NUA','HAB']
    df_comp = df_comp[co]

    df_comp['ID_RECI'] = (df_comp.index/100).astype(np.int64)
    df_comp['COUNT'] = True


    p = os.path.join(eb.util.DATA_PATH1_2020,'z010R_geopadron_mesas_2020_ALL.csv')
    df_all = pd.read_csv(p).set_index('ID_MESA')
    #['ID_RECI', 'ID_MESA', 'HAB', 'INHAB']

    df_all['VV'] = 0
    df_all['COUNT'] = False

    p = os.path.join(eb.util.DATA_PATH1_2020,'z020_geopadron_recintos_2020_ALL_DEN.csv')
    df_den = pd.read_csv(p).set_index('ID_RECI')
    #['ID_RECI', 'LAT', 'LON', 'HAB', 'INHAB', 'PAIS', 'N_MESAS', 'REC',
    # 'MUN', 'BOL', 'CIU', 'PROV', 'DEP', 'URB', 'DEN_C', 'DEN']

    df_den = df_den[['LAT', 'LON', 'PAIS', 'N_MESAS', 'REC',
                     'MUN', 'BOL', 'CIU', 'PROV', 'DEP', 'URB', 'DEN_C', 'DEN']]

    _s  = df_comp.index.isin(df_all.index)
    assert (~_s).sum() == 0

    b = ~df_all.index.isin(df_comp.index)
    df_trim = df_all[b]
    assert len(df_all) - len(df_comp) == len(df_trim)
    df_concat = pd.concat([df_comp,df_trim])
    df_full = df_concat.join(df_den,how='left',on='ID_RECI')
    p = os.path.join(eb.util.DATA_PATH1_2020,'z030_carto_xy.csv')
    df_xy = pd.read_csv(p).set_index('ID_RECI')
    df2 = df_full.join(df_xy,on='ID_RECI',how='left')
    res = pd.cut(df2['DEN'],eb.util.DEN_LIMS,labels=eb.util.DEN_CODES)
    df2['DEN_CODES'] = res.astype(int)
    return df2


def get_bolivian_time(diff_utc):
    """
    :param:
        diff_utc -- input localtime difference in hours from UTC: e.g. if Argentina (UTC-3): diff_utc:-3
    : return:
         dictionary: str_val, datetime_val
    """
    diff = -4
    current_time_UTC = datetime.datetime.utcnow()
    horas_added = datetime.timedelta(hours=diff)
    current_time_BOT = current_time_UTC + horas_added
    timeBOT = current_time_BOT.strftime("%Y%m%d%H%M%S")
    bolivian_time = {
        "str_val":timeBOT,
        "datetime_val": current_time_BOT
    }
    return bolivian_time

