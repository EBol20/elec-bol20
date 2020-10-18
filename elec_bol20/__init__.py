# project name: prototipo_elecciones_bol2019
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# load and autoreload
from IPython import get_ipython

# noinspection PyBroadException
try:
    _ipython = get_ipython()
    _magic = _ipython.magic
    _magic('load_ext autoreload')
    _magic('autoreload 2')
except:
    pass


import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import os
import pandas as pd
import matplotlib
import matplotlib.colors
# import holoviews
import bokeh
import bokeh.models
import bokeh.plotting
import bokeh.palettes
import bokeh.colors
import bokeh.palettes
import seaborn as sns
import matplotlib