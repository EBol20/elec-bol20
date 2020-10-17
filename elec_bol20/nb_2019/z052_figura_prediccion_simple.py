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
df['D_MAS_CC'] = df['MAS'] - df['CC']
df_full = df[df['VV'] > 0]
# %%
path = os.path.join(ebu.DATA_PATH0, '2019', 'percentil_trep.csv')
df_comp = ebu.traductor_df(path, ebu.TRAD_2019_PER_TREP).set_index('ID_MESA')
df_comp = df_comp[~df_comp.index.duplicated()]
# %%
df = pd.merge(df_full, df_comp, right_index=True, left_index=True, how='inner')


# %%
['ID_RECI', 'HAB', 'CC', 'MAS', '21F', 'PDC', 'VV', 'BL', 'NL', 'X', 'Y',
 'PAIS', 'LAT', 'LON', 'DEN', 'REC', 'MUN', 'BOL', 'P_COMP']
df.columns


# %%
R = 80


# %%
def single_pred(*, R, df):
    df_12 = df.copy()
    df_1 = df_12[df_12['PJ_TREP'] <= R]
    df_2 = df_12[df_12['PJ_TREP'] > R]

    # %%

    # MAS_p  = ebu.predictor(df_1,df_2,'X','Y','HAB','MAS')
    D_MAS_CC = ebu.predictor(df_1, df_2, 'X', 'Y', 'HAB', 'D_MAS_CC')
    VV_p = ebu.predictor(df_1, df_2, 'X', 'Y', 'HAB', 'VV')
    actual_dmascc = df_12['D_MAS_CC'].sum() / df_12['VV'].sum() * 100

    a = df_1['D_MAS_CC'].sum()
    b = D_MAS_CC.sum()
    c = df_1['VV'].sum()
    d = VV_p.sum()
    calc_dmascc = (a + b) / (c + d) * 100
    return {'pred':calc_dmascc,'actual':actual_dmascc}

def rand_diff(*,df,rr):
    test,train = ebu.partition_df(df,rr)
    MAS_p  = ebu.predictor(train,test,'X','Y','HAB','MAS')
    D_MAS_CC = ebu.predictor(train,test,'X','Y','HAB','D_MAS_CC')
    VV_p = ebu.predictor(train,test,'X','Y','HAB','VV')
    actual_dmascc = df['D_MAS_CC'].sum()/df['VV'].sum()*100

    a = train['D_MAS_CC'].sum()
    b = D_MAS_CC.sum()
    c = train['VV'].sum()
    d = VV_p.sum()
    calc_dmascc = (a + b)/(c + d) * 100
    return actual_dmascc - calc_dmascc


def mc_pred(*,R,r,df,n=2):
    df_R = df[df['PJ_TREP'] <= R].copy()
    
    dif = []
    for i in range(n):
        d = rand_diff(df=df_R,rr=r/100)
    
        dif.append(d)
    return np.std(dif,ddof=1)



# %%
_pred = single_pred(R=R,df=df)
calc_dmascc = _pred['pred']
actual_dmascc = _pred['actual']
_st = mc_pred(R=R,r=R,df=df,n=20)

# %%
_st

# %%
calc_dmascc

# %%
f = bokeh.plotting.Figure()

# %%
df_1 = df_12[df_12['PJ_TREP'] <= R]
dd = df_1[['D_MAS_CC', 'PJ_TREP', 'VV']].set_index('PJ_TREP').sort_index()

# %%
ds = dd.cumsum()
ds['d_mas_cc'] = ds['D_MAS_CC'] / ds['VV'] * 100

# %% [markdown]
#

# %%
src = bokeh.models.ColumnDataSource(ds[['d_mas_cc']])

# %%

f = bokeh.plotting.Figure(height=400, width=600)
f.line(x='PJ_TREP', y='d_mas_cc', source=src, line_width=3)
f.line(x=[R, 100], y=[ds['d_mas_cc'].iloc[-1], calc_dmascc], color='red', line_width=1)
f.varea(x=[R,100],
        y1=[ds['d_mas_cc'].iloc[-1], calc_dmascc + _st * 3],
        y2=[ds['d_mas_cc'].iloc[-1], calc_dmascc - _st * 3],
        color='red',
        alpha=.5,
#         line_width=1
       )
f.toolbar_location = None
f.y_range.start = -14
f.y_range.end = 14
f.x_range.start = 0
f.x_range.end = 101
bokeh.plotting.output_notebook()
bokeh.plotting.show(f)

# %%
ds.iloc[-1]

# %%
