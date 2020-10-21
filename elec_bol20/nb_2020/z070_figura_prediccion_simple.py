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

df = ebu.get_dataframe_2020()
df['D_MAS_CC'] = df['MAS'] - df['CC']
# df_full = df[df['VV'] > 0]

# %%



# %%
['ID_RECI', 'HAB', 'CC', 'MAS', '21F', 'PDC', 'VV', 'BL', 'NL', 'X', 'Y',
 'PAIS', 'LAT', 'LON', 'DEN', 'REC', 'MUN', 'BOL', 'P_COMP']
df.columns



# %%
def single_pred(*, df, var):
    VAR, VV_p, df_1 = var_predictor(df, var)
    # actual_dmascc = df_12[VAR].sum() / df_12['VV'].sum() * 100

    a = df_1[var].sum()
    b = VAR.sum()
    c = df_1['VV'].sum()
    d = VV_p.sum()
    cal_var = (a + b) / (c + d) * 100
    dic_ret = {
        'pred': cal_var,
        # 'actual': actual_dmascc
    }
    return dic_ret


def var_predictor(df, var):
    df_12 = df.copy()
    df_1 = df_12[df_12['COUNT']]
    df_2 = df_12[~df_12['COUNT']]
    # MAS_p  = ebu.predictor(df_1,df_2,'X','Y','HAB','MAS')
    VAR = ebu.predictor(df_1, df_2, 'X', 'Y', 'HAB', var)
    VV_p = ebu.predictor(df_1, df_2, 'X', 'Y', 'HAB', 'VV')
    return VAR, VV_p, df_1


#%%
def rand_diff(*, df, rr, var):
    test, train = ebu.partition_df(df, rr)
    VAR = ebu.predictor(train, test, 'X', 'Y', 'HAB', var)
    VV_p = ebu.predictor(train, test, 'X', 'Y', 'HAB', 'VV')
    actual_dmascc = df[var].sum() / df['VV'].sum() * 100

    a = train[var].sum()
    b = VAR.sum()
    c = train['VV'].sum()
    d = VV_p.sum()
    calc_dmascc = (a + b) / (c + d) * 100
    return actual_dmascc - calc_dmascc


def mc_pred(*, df, var,n=2):
    df_R = df[df['COUNT']].copy()
    r = df[df['COUNT']]['HAB'].sum()/df['HAB'].sum()

    dif = []
    for i in range(n):
        d = rand_diff(df=df_R, rr=r ,var=var)

        dif.append(d)
    return dif


# %%
vs = ['MAS','CC','CREEMOS','FPV']
rd = {}
for v in vs:
    _pred = single_pred(df=df,var= v)

    #%%
    calc_dmascc = _pred['pred']
    # actual_dmascc = _pred['actual']

    #%%
    r = df[df['COUNT']]['HAB'].sum()/df['HAB'].sum()
    #%%
    _st1 = mc_pred(df=df, n=20,var=v)
    _td = np.std(_st1,ddof=1)
    rd[v] = {'res':calc_dmascc,'stl':_st1,'std':_td}


# %%
#todo finish this
pd_df = pd.DataFrame(rd)
p_df=pd_df.drop('stl').T
p_df['3std'] = p_df['std']*3*2
p_df[['res','3std']]
# %%
ls = ['PAIS','DEP','PROV','MUN']
gr = df.groupby(ls)
#%%
res = []
for l,d in gr:
    pd

#%%