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
# abrimos el file de georeferencias
i = 'reci_interior'
e = 'reci_exterior'
path = os.path.join(ebu.DATA_PATH0,'2020','2020_geo_padron_final/2020_geo_padron_final.xlsx')
#nacional
dn = pd.read_excel(path, sheet_name=i)
#exterior
de = pd.read_excel(path,sheet_name=e)


# %%
# Verificar no duplicados
dn['RECI'].duplicated().sum()

# %%
dn['RECI_GEO_FID'].duplicated().sum()

# %%
de['RECI'].duplicated().sum()

# %%
de['RECI_GEO_FID'].duplicated().sum()

# %%
dn['País'].value_counts()

# %%
len(dn)

# %%
len(de)

# %% [markdown]
# #### merge

# %%
# columnas de traduccion
je = ['NumPaís','NumDep','NumProv','NumMuni','idloc',	'NumDist',	'NumZona',	'RECI']
te = ['pais','Ciudad','PROV','sec','idloc','dist','zona','RECI']

jn = ['NumDep','NumProv','NumMuni','idloc','NumDist','NumZona','CIRCUNDIST','RECI']
tn = ['dep','PROV','sec','idloc','dist','zona','CIRCUNDIST','RECI'] 

# %%
#diccionarios de traduccion
dic_e = {a:b for a,b in zip(je,te) }
dic_n = {a:b for a,b in zip(jn,tn) }

# %%
#abrir ope excel NAC
s='Hab_Inhab_depu_X_Mesa'
pn = os.path.join(ebu.DATA_PATH0,'2020',
                  'padron_oep','ESTADISTICAS_NACIONAL_EG_2020.xlsx')
#eliminat última columna na
pn = pd.read_excel(pn,sheet_name=s,skiprows=5, dtype={'nummesa':str}).iloc[:-1]

# %%
#abrir oep excel EXT
s='Hab_Inhab_Dep_X_Recinto_X_Mesa'
pe = os.path.join(ebu.DATA_PATH0,'2020',
                  'padron_oep','ESTADISTICAS_EXTERIOR_EG_2020.xlsx')

#eliminar última columna na
pe = pd.read_excel(pe,sheet_name=s,skiprows=5, dtype={'nummesa':str}).iloc[:-1]

# %%
# juntar dn con je
# juntar de con

# %%
