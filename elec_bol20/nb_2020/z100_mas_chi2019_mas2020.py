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

# %% [markdown] heading_collapsed=true
# ###### import

# %% hidden=true
import elec_bol20.util as ebu
from elec_bol20 import *
# %% [markdown]
# ##### code

# %%

DCHI = 'CHI20 - CHI19'
DMAS = 'MAS20 - MAS19'
DCRE = 'CRE20 - CRE19'
D21F = '21F20 - 21F19'
DCC = 'CC20 - CC19'
DMAS_M_DCHI = f'({DMAS}) + ({DCHI})'
df20 = ebu.get_dataframe_2020()
df19 = ebu.open_combine_2019()

# %%
#join 20 with 19
df = pd.merge(
    df19,df20,left_on='ID_MESA', right_on='ID_MESA',
    suffixes=['_19','_20'],
    # how='inner'
              )
# clean 0 vote tables from last election
df = df[df['VV_19']>0]



# %%
df['mas_20'] = df['MAS_20']/df['VV_20']*100
df['mas_19'] = df['MAS_19']/df['VV_19']*100
df[DMAS] = df['mas_20'] - df['mas_19']

df['chi_20'] = df['FPV']/df['VV_20']*100
df['chi_19'] = df['PDC']/df['VV_19']*100
df[DCHI] = df['chi_20'] - df['chi_19']


df['cc_20'] = df['CC_20']/df['VV_20']*100
df['cc_19'] = df['CC_19']/df['VV_19']*100
df[DCC] = df['cc_20'] - df['cc_19']

df['creemos_20'] = df['CREEMOS']/df['VV_20']*100
df['creemos_19'] = 0
df[DCRE] = df['creemos_20'] - df['creemos_19']

df['21f_20'] = 0
df['21f_19'] = df['21F']/df['VV_19']*100
df[D21F] = df['21f_20'] - df['21f_19']
l = len(df)
df['xj'] = df['X_20'] + (np.random.randn(l)-.5) * .002 * np.sqrt(df['DEN_20'])
df['yj'] = df['Y_20'] + (np.random.randn(l)-.5) * .002 * np.sqrt(df['DEN_20'])
# %%
from sklearn.cluster import KMeans
cols = [DMAS, DCC, DCRE, D21F,DCHI]
df1=df[[*cols,'xj','yj']].dropna(how='any',axis=0)
N=5
kmeans = KMeans(n_clusters=N).fit(df1[cols])

df1['l'] = kmeans.labels_

# %%
df1.groupby('l').sum()

# %%
df1.groupby('l')[cols].sum().plot.bar()
plt.gca().set_ylim(-250000,400000)

# %%

f,ax=plt.subplots(figsize=(13,13))
sns.scatterplot(x='xj',y='yj', data=df1,hue='l',palette=sns.color_palette("Set1")[:N])

# %%
nf = pd.DataFrame(kmeans.cluster_centers_,columns=cols)

# %%
nf.plot.bar()

# %%
df[DMAS_M_DCHI] = df[DMAS] + df[DCHI]



df['s'] = np.sqrt(df['HAB_20']/45000)



df = df.sort_values('DEN_20')
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


cols = [
    # 'mas_20','mas_19',
    'xj','yj','s',
    DMAS, DCHI,
    DMAS_M_DCHI
]

HW = 400
f = bokeh.plotting.Figure(width=HW, height=HW, output_backend="webgl")
f1 = bokeh.plotting.Figure(width=HW, height=HW, output_backend="webgl")
f2 = bokeh.plotting.Figure(width=HW, height=HW, output_backend="webgl")

sr = bokeh.plotting.ColumnDataSource(df[cols])

cm = bokeh.transform.linear_cmap(VAR, palette=PAL, low=CMIN, high=CMAX)
cm1 = bokeh.transform.linear_cmap(VAR1, palette=PAL1, low=CMIN1, high=CMAX1)
cm2 = bokeh.transform.linear_cmap(VAR2, palette=PAL2, low=CMIN2, high=CMAX2)
cb = bokeh.models.ColorBar(
    color_mapper=cm['transform'], width='auto',
    location=(0, 1),
    title="",
    # margin=0,padding=0,
    title_standoff = 10
)

# f.scatter(x='xj',y='yj',source=sr,color=cm,radius='s')

f.scatter(x='xj',
          y='yj',
          source=sr,
          color=cm,
          radius='s',
          # size = 1,
          alpha=.5
          )
f.add_layout(cb,'center')
f.title.text = VAR

f1.scatter(x='xj',
          y='yj',
          source=sr,
          color=cm1,
          radius='s',
          # size = 1,
          alpha=.5
          )
f1.title.text = VAR1
f1.add_layout(cb,'center')

f2.scatter(x='xj',
           y='yj',
           source=sr,
           color=cm2,
           radius='s',
           # size = 1,
           alpha=.5
           )
f2.title.text = VAR2
f2.add_layout(cb,'center')



lay = bokeh.layouts.row([f,f1])
lay = bokeh.layouts.gridplot([[f,f1],[f2,None]])


# %% [markdown]
# ##### plot

# %%
bokeh.plotting.output_notebook()
bokeh.plotting.show(lay)

# %%
df

# %%
import numpy as np

from bokeh.io import output_file, show
from bokeh.models import HoverTool
from bokeh.plotting import figure

n = 500
_df = df[[DCHI,DMAS]].dropna().copy()
x = _df[DCHI]
y = _df[DMAS]

p = figure(title="Hexbin for 500 points", match_aspect=True,
#            tools="wheel_zoom,reset",
           background_fill_color='#440154')
p.grid.visible = False

# r, bins = p.hexbin(x, y, size=.5, hover_color="pink", hover_alpha=0.8)

p.circle(x, y, color="white", size=1,alpha=.5)

p.add_tools(HoverTool(
    tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
    mode="mouse", point_policy="follow_mouse", renderers=[r]
))



show(p)

# %%
f,axs = plt.subplots(1,3,figsize=[16,3],sharex=True,sharey=True,dpi=150)
axf = axs.flatten()
sns.histplot(df[DCHI], ax=axf[0])
sns.histplot(df[DMAS], ax=axf[1])
sns.histplot(df[DMAS_M_DCHI], ax=axf[2]);
# %% [markdown]
#

# %%
df

# %%
