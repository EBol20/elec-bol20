import sys
sys.path.append(".")
from elec_bol20 import *
import elec_bol20.util as ebu
import elec_bol20.tools as ebt


#df0 = ebu.open_combine_2019()
df0 = ebu.get_dataframe_2020()
z = ebt.CartoPlots()
y = z.load_file(df0, _mean=['X', 'Y', 'LAT', 'LON', 'DEN', ], _sum=['HAB', 'CC', 'MAS','CREEMOS', 'FPV','PAN_BOL','VV'],
                _first=['PAIS', 'REC', 'MUN', 'BOL'])
x1 = z.plot_carto_single(y, 'diff', ebu.P_DIF, name_file='test2020.html', low=0, high=100)
x2 = z.plot_carto_single(y, 'mas', ebu.P_GRAD_MAS, name_file='test2020.html', low=0, high=100)
x3 = z.plot_carto_single(y, 'cc', ebu.P_GRAD_CC, name_file='test2020.html', low=0, high=100)
x4 = z.plot_carto_single(y, 'creemos', ebu.P_GRAD_CREEMOS, name_file='test2020.html', low=0, high=100)
x5 = z.plot_carto_single(y, 'pan_bol', ebu.P_GRAD_PANBOL, name_file='test2020.html', low=0, high=100)
x6 = z.plot_carto_single(y, 'fpv', ebu.P_GRAD_FPV, name_file='test2020.html', low=0, high=100)
