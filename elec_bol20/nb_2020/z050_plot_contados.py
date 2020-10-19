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
# ###### init

# %%
# de los resultados generales crea silmulaciones con % de
# datos para que luego sean procesados

# %%

# %%

# %%

# %%
# import
from elec_bol20 import *
import elec_bol20.util as ebu
import bokeh.layouts
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure
# output_file, show
import bokeh.tile_providers



# %%
bokeh.plotting.output_file(os.path.join(ebu.DIR,'htlml_1_intermedios/2020/z050_panel.html'))
# bokeh.plotting.output_notebook()

# %%
df2= ebu.get_dataframe_2020()


# %%
df2['COUNT'].sum()

# %%
df2['HAB']

# %%
bokeh.plotting.output_notebook()
COL_LLEGO = '#aaaaaa'
COL_FALTA = '#db2879'


ll = len(df2)
np.random.seed(100)
df2['xj'] = df2['X'] + np.random.rand(ll) * .5
np.random.seed(200)
df2['yj'] = df2['Y'] + np.random.rand(ll) * .5
cols = ['yj','xj','PAIS','MUN','REC','HAB','COU']

df2['COU'] = 'No'
df2.loc[df2['COUNT'],'COU'] = 'Sí'

s1 = df2[df2['COUNT']][cols]
s2 = df2[~df2['COUNT']][cols]
sr1 = bokeh.models.ColumnDataSource(s1)
sr2 = bokeh.models.ColumnDataSource(s2)


f = bokeh.plotting.figure(output_backend="webgl",height=500,width=500)
f.scatter(x='xj',y='yj',source = sr2,color=COL_FALTA,radius=.05, alpha=1, legend_label='Mesas por computar (haz click)')
f.scatter(x='xj',y='yj',source = sr1,color=COL_LLEGO,radius=.05, alpha=1, legend_label='Mesas computadas (haz click)')
f.legend.click_policy="hide"




# %%
dfn = df2.copy()
dfn.loc[~dfn['BOL'],'DEN_CODES'] = -1

# %%
_df = dfn
gr = _df.groupby('DEN_CODES')
den = gr[['HAB']].sum()
den['cum'] = den['HAB'].cumsum()
tot = den['HAB'].sum()
den['mid'] = den['cum'] - den['HAB']/2
den['top'] = 100
den['width'] = den['HAB']-(tot*.01)
den1 = den.copy()

# %%
_df = dfn[dfn['COUNT']]
gr = _df.groupby('DEN_CODES')
den = gr[['HAB']].sum()
den['cum'] = den['HAB'].cumsum()
tot = den['HAB'].sum()
den['mid'] = den['cum'] - den['HAB']/2
den['top'] = 1
den['width'] = den['HAB']-(tot*.01)
den2 = den.copy()

# %%
dfn['HAB']

# %%
den1['counted'] = den2['HAB'].astype(np.int64)

# %%
den1['top_c'] =den1['counted']/den1['HAB']*100

# %%
den1.loc[-1,'mid'] = den1.loc[-1,'mid'] - 1000000

# %%
df2[df2['COUNT']]['HAB'].sum()

def _t(s):
    if np.isnan(s): s=0
    return f'{s:0.1f}'

def _t1(s):
    if np.isnan(s): s=0
    return f'{s:0.0f}'

def _t2(r):
#     return f'{r["tv"]} ({r["tc"]} %)'
    return f'{r["tc"]}%'

den1['tc']=den1['top_c'].apply(_t)
den1['tv']=den1['counted'].apply(_t1)
den1['text'] = den1.apply(_t2,axis=1)

# %%


p = bokeh.plotting.figure(height=250)
# fi = bokeh.plotting.figure()
p.vbar(x=den1['mid'],width=den1['width'],top=den1['top'],color=COL_FALTA)
p.vbar(x=den1['mid'],width=den1['width'],top=den1['top_c'],color=COL_LLEGO)
p.title.text = ''

x = den1[den1.index>=0]['mid'].mean()
p.text(x=[x],y=[140],text=['Nacional'])

an = .35
x = den1[den1.index==0]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad baja (0-50)'],angle=an, text_font_size="8pt")

x = den1[den1.index==1]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad media (50-500)'],angle=an, text_font_size="8pt")

x = den1[den1.index==2]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad moderada (500-1500)'],angle=an, text_font_size="8pt")

x = den1[den1.index==3]['mid'].mean()
p.text(x=[x],y=[101],text=['Densidad alta > 1500'],angle=an, text_font_size="8pt")

x = den1[den1.index<0]['mid'].mean()
p.text(x=[x],y=[110],text=['Exterior'],text_align='center')
p.xaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
f.yaxis.visible = False
f.yaxis.visible = False
p.y_range.start=0
p.y_range.end=160
p.yaxis.axis_label="Porcentaje"
ppp=den1['counted'].sum()/den1['HAB'].sum() * 100
p.title.text = f'Porcentaje de votos computados por densidad (total computado={ppp:0.1f}%)'
p.xaxis.axis_label=f'Porcentaje total de votos computados = ({ppp:0.1f}%)'
p.toolbar.logo = None
p.toolbar_location = None

f.title.text = "Cartolocación de las mesas"

for l,r in den1.iterrows():
    if l ==-1:
        x = r['mid'] + 400000
    else:
        x = r['mid']

    p.text(x=x,y=[r['tc']],text=[r['text']],text_align='center',text_font_size="8pt")



_c = ['CREEMOS',	'MAS',	'FPV',	'PAN_BOL',	'CC']
dd= df2[[*_c,'VV']].copy()
res = dd[_c].sum()/dd['VV'].sum()*100
res.name = 'per'
res.index.name ='party'
res= res.reset_index()
res['i'] =  res.index+.5
se = pd.Series(ebu.C_DIC)
se.name='colors'
res = pd.merge(res,se,left_on='party',right_index=True)

source = ColumnDataSource(res)

r = bokeh.plotting.figure(x_range=res['party'], toolbar_location=None,height=250)
r.vbar(x='i', top='per', width=0.9, source=source,
       line_color='white', fill_color=bokeh.transform.factor_cmap('party', palette=res['colors'], factors=res['party']))

def _f(p): return f'{p:0.1f}%'
res['t']=res['per'].apply(_f)

r.text(x=res['i'],y=res['per'],text=res['t'],text_align='center')

r.xgrid.grid_line_color = None
r.y_range.start = 0
r.y_range.end = np.ceil(res['per'].max()/20)*20
r.title.text = f'Porcentaje sobre el total de votos válidos computados ({ppp:0.1f}%)'


TOOL_TIP = [
    ('Inscritos', '@HAB'),
    ('PAIS, Municipalidad', '@PAIS, @MUN'),
    ('Recinto', '@REC'),
    ('Computada','@COU'),
    # ('MAS [%]', '@mas{0.0}'),
    # ('CC [%]','@cc{0.0}'),
    # ('Diferencia [%]', '@ad_mas_cc{0.0} (@mas_o_cc)'),
    ('------','------')
    # ('DEN %', '@DEN')
    # ('PAIS', '@PAIS'),
]

hover_map = bokeh.models.HoverTool(
    tooltips=TOOL_TIP,
    # callback=callback_red_car,
    # renderers = [red_scat_map]
)
f.add_tools(hover_map )

l0 = bokeh.layouts.column([r,p,f],sizing_mode='scale_width')
lay = l0
l0.max_width = 700
# lay = bokeh.layouts.row([l0,f])
# lay = p
# %%
bokeh.plotting.show(lay)

# %%
