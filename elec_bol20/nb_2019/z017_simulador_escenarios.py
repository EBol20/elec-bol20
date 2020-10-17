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
# ##### import

# %%
# de los resultados generales crea silmulaciones con % de datos para que luego sean procesados
from elec_bol20 import *
import elec_bol20.util as ebu

# %% [markdown]
# ##### open data

# %%
# abrimos la base de datos del 2019
df = ebu.open_combine_2019()
df['D_MAS_CC'] = df['MAS'] - df['CC']

#eliminamos los datos donde votos válidos son 0
df = df[df['VV']>0]

# %%
df


# %% [markdown]
# ## Predicción

# %%
# %matplotlib notebook
f,ax = plt.subplots()
#partimos la base de datos en dos
for i in range(1000):
    np.random.seed(i)
    rr = np.random.rand(1)
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
    ax.scatter(rr,calc_dmascc,c='k',alpha=.1)
    f.canvas.draw()

# %%

# %%

# %%

# %%
len(test), len(train)



# %% [markdown]
# ## juntar

# %%
mas_p = MAS_p/VV_p * 100

test['mas'] = test['MAS']/test['VV'] * 100
train['mas'] = train['MAS']/train['VV'] *100
test['mas_p'] = mas_p
test['mas_r'] = test['mas'] - test['mas_p']
sns.distplot(test['mas_r']);plt.show()
print(test['mas_r'].mean())
print(test['mas_r'].median())

# %%
bokeh.plotting.output_notebook()
to = bokeh.models.HoverTool(tooltips=ebu.TOOL_TIPS)

_train = bokeh.models.ColumnDataSource(train)
_test = bokeh.models.ColumnDataSource(test)
_val = train
pa = ebu.P_MAS

mapper_t = bokeh.transform.linear_cmap(
    field_name='mas', palette=pa, low=0, high=80)
mapper_p = bokeh.transform.linear_cmap(
    field_name='mas_p', palette=pa, low=0, high=80)

mapper_d = bokeh.transform.linear_cmap(
    field_name='mas_p', palette=ebu.P_DIF, low=-100, high=100)

p = bokeh.plotting.figure(output_backend="webgl")
p.add_tools(to)
for t, l, c in zip([_train, _test, _test,_test],
                   ['train', 'test', 'result','dif'],
                   [mapper_t, mapper_p, mapper_t,mapper_d]):
    p.scatter('X', 'Y',
              # radius='r',
              fill_color=c, source=t,
              line_color=None,
              legend_label=l
              )
color_bar = bokeh.models.ColorBar(
    color_mapper=mapper_t['transform'],
    location=(1, 1)
)
p.add_layout(color_bar, 'left')
p.legend.location = "top_left"
p.legend.click_policy = "hide"
bokeh.plotting.output_file(os.path.join(ebu.DATA_FIG_OUT,'asdf.html'))
# bokeh.plotting.show(p,browser='safari/Applications/)/

# %%

# %%
