import sys
sys.path.append(".")
from elec_bol20 import *
import elec_bol20.util as ebu
import elec_bol20.tools as eto

df0 = ebu.open_combine_2019()
z = eto.CartoPlots()
y = z.load_file(df0)

x = z.plot_carto_single(y, 'diff', ebu.P_DIF, name_file='test0.html', low=0, high=100)
x = z.plot_carto_single(y, 'cc', ebu.P_GRAD_CC, name_file='test0.html', low=0, high=100)
x = z.plot_carto_single(y, 'mas', ebu.P_GRAD_MAS, name_file='test0.html', low=0, high=100)

