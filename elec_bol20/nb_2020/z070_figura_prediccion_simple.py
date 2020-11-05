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
from elec_bol20.util import single_pred, monte_carlo_predictions

df = ebu.get_dataframe_2020()
df['D_MAS_CC'] = df['MAS'] - df['CC']
# df_full = df[df['VV'] > 0]

# %%


# %%
['ID_RECI', 'HAB', 'CC', 'MAS', '21F', 'PDC', 'VV', 'BL', 'NL', 'X', 'Y',
 'PAIS', 'LAT', 'LON', 'DEN', 'REC', 'MUN', 'BOL', 'P_COMP']
df.columns


# %%


# %%


# %%
vs = ['MAS', 'CC', 'CREEMOS', 'FPV']
rd = {}
for v in vs:
    _pred = single_pred(df=df, var=v)

    # %%
    calc_dmascc = _pred['pred']
    # actual_dmascc = _pred['actual']

    # %%
    r = df[df['COUNT']]['HAB'].sum() / df['HAB'].sum()
    # %%
    _st1 = monte_carlo_predictions(df=df, n=20, var=v)
    _td = np.std(_st1, ddof=1)
    rd[v] = {'res': calc_dmascc, 'stl': _st1, 'std': _td}

# %%
# todo finish this
pd_df = pd.DataFrame(rd)
p_df = pd_df.drop('stl').T
p_df['3std'] = p_df['std'] * 3 * 2
p_df[['res', '3std']]
# %%
ls = ['PAIS', 'DEP', 'PROV', 'MUN']
gr = df.groupby(ls)
# %%
res = []
for l, d in gr:
    pd

# %%
