from elec_bol20 import *
import geopandas as gp
import elec_bol20.util as ebu

VV = 'VV'
COUNT = 'COUNT'
VAL = 'MAS'
PC = 'P_COMP'


def predict_p(df, p):
    df = simple_split(df, p)
    # %%
    p1 = (df[COUNT] == True).sum() / len(df) * 100
    p2 = (df[COUNT] == False).sum() / len(df) * 100
    p1, p2
    # %%
    return ebu.single_pred(df=df, var=VAL, pred_mask=COUNT)


def simple_split(df, p):
    df.loc[df[PC] <= p, COUNT] = True
    df.loc[df[PC] > p, COUNT] = False
    return df


def get_counted(df):
    return df[df[COUNT]]


def get_not_counted(df):
    return df[~df[COUNT]]

def get_coverage(df, buffer=.5):
    buf = df.buffer(buffer, resolution=2)
    res = buf.unary_union
    return res

def add_point(df):
    # global gf
    gf = gp.GeoDataFrame(df)
    gf = gf.set_geometry(gp.points_from_xy(gf['X'], gf['Y']))
    return gf