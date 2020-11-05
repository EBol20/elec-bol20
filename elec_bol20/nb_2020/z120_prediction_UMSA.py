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
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: ebol20
#     language: python
#     name: ebol20
# ---

# %%
from elec_bol20 import *
import elec_bol20.util as ebu
import elec_bol20.nb_2020.z120_fu  as zfu
from elec_bol20.nb_2020.z120_fu import *

# %%
df = ebu.get_full_combined_2020()
df = zfu.add_point(df)

# %%
(~df[COUNT]).sum()

# %%
df[PC].describe()

# %%
df[VAL].sum() / df[VV].sum() * 100


# %%
def _run():
    dat = []
    N = 60
    B = 2
    df[COUNT] = True
    full_coverage = zfu.get_coverage(df, buffer=B)
    for i in np.linspace(0, 100, N)[1:]:
        P = i
        res = predict_p(df=df, p=P)
        counted_coverage = zfu.get_coverage(zfu.get_counted(df), buffer=B)

        cov = 100 - (counted_coverage.area / full_coverage.area * 100)

        res = {'p': i, **res, 'cov': cov}
        dat.append(res)
    pdf = pd.DataFrame(dat)


# %%
# run()
pout = os.path.join(ebu.DATA_PATH1,'z120_prediction_area.csv')
# pdf.to_csv(pout)
pdf = pd.read_csv(pout,index_col=0)

# %%
pdf['unc'] = pdf['cov']/3
pdf['m'] = -pdf['unc'] + pdf['pred'] - .1
pdf['M'] = pdf['unc'] + pdf['pred'] + .1
# pdf

# %%
RES = pdf.iloc[-1]['pred']

# %%
pdf['abs_res'] = (pdf['pred'] - RES).abs()

# %%
f,ax = plt.subplots(dpi=150)
pdf['Predicción'] = pdf['pred']
ax.fill_between(pdf['p'],pdf['m'],pdf['M'],alpha=.5)
pdf.plot(x='p', y='Predicción', marker='o',ax=ax)
ax.set_xlabel('Cómputo [%]')
ax.set_ylabel('Predicción resultado final MAS [%]')

# %%
ax.set_xlim(60,100)
ax.set_ylim(50,60)
f

# %%
pdf.plot(x='p', y='cov', marker='o')

# %%
pdf.plot.scatter(x='abs_res', y='cov')

# %%
df_ = simple_split(df, 20)
cols = ['yj', 'xj', 'PAIS', 'MUN', 'REC', 'HAB', COUNT,'MAS']
bokeh.plotting.reset_output()
bokeh.plotting.output_notebook()
f: bokeh.plotting.Figure = bokeh.plotting.figure()
df_ = df_[df_[COUNT] == True]
s = bokeh.plotting.ColumnDataSource(df_[cols])
f.scatter('xj', 'yj', source=s, color='green',
#           size='HAB'
         )
bokeh.plotting.show(f)

# %%
B = .3
P = 40

# %%
df = zfu.add_point(df)

# %%
full_coverage = zfu.get_coverage(df, buffer=B)

# %%
df = zfu.simple_split(df, P)
counted_coverage = zfu.get_coverage(zfu.get_counted(df), buffer=B)

# %%
f, ax = plt.subplots()
gp.GeoSeries(full_coverage).plot(figsize=(10, 10), color='blue', ax=ax)
gp.GeoSeries(counted_coverage).plot(figsize=(10, 10), color='red', ax=ax)

# %%
diff = full_coverage.difference(counted_coverage)

# %%
gp.GeoSeries(diff).plot()

# %%
diff.area / full_coverage.area

# %%
import random

# %%
dat = []
for i in range(1000):
    random.seed(i)
    r = random.random()
    dtest, dtrain = ebu.partition_df(df, r, random_state=i)
    dtest[COUNT] = False
    dtrain[COUNT] = True
    df = pd.concat([dtest, dtrain])
    # gp.GeoSeries(zfu.get_coverage(zfu.get_counted(df))).plot()
    res = ebu.single_pred(df=df, var=VAL, pred_mask=COUNT)
    res = {'i': i, 'p': r * 100, **res}
    dat.append(res)

# %%
matplotlib.scale.SymmetricalLogScale

# %%
res_df = pd.DataFrame(dat)
res_df['res'] = res_df['pred'] - RES
f, ax = plt.subplots()
res_df.plot.scatter(x='p', y='res', ax=ax, alpha=.5, marker='o', color='k')
ax.axhline(0, c='r')
ax.set_yscale('symlog', linthresh=.1)

# %%
res_df['res_abs'] = res_df['res'].abs()
res_df.sort_values('res_abs', ascending=False)

# %%
dtest, dtrain = ebu.partition_df(df, .005,
                                 #                                 random_state=10
                                 )
dtest[COUNT] = False
dtrain[COUNT] = True
df = pd.concat([dtest, dtrain]).sort_index()
ebu.single_pred(df=df, var=VAL, pred_mask=COUNT)

# %%
items = ["a", "b", "c", "d"]

distribution = [.99, .005, .005, 0]
num_samples = 4
samples = np.random.choice(items, 2, False, distribution)
samples

# %%

# %%
df['covered'] = [p.within(counted_coverage) for p in df.geometry]

# %%
df[~df['covered']]['HAB'].sum() / df['HAB'].sum() * 100

# %%
