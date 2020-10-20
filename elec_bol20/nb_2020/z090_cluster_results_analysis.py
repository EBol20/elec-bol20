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

# %%
from elec_bol20 import *
import elec_bol20.util as ebu


# %%
path = 'datos_1_intermedios/2020/clustermodel/clustermodel_mesas_percentage_actual.csv'
path = os.path.join(ebu.DIR,path)
df = pd.read_csv(path,dtype={'ID_MESA':str})

# %%
df['ID_MESA'].isna().sum()

# %%
df.set_index('ID_MESA')

# %%
df['ID_RECI'] = df['ID_MESA'].str[:-2]
df = df[~df['ID_RECI'].isna()].set_index('ID_RECI')
df.index = df.index.astype(np.int64)

# %%
cart = os.path.join(ebu.DATA_PATH1_2020,'z030_carto_xy.csv')
cart = pd.read_csv(cart).set_index('ID_RECI')
cart.index = cart.index.astype(np.int64)

cart = os.path.join(ebu.DATA_PATH1_2020,'z030_carto_xy.csv')
cart = pd.read_csv(cart).set_index('ID_RECI')
cart.index = cart.index.astype(np.int64)


_mean = ['X', 'Y']
_sum = ['BL_perc_mean', 'NU_perc_mean',
       'MAS_perc_mean', 'CC_perc_mean', 'CREEMOS_perc_mean', 'FPV_perc_mean',
       'PAN_BOL_perc_mean', 'vv_mean']

df[_sum] =  df[_sum].multiply(df['HAB'],axis='index')

# %%

# %%
dj = df.join(cart)
l = len(dj)
gr = dj.groupby('ID_RECI') 

# %%
nd = gr[_mean].mean()
nd[_sum] = gr[_sum].sum()
nd['HAB'] = gr['HAB'].sum()
nd[_sum] = nd[_sum].multiply(1/nd['HAB'],axis='index')



# %%
nd['MAS_perc_mean']

# %%
va = 'CREEMOS_perc_mean'
def plo(va):
    C_DIC = {
        'CC_perc_mean':ebu.P_GRAD_CC,
        'FPV_perc_mean':ebu.P_GRAD_FPV,
        'MAS_perc_mean':ebu.P_GRAD_MAS,
        'CREEMOS_perc_mean':ebu.P_GRAD_CREEMOS,
        'PAN_BOL_perc_mean':ebu.P_GRAD_PANBOL,
    }



    MAX = nd[va].quantile(.99)

    nd['s'] = nd['HAB']/1000
    sr = bokeh.models.ColumnDataSource(nd)
    from bokeh.transform import linear_cmap
    from bokeh.transform import log_cmap

    cm = linear_cmap(va, palette=C_DIC[va], low=0, high=MAX)

    cb = bokeh.models.ColorBar(
        color_mapper=cm['transform'])

    f = bokeh.plotting.figure()
    f.scatter(x='X',y='Y',source = sr,color=cm,size = 's')
    f.add_layout(cb)
    f.title.text=va
    TOOL_TIP = [
        ('Inscritos', '@HAB'),
        ('PAIS, Municipalidad', '@PAIS, @MUN'),
        ('Recinto', '@REC'),
        (f'{va} [%]', f'@{va}{{0.0}}'),
    #     ('CC [%]','@cc{0.0}'),
    #     ('Diferencia [%]', '@ad_mas_cc{0.0} (@mas_o_cc)'),
        ('------','------')
        # ('DEN %', '@DEN')
        # ('PAIS', '@PAIS'),
    ]

    ho = bokeh.models.HoverTool(
    tooltips=TOOL_TIP
    )

    f.add_tools(ho)

    bokeh.plotting.output_notebook()
    bokeh.plotting.show(f)

ll=['MAS_perc_mean', 'CC_perc_mean', 'CREEMOS_perc_mean', 'FPV_perc_mean',
       'PAN_BOL_perc_mean']
    
for va in ll: plo(va)

# %%

# %%
