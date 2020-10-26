# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
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

# %%

import elec_bol20.util as ebu
from elec_bol20 import *

# CONS
CLUS_DIC = {0: '++MAS', 1: '+MAS', 2: '+CRE', 3: '++CRE', 4: '+CC'}
DCHI = 'CHI20 - CHI19'
DMAS = 'MAS20 - MAS19'
DCRE = 'CRE20 - CRE19'
D21F = '21F20 - 21F19'
DCC = 'CC20 - CC19'
DNB = 'NB20 - NB19'
DOTROS = 'OTROS20 - OTROS19'

COLUMNS_CLUS = [DMAS, DCC, DCRE, D21F, DCHI, DNB, DOTROS]
def _fff(): pass
DMAS_M_DCHI = f'({DMAS}) + ({DCHI})'
DMAS_M_DCC = f'({DMAS}) + ({DCC})'
DMAS_M_D21F = f'({DMAS}) + ({D21F})'

PAL = bokeh.palettes.PuOr7
PAL1 = bokeh.palettes.PuOr7
PAL2 = bokeh.palettes.PuOr7
VAR = DCHI
VAR1 = DMAS
VAR2 = DMAS_M_DCHI
CMIN = -20
CMAX = 20
CMIN1 = -20
CMAX1 = 20
CMIN2 = -20
CMAX2 = 20
COLS_PLOT = [
    # 'mas_20','mas_19',
    'xj', 'yj', 's',
    DMAS, DCHI,
    DMAS_M_DCHI
]

COLORS = bokeh.palettes.Colorblind[len(CLUS_DIC)][:]

HW = 400

CLUS = 'Cluster'


# FUNCS

def get_df_simple():
    df20 = ebu.get_dataframe_2020()

    df19 = ebu.open_combine_2019()

    df = pd.merge(
        df19, df20, left_index=True, right_index=True,
        suffixes=['_19', '_20'],
        how='inner'
    )
    return df


def get_df():
    # global df
    VV_20 = 'VV_20'
    VV_19 = 'VV_19'
    df = get_df_simple()
    # clean 0 vote tables from last election
    df = df[df[VV_19] > 0]
    df = df[df[VV_20] > 0]

    _b1 = np.abs(df['LAT_20'] - df['LAT_19']) < .1
    df = df[_b1]

    _b1 = np.abs(df['LON_20'] - df['LON_19']) < .1
    df = df[_b1]

    VT_20 = 'VT_20'
    VT_19 = 'VT_19'

    df['NB_20'] = (df['NUA'] + df['NU_20'] + df['BL_20'])
    df['NB_19'] = (df['NU_19'] + df['BL_19'])

    df[VT_20] = df['NU_20'] + df['NUA'] + df['BL_20'] + df[VV_20]
    df['OTROS_20'] = df[VT_20] - df['MAS_20'] \
                     - df['FPV'] - df['CC_20'] - df['CREEMOS'] - df['NB_20']

    df[VT_19] = df['NU_19'] + df['BL_19'] + df[VV_19]
    df['OTROS_19'] = df[VT_19] - df['MAS_19'] - df['PDC'] - df['CC_19'] \
                     - df['21F'] - df['NB_19']

    df['mas_20'] = df['MAS_20'] / df[VT_20] * 100
    df['mas_19'] = df['MAS_19'] / df[VT_19] * 100
    df[DMAS] = df['mas_20'] - df['mas_19']

    df['chi_20'] = df['FPV'] / df[VT_20] * 100
    df['chi_19'] = df['PDC'] / df[VT_19] * 100
    df[DCHI] = df['chi_20'] - df['chi_19']

    df['cc_20'] = df['CC_20'] / df[VT_20] * 100
    df['cc_19'] = df['CC_19'] / df[VT_19] * 100
    df[DCC] = df['cc_20'] - df['cc_19']

    df['creemos_20'] = df['CREEMOS'] / df[VT_20] * 100
    df['creemos_19'] = 0
    df[DCRE] = df['creemos_20'] - df['creemos_19']

    df['21f_20'] = 0
    df['21f_19'] = df['21F'] / df[VT_19] * 100
    df[D21F] = df['21f_20'] - df['21f_19']

    df['nb_20'] = df['NB_20'] / df[VT_20] * 100
    df['nb_19'] = df['NB_19'] / df[VT_19] * 100
    df[DNB] = df['nb_20'] - df['nb_19']

    df['dotros_20'] = df['OTROS_20'] / df[VT_20] * 100
    df['dotros_19'] = df['OTROS_19'] / df[VT_19] * 100
    df[DOTROS] = df['dotros_20'] - df['dotros_19']

    LEN = len(df)
    # add jitter to the tables
    df['xj'] = df['X_20'] + (np.random.randn(LEN) - .5) * .002 * np.sqrt(
        df['DEN_20'])
    df['yj'] = df['Y_20'] + (np.random.randn(LEN) - .5) * .002 * np.sqrt(
        df['DEN_20'])
    df[DMAS_M_DCHI] = df[DMAS] + df[DCHI]
    df[DMAS_M_DCC] = df[DMAS] + df[DCC]
    df[DMAS_M_D21F] = df[DMAS] + df[D21F]
    df['s'] = np.sqrt(df['HAB_20'] / 45000)
    df = df.sort_values('DEN_20')
    return df


def plot_scatter(*, sr, HW, VAR, CMIN, CMAX, PAL):
    # global f, cb, f
    f = bokeh.plotting.Figure(width=HW, height=HW, output_backend="webgl")
    cm = bokeh.transform.linear_cmap(VAR, palette=PAL, low=CMIN, high=CMAX)
    cb = bokeh.models.ColorBar(
        color_mapper=cm['transform'], width='auto',
        location=(0, 1),
        title="",
        # margin=0,padding=0,
        title_standoff=10
    )
    f.scatter(x='xj',
              y='yj',
              source=sr,
              color=cm,
              radius='s',
              # size = 1,
              alpha=.5
              )
    f.add_layout(cb, 'center')
    f.title.text = VAR
    return f


def plot_clusters_carto(*, df1):
    f = bokeh.plotting.figure()

    f.background_fill_color = "gainsboro"
    for i, l in enumerate(CLUS_DIC.values()):
        sr = bokeh.models.ColumnDataSource(df1[df1[CLUS] == l])
        f.scatter('xj', 'yj', source=sr, color=COLORS[i],
                  legend_label=l + ' (haz clic)', radius=.02)

    f.legend.click_policy = "hide"

    TOOL_TIP = [
        (CLUS, f'@{CLUS}'),
        *[(v + '[%]', f'@{{{v}}}{{0}}') for v in COLUMNS_CLUS],
        ('----', '----')
    ]

    ho = bokeh.models.HoverTool(
        tooltips=TOOL_TIP
    )

    f.add_tools(ho)

    bokeh.plotting.show(f)
    return f


def plot_3_comparison(*, df):
    sr = bokeh.plotting.ColumnDataSource(df[COLS_PLOT])
    f0 = plot_scatter(
        sr=sr, HW=HW, VAR=VAR, CMIN=CMIN, CMAX=CMAX, PAL=PAL)
    f1 = plot_scatter(
        sr=sr, HW=HW, VAR=VAR1, CMIN=CMIN1, CMAX=CMAX1, PAL=PAL1)
    f2 = plot_scatter(
        sr=sr, HW=HW, VAR=VAR2, CMIN=CMIN2, CMAX=CMAX2, PAL=PAL2)

    # lay = bokeh.layouts.row([f0, f1])
    lay = bokeh.layouts.gridplot([[f0, f1], [f2, None]])

    bokeh.plotting.output_notebook()
    bokeh.plotting.show(lay)


def cluster_analysis(*, df, n=5, seed=123,cl = CLUS_DIC):
    from sklearn.cluster import KMeans
    cols = COLUMNS_CLUS

    df1 = df[[*cols, 'xj', 'yj', 'VV_20']].dropna(how='any', axis=0)
    N = n
    kmeans = KMeans(n_clusters=N, random_state=seed,
                    n_init=20
                    ).fit(df1[cols])

    # %%
    cen = pd.DataFrame(kmeans.cluster_centers_, columns=cols
                       ).sort_values(DMAS,
                                     ascending=False)
    kmeans = KMeans(n_clusters=N, random_state=seed, init=cen).fit(df1[cols])
    cen = pd.DataFrame(kmeans.cluster_centers_, columns=cols
                       ).sort_values(DMAS,
                                     ascending=False)

    # %%


    # %%

    # %%
    df1[CLUS] = [cl[i] for i in kmeans.labels_]
    return df1
