# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
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

# %% [markdown]
# [Página principal](https://ebol20.github.io/elec-bol20/)  
# [Artículos](https://ebol20.github.io/elec-bol20/articulos)

# %% [markdown]
# # ¿Qué pasó en las elecciones?
#
# HIPÓTESIS NO. 1: EL FACTOR CHI

# %% [markdown]
# Primera versión: 23 de Octubre de 2020 (en desarrollo)

# %% [markdown]
# <div style="text-align: right">Texto: Ana Lucía Velasco (avelascou@gmail.com)</div>
# <div style="text-align: right">Análisis de datos: Diego Aliaga</div>

# %% [markdown]
# [código fuente](https://github.com/EBol20/elec-bol20/blob/master/elec_bol20/nb_2020/z100_mas_chi2019_mas2020.ipynb)
#

# %% code_folding=[0]
# Importar librerías
from elec_bol20.nb_2020.z100_mas_chi2019_mas2020_fun import *

import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

# %% [markdown]
# Los resultados de las últimas elecciones presidenciales en Bolivia han generado mucha sorpresa en la población boliviana. Después de un final ajustado en el referéndum de la re-postulación del binomio Evo-Álvaro el año 2016 y de las controversiales elecciones nacionales del 2019, las expectativas sobre los resultados de las elecciones del 2020 eran muy altas. El margen de diferencia en el resultado final de las elecciones 2020 ha causado sorpresa. A pesar de esto, un breve análisis comparativo entre los datos oficiales de la elección del 2020 y la elección del 2019 arroja pistas interesantes que nos ayudan a entender mejor lo que pasó en las últimas elecciones.
#
# La primera hipótesis que trataremos aquí es la que hemos denominado como “el factor CHI”.

# %%
df20 = ebu.get_dataframe_2020()

df20['i2'] = df20.index



df19 = ebu.open_combine_2019()
df19['i0'] = df19.index

df = pd.merge(
    df19, df20, left_index=True, right_index=True,
    suffixes=['_19', '_20'],
    how='inner'
)

# %%
(df['i2'] - df['i0']).sum()

# %%
df

# %% code_folding=[0]
# Tabla 1
df = get_df()

# %%

# %% code_folding=[0]
pd.DataFrame(df[['VV_20','VV_19','HAB_20','HAB_19']].sum(),columns=['VOTANTES'])

# %% [markdown]
# <center>Tabla 1: Número de votantes válidos (VV) y habilitados (HAB) para este análisis. Solo utilizamos las mesas para las cuales el código de mesa no ha cambiado entre 2020 y 2019<center>

# %% [markdown]
# La siguiente información es obtenida realizando un [análisis de grupos](https://es.wikipedia.org/wiki/An%C3%A1lisis_de_grupos) (clusters) con el método de
# ['KMeans'](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html).
# El objetivo es agrupar en clusters a las mesas que han tenido cambios similares en los votos para cada partido, es decir, dónde la tendencia de la variación de votos en las mesas respecto al año pasado es comparable.
#
# Todo lo que está por encima de 0 en la siguiente figura (Fig. 1), representa votos que un partido político ganó respecto al año pasado, y lo que está por debajo equivale a los votos que el partido perdió.
# En el caso de Creemos que no participó en 2019, el cambio es siempre positivo.
# Lo opuesto ocurre con 21F que no participó en 2020.
#
# Los resultados de este análisis también se ven reflejados en la Tabla 2.

# %% code_folding=[]
# Fig. 1
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

m=5
# cools = {i:i for i in range(m)}
# CLUS_DIC=cools
df1 = cluster_analysis(df=df,seed = 1,n=m)

nm_dic = df1.groupby(CLUS).count().iloc[:,0].to_dict()
nm_dic = {b:f'{b}\n$_{{({nm_dic[b]} \mathrm{{\ mesas}})}}$' for a,b in CLUS_DIC.items()}
mel = pd.melt(df1[[*COLUMNS_CLUS, CLUS]], id_vars=CLUS)
# mel[CLUS] = mel[CLUS].apply(lambda r: nm_dic[r])

# CLUS_DIC = {0: '++MAS', 1: '+MAS', 2: '+CRE', 3: '++CRE', 4: '+CC'}
mea = df1[[*COLUMNS_CLUS,CLUS]].groupby(CLUS).mean()
mea['SUM'] = mea.sum(axis=1)
f, ax = plt.subplots(figsize=(8, 4),dpi=300)
sns.barplot(x=CLUS, y='value', data=mel, hue='variable',
            order=nm_dic.keys(), ci='sd');
ax.set_ylabel('$\mathrm{DELTA}_{20-19}$ [% por mesa]');

labs = ax.get_xticklabels()
labs = [matplotlib.text.Text(i.get_position(),text=nm_dic[i.get_text()]) for i in labs]
rr=ax.set_xticklabels(labs)
ax.set_ylim(-60,90)
ax.set_xlim(-.5,7)
sns.despine(ax=ax,offset=10,bottom=True)


# %% code_folding=[0]
nm_dic = df1.groupby(CLUS).count().iloc[:,0].to_dict()
nm_dic = {b:f'{b}\n$_{{({nm_dic[b]} \mathrm{{\ mesas}})}}$' for a,b in CLUS_DIC.items()}
mel = pd.melt(df1[[*COLUMNS_CLUS, CLUS]], id_vars=CLUS)
# mel[CLUS] = mel[CLUS].apply(lambda r: nm_dic[r])


# %% code_folding=[]
# CLUS_DIC = {0: '++MAS', 1: '+MAS', 2: '+CRE', 3: '++CRE', 4: '+CC'}
mea = df1[[*COLUMNS_CLUS,CLUS]].groupby(CLUS).mean()
mea['SUM'] = mea.sum(axis=1)
f, ax = plt.subplots(figsize=(8, 4),dpi=200)
sns.barplot(x=CLUS, y='value', data=mel, hue='variable',
            order=nm_dic.keys(), ci='sd');
ax.set_ylabel('$\mathrm{DELTA}_{20-19}$ [% por mesa]');

labs = ax.get_xticklabels()
labs = [matplotlib.text.Text(i.get_position(),text=nm_dic[i.get_text()]) for i in labs]
rr=ax.set_xticklabels(labs)
ax.set_ylim(-60,90)
ax.set_xlim(-.5,7)
sns.despine(ax=ax,offset=10,bottom=True)


# %%

# %%
def ss(i,y0,y1):
    ax.set_ylim(y0,y1)
    ax.set_xlim(i-.5,i+.5)
    f.set_figwidth(1)
    f.set_figheight(2)
    ax.legend([])
    return f


# %%
ss(0,-20,40)

# %%
ss(1,-10,20)

# %%
ss(2,-40,60)

# %%
ss(3,-60,70)

# %%
ss(4,-10,15)

# %%
df1.columns

# %%
df['clus'] = df1['Cluster']


# %%
df.columns

# %%
cols = ['mas_19','mas_20','cc_19','cc_20','creemos_19','creemos_20','21f_19','21f_20',
   'chi_19','chi_20','dotros_19','dotros_20','nb_19','nb_20'
   ]

# %%
cc = sns.color_palette("tab10",n_colors=7)
nc = []
for c in cc:
    nc.append(np.array(c)*1)
    nc.append(c)


# %%
def _plt(cl = '++MAS',i=101):
    f,ax = plt.subplots(figsize=(2.5,3),dpi=200)
    _dd = df[df['clus'] == cl].iloc[i][cols]
    _dd.plot.barh(color= nc,ax=ax)
    ax.set_xlabel('%')
_plt('++MAS')

# %%
_plt('++CRE')

# %%
_plt('+CC',i=200)

# %% [markdown]
# <center>Fig. 1: Porcentaje del cambio de votos para cada mesa entre 2020 y 2019 por cluster. Las líneas negras muestran la desviación estandard. * NB= nulos blancos <center>

# %% code_folding=[0]
# Tabla 2

mea.round()

# %% [markdown]
# <center>Tabla 2: Porcentajes de votos mostrados en la Fig. 1. <center>

# %% [markdown]
# En este gráfico (Fig. 1) mostramos 5 casos identificados. Los primeros dos casos son los de los clusters ++MAS y +MAS. El primero muestra cerca a 7 mil mesas de votación y el segundo cerca a 11 mil mesas. En el primer caso el MAS se beneficia de un gran número de votos de Chi, Carlos Mesa y votos nulos y blancos, en ese orden. Creemos parece beneficiarse de una cantidad pequeña de votos que quedaron cautivos por la retirada de la sigla del 21F (este es nuestro supuesto dada la afinidad política). En el segundo caso, el comportamiento es similar pero el aumento de votos del MAS no es tan alto y en comunidad ciudadana no se da ni un aumento ni un decremento.
#
#
# En los siguientes clusters +CRE y ++CRE podemos ver los casos en los que la agrupación Creemos ha obtenido votos y de dónde los obtuvo. Ambos clusters están compuestos de cerca de 8 mil mesas de sufragio. En ambos casos vemos cómo antiguos votantes de CC, de 21F y de Chi, en ese orden, beneficiaron en mayor y abrumadora medida a Creemos y, en una pequeña minoría, al MAS. De estos datos podemos ver que aquellos votantes que se han desencantado con el MAS y decidieron dar su apoyo a CC o a Creemos, sí existen, pero son casos excepcionales, el caso más común es el ex votante de Chi que decide dar su voto al MAS y ex votantes de CC que deciden dar su voto a Creemos.
#
# Resumiendo: ¿Cómo cambió el voto entre el 2019 al 2020? Principalmente, el 7.30% de votación que perdió Chi el 2020 fue en mayor medida hacia el MAS y en menor medida a Creemos, y en mucha menor medida a CC. El segundo cambio evidente es que Creemos recogió la votación de la agrupación 21F, poco de la votación de Chi y menos aún de votantes del MAS, pero logró atraer a un importante porcentaje del voto de CC. Podemos ver los siguientes datos en números absolutos en el siguiente gráfico y tabla (Fig. 2, Tabla 3).

# %%

# %% code_folding=[]
# Fig. 2
ds = df1.copy()
ds[COLUMNS_CLUS] = df1[COLUMNS_CLUS].multiply(df1['VV_20'], axis=0) / 100

mel1 = pd.melt(ds[[*COLUMNS_CLUS, CLUS]], id_vars=CLUS)
mel1 = mel1.groupby([CLUS, 'variable']).sum()



# noinspection PyRedeclaration
f, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
sns.barplot(x=CLUS, y='value', data=mel1.reset_index(), hue='variable',
            order=CLUS_DIC.values(), hue_order=COLUMNS_CLUS);
ax.set_ylabel('$\mathrm{DELTA}_{20-19}$ [Número de Votos]');

ax.set_ylim(-300000,600000)
ax.set_xlim(-.5,6)
sns.despine(ax=ax,offset=10,bottom=True)


# %%
ds

# %%
# Fig. 2
ds = df1.copy()
ds[COLUMNS_CLUS] = df1[COLUMNS_CLUS].multiply(df1['VV_20'], axis=0) / 100 / 5557961 * 100


mel1 = pd.melt(ds[[*COLUMNS_CLUS, CLUS]], id_vars=CLUS)
mel1 = mel1.groupby([CLUS, 'variable']).sum()



# noinspection PyRedeclaration
f, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
sns.barplot(x=CLUS, y='value', data=mel1.reset_index(), hue='variable',
            order=CLUS_DIC.values(), hue_order=COLUMNS_CLUS);
ax.set_ylabel('$\mathrm{DELTA}_{20-19}$ [%]');

ax.set_ylim(-6,10)
ax.set_xlim(-.5,6)
sns.despine(ax=ax,offset=10,bottom=True)

# %% [markdown]
# <center>Fig 2. Cambio de voto en valor absoluto para cada cluster mostrado en la Fig. 1.<center>

# %% code_folding=[]
# Tabla 3
tab=mel1.round().astype(int)
tab=tab.reset_index().set_index([CLUS,'variable']).unstack()
tab=tab['value'].T
tab= pd.DataFrame(tab.to_dict()).T
tab['SUM'] = tab.sum(axis=1)
tab

# %%
# Tabla 3
tab=(mel1)
tab=tab.reset_index().set_index([CLUS,'variable']).unstack()
tab=tab['value'].T
tab= pd.DataFrame(tab.to_dict()).T
tab['SUM'] = tab.sum(axis=1)
tab = tab.T
tab['SUM'] = tab.sum(axis=1)
tab = tab.T
tab = (tab/5557961 * 100*10).round()/10
tab

# %%
sns.heatmap(tab.T.iloc[:-1,:-1],annot=True,center=0,cmap = 'RdBu_r')

# %%
a = df['MAS_20'].sum()/df['VV_20'].sum()*100

# %%
b = df['MAS_19'].sum()/df['VV_19'].sum()*100

a-b

# %% [markdown]
# <center>Tabla 3: Cantidad de votos mostrados en la Fig. 2.<center>

# %% code_folding=[0]
# Fig. 3
bokeh.plotting.reset_output()
bokeh.plotting.output_notebook()
plot_clusters_carto(df1=df1);

# %% [markdown]
# <center>Fig. 3: Posicionamiento de cada cluster en el cartograma de Bolivia descrito en <a href="https://ebol20.github.io/elec-bol20/Ejemplos/que_es_un_cartograma.html">ebol20</a>. Puedes hacer clic en la leyenda para desactivar cada grupo.<center>

# %% [markdown]
# Ahora veamos dónde se encuentran localizadas estas mesas en el mapa del país. El cluster ++MAS y +MAS se encuentran representados en color azul y naranja, respectivamente. Podemos ver que la mayoría de votos que ha ganado el MAS, provenientes de estos clusters, se encuentran en lugares como El Alto y La Paz, así como zonas periurbanas de las ciudades capitales de La Paz, Cochabamba, Sucre y Oruro, principalmente.
#
# El caso de los clusters de +CRE y ++CRE se encuentran representados en amarillo y verde. Aquí podemos ver que los cambios se han concentrado fundamentalmente en la ciudad de Santa Cruz y sus alrededores, así como algunos sectores del departamento de Pando.
#
# Finalmente, el cluster +CC puede encontrarse fundamentalmente en todas las ciudades capitales, en mayor o menor medida, salvo en Santa Cruz.
#
# Si bien resulta evidente que la candidatura de Fernando Camacho y Marco Pumari significó una importante merma de votos para los candidatos de Comunidad Ciudadana; este fenómeno no permite explicar cómo el MAS logró subir tanto su porcentaje de votación en la reciente contienda electoral. El dato final del cómputo 2020 dejó sorprendidos a analistas y estrategas, parece ser que en los análisis vertidos hasta ahora se han estado olvidando del factor Chi.
#
# En las gráficas podemos ver que los votos nulos y blancos también jugaron un rol importante, que debe ser explicado aparte. Esto será expuesto en un siguiente artículo o versión.


# %% [markdown]
# # Material complementario

# %% code_folding=[0]
# Fig. 4
((df[DMAS_M_DCHI]*df['VV_20']/100).mean()).round()

((df[DMAS]*df['VV_20']/100).mean()).round()

(df['VV_20']).mean()


import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
pl_dic = {

    'A':{'a':DCHI,'b':DMAS,'c':DMAS_M_DCHI},
    'B':{'a':DCC,'b':DMAS,'c':DMAS_M_DCC},
#     'C':{'a':D21F,'b':DMAS,'c':DMAS_M_D21F},
}

i = 0
st = 'ABCDEF'
for a,A in pl_dic.items():
    a = A['a']
    b = A['b']
    c = A['c']

    _df = df[[a,b,c,'VV_20']].dropna(how='any')

    # noinspection PyTypeChecker
    f, axs = plt.subplots(1, 3, figsize=[16, 3], sharex=True, sharey=True, dpi=150)
    axf = axs.flatten()
    def _pl(ax,a,t):
        bs = np.arange(-60,71,3)
        sns.distplot(_df[a]*_df['VV_20']/100, ax=ax,
#                      hist_kws={'weights':_df['HAB_20']*np.abs(_df[a])},
                     kde=False,
                    bins=bs)
        ax.set_ylabel('N. de mesas')
        ax.set_xlabel(ax.get_xlabel() + f'{a} [Votos por mesa]')
        ax.text(0.01,1.02,t,transform=ax.transAxes)
    _pl(axf[0],a,st[i]);i=i+1
    _pl(axf[1],b,st[i]);i=i+1
    _pl(axf[2],c,st[i]);i=i+1

# %% [markdown]
# <center>Fig. S1: Panel A muestra un histograma de diferencias de voto por mesa entre 2020 y 2019 para CHI. El panel B hace lo mismo para MAS. El panel C es el resultado de (MAS20-MAS19) + (CHI20-CHI19). Los paneles  D, E y F muestran lo mismo que A, B y C pero para CC y MAS.
# sasdf
#     <center>

# %% [markdown]
# En la Fig. S1, se puede apreciar la diferencia de la cantidad de votos que recibió Chi el año 2020 y 2019. A la izquierda del punto medio marcado por el cero se muestra dónde perdió votos, y a la derecha, los votos ganados por Chi el año 2020. Al lado (B), hacemos el mismo ejercicio para el MAS. En el tercer panel (C) sobreponemos las diferencias de votos sacados entre el 2019 y el 2020 por ambos candidatos y podemos apreciar que se equilibran entre sí. En otras palabras el promedio y la media de B es 14 votos por mesa mientras que el promedio de C es 1 voto por mesa. Es decir, la pérdida de CHI llega a explicar 13 de los 14 votos ganados por MAS.
# Hemos repetido el mismo ejercicio para CC y el MAS, en la segunda línea de gráficos. Aquí podemos ver que al comparar los votos obtenidos por el MAS y CC tanto el 2019 como en el 2020, ambos no se equilibran entre sí. Esto demuestra que la diferencia de la votación del MAS obtenida este año, en comparación a la obtenida el año pasado se explica mucho mejor por una migración de votos de Chi al MAS, que por una migración de votos de CC al MAS.
#
#

# %%
# Fig. A 1
plot_3_comparison(df=df);

# %% [markdown]
# <center>Fig S2. En al panel A se oberva la diferencia de CHI20 y CHI19 por mesa electoral. En el panel B hacemos el mismo ejercicio para MAS. Pot último, en el panel C hacemos la suma A + B, es decir, tratamos de ver cuán bien el aumento de MAS es explicado por la derrota de CHI.<center>

# %%

# %%
path = os.path.join(ebu.DIR,'nb_2020','z102_mas_chi2019_mas2020-1.ipynb')
phtml = path.replace('.ipynb','.html')
# !jupyter nbconvert --to html_hc  --TemplateExporter.exclude_input=True --no-prompt {path}
# !open {phtml}

# %%

# %%

# %%

# %%
