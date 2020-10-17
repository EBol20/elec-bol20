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
i = 'reci_interior'
e = 'reci_exterior'
path = os.path.join(ebu.DATA_PATH0,'2020','2020_geo_padron_final/2020_geo_padron_final.xlsx')
di = pd.read_excel(path,sheet_name=i)
de = pd.read_excel(path,sheet_name=e)

# %% [markdown] heading_collapsed=true
# ##### ver 

# %% hidden=true
['RECI_GEO_FID', 'NumPaís', 'País', 'NumDep', 'Departamento', 'NumProv',
       'Provincia', 'NumMuni', 'Municipio', 'idloc', 'AsientoElectoral',
       'NumDist', 'Distrito', 'NumZona', 'Zona', 'CIRCUNDIST', 'nomCircun',
       'TipoCircunscripcion', 'RECI', 'Recinto', 'Mesas', 'Habilitados',
       'latitud', 'longitud', 'rural_urbano', 'denspop']



# %% hidden=true
di['RECI'].duplicated().sum()

# %% hidden=true
di['RECI_GEO_FID'].duplicated().sum()

# %% hidden=true
de['RECI'].duplicated().sum()

# %% hidden=true
de['RECI_GEO_FID'].duplicated().sum()

# %% hidden=true
di['País'].value_counts()

# %% hidden=true
len(di)

# %% hidden=true
len(de)

# %% [markdown]
# #### merge

# %%
je = ['NumPaís','NumDep','NumProv','NumMuni','idloc',	'NumDist',	'NumZona',	'RECI']
te = ['pais','Ciudad','PROV','sec','idloc','dist','zona','RECI']

jn = ['NumDep','NumProv','NumMuni','idloc','NumDist','NumZona','CIRCUNDIST','RECI']
tn = ['dep','PROV','sec','idloc','dist','zona','CIRCUNDIST','RECI'] 

# %%
dic_e = {a:b for a,b in zip(je,te) }
dic_n = {a:b for a,b in zip(jn,tn) }

# %%
s='Hab_Inhab_depu_X_Mesa'
pn = os.path.join(ebu.DATA_PATH0,'2020',
                  'padron_oep','ESTADISTICAS_NACIONAL_EG_2020.xlsx')
pn = pd.read_excel(pn,sheet_name=s,skiprows=5)

# %%
pn1 = pn.iloc[:-1]

# %%
pn1

# %%
pn1[[*dic_n.values(),'nummesa']]
pn1['N_MESA'] = pn1['nummesa'].astype(np.int64)

# %%
pn1['nummesa'].astype()

# %%
