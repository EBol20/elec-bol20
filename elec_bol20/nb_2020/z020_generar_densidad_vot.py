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
from elec_bol20 import *
import elec_bol20.util as ebu

# %% [markdown]
# ## open file

# %%
path = ebu.DATA_PATH1
path = os.path.join(path,'2020','z010r_geopadron_recintos_2020_ALL.csv')
df = pd.read_csv(path,encoding='ISO-8859-1').set_index('ID_RECI')

# %%
gr = df.groupby('PAIS')

# %%
gr.groups.keys()

# %%
fs = []
for i in gr.groups.keys():
    f = gr.get_group(i)

    f_out = ebu.get_dens_from_hab(f)
    fs.append(f_out)



# %%
res=pd.concat(fs)

# %%
res.to_csv(os.path.join(ebu.DATA_PATH1,'2020','z020_geopadron_recintos_2020_ALL_DEN.csv'))

# %%
