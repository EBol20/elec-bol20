from elec_bol20 import *
import elec_bol20.util as ebu
import bokeh.layouts
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure, output_file, show
import bokeh.tile_providers

p = os.path.join(ebu.DATA_PATH1_2020,'comp/exportacion_EG2020_actual.csv')
df_comp = pd.read_csv(p).set_index('ID_MESA')
b_ = df_comp["CANDIDATURA"] == "PRESIDENTE"
df_comp = df_comp[b_]
co = ['VV', 'BL', 'NU', 'VOTO_EMITIDO','CREEMOS', 'MAS', 'FPV',
      'PAN_BOL', 'CC','NUA']
df_comp = df_comp[co]

df_comp['ID_RECI'] = (df_comp.index/100).astype(np.int64)
df_comp['COUNT'] = True


p = os.path.join(ebu.DATA_PATH1_2020,'z010R_geopadron_mesas_2020_ALL.csv')
df_all = pd.read_csv(p).set_index('ID_MESA')
#['ID_RECI', 'ID_MESA', 'HAB', 'INHAB']

df_all['VV'] = 0
df_all['COUNT'] = False

p = os.path.join(ebu.DATA_PATH1_2020,'z020_geopadron_recintos_2020_ALL_DEN.csv')
df_den = pd.read_csv(p).set_index('ID_RECI')
#['ID_RECI', 'LAT', 'LON', 'HAB', 'INHAB', 'PAIS', 'N_MESAS', 'REC',
# 'MUN', 'BOL', 'CIU', 'PROV', 'DEP', 'URB', 'DEN_C', 'DEN']

df_den = df_den[['LAT', 'LON', 'PAIS', 'N_MESAS', 'REC',
                 'MUN', 'BOL', 'CIU', 'PROV', 'DEP', 'URB', 'DEN_C', 'DEN']]

_s  = df_comp.index.isin(df_all.index)
assert (~_s).sum() == 0

b = ~df_all.index.isin(df_comp.index)
df_trim = df_all[b]
assert len(df_all) - len(df_comp) == len(df_trim)
df_concat = pd.concat([df_comp,df_trim])
df_full = df_concat.join(df_den,how='left',on='ID_RECI')
p = os.path.join(ebu.DATA_PATH1_2020,'z030_carto_xy.csv')
df_xy = pd.read_csv(p).set_index('ID_RECI')
df2 = df_full.join(df_xy,on='ID_RECI',how='left')
res = pd.cut(df2['DEN'],ebu.DEN_LIMS,labels=ebu.DEN_CODES)
df2['DEN_CODES'] = res.astype(int)
