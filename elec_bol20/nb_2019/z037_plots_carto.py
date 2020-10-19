import sys
sys.path.append(".")
#from elec_bol20 import *
import elec_bol20 as eb
import elec_bol20.util as ebu
import elec_bol20.tools as ebt
import os

#df0 = ebu.open_combine_2019()
df0 = ebu.get_dataframe_2020()
z = ebt.CartoPlots()
y = z.load_file(df0, _mean=['X', 'Y', 'LAT', 'LON', 'DEN', ], _sum=['HAB', 'CC', 'MAS','CREEMOS', 'FPV','PAN_BOL','VV'],
                _first=['PAIS', 'REC', 'MUN', 'BOL'])
# stamp Bolivian time at the moment of plotting
bot_time = ebu.get_bolivian_time(-3)["str_val"]
#print(bot_time)

goal_dir = os.path.join(ebu.DIR)

#par dir ya esta en elec-bol20
par_dir = os.path.pardir(goal_dir)


#path_cart_maps=os.path.join(os.getcwd().,"../../carto_maps")
#print(path_cart_maps)
#
# x1 = z.plot_carto_single(y, 'diff', ebu.P_DIF,path=path_cart_maps, name_file=bot_time, low=0, high=100, show_plot=False)
# x2 = z.plot_carto_single(y, 'mas', ebu.P_GRAD_MAS,path=path_cart_maps, name_file=bot_time, low=0, high=100, show_plot=False)
# x3 = z.plot_carto_single(y, 'cc', ebu.P_GRAD_CC, path=path_cart_maps, name_file=bot_time, low=0, high=100, show_plot=False)
# x4 = z.plot_carto_single(y, 'creemos', ebu.P_GRAD_CREEMOS, path=path_cart_maps, name_file=bot_time, low=0, high=100, show_plot=False)
# x5 = z.plot_carto_single(y, 'pan_bol', ebu.P_GRAD_PANBOL, path=path_cart_maps, name_file=bot_time, low=0, high=100, show_plot=False)
# x6 = z.plot_carto_single(y, 'fpv', ebu.P_GRAD_FPV, path=path_cart_maps, name_file=bot_time, low=0, high=100, show_plot=False)

x1 = z.plot_carto_single(y, 'diff', ebu.P_DIF, name_file=bot_time, low=0, high=100)
x2 = z.plot_carto_single(y, 'mas', ebu.P_GRAD_MAS, name_file=bot_time, low=0, high=100)
x3 = z.plot_carto_single(y, 'cc', ebu.P_GRAD_CC, name_file=bot_time, low=0, high=100)
x4 = z.plot_carto_single(y, 'creemos', ebu.P_GRAD_CREEMOS, name_file=bot_time, low=0, high=100)
x5 = z.plot_carto_single(y, 'pan_bol', ebu.P_GRAD_PANBOL, name_file=bot_time, low=0, high=100)
x6 = z.plot_carto_single(y, 'fpv', ebu.P_GRAD_FPV, name_file=bot_time, low=0, high=100)
