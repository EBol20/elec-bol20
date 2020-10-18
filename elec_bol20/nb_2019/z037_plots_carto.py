import sys
sys.path.append(".")
from elec_bol20 import *
import elec_bol20.util as ebu
from z036_crear_carto_grandeV3_class import CartoPlots

df0 = ebu.open_combine_2019()
z = CartoPlots()
y = z.load_file(df0)
x = z.plot_cart(y)
