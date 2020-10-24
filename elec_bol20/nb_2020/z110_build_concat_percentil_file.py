# %%
import elec_bol20.util as ebu
from elec_bol20 import *
import glob

# %%
#### cons
CAN_OPEN = 'CAN_OPEN'
TIMESTAMP = 'TIMESTAMP'
POS = 'POS'
FILE = 'FILE'
ID_MESA = 'ID_MESA'
path = os.path.join(ebu.DATA_PATH1_2020, 'comp')
files = glob.glob(os.path.join(path, '*_*_*_*.csv'))


# %%
#### funs

def open_df(p1):
    n1 = os.path.basename(p1)
    # name2 = os.path.basename(p2)

    d1 = pd.read_csv(p1). \
        set_index(ID_MESA)
    if 'X' in d1.columns:
        d1 = d1.drop(columns=['X'])
    d1 = d1[d1['CANDIDATURA'] == 'PRESIDENTE']

    len_ = d1.index.astype(str).str.len() == 18
    _sum = (~len_).sum()
    if _sum >0:
        print('warning some index not equal 0',_sum)

    d1 = d1[len_]

    d1.index = d1.index.astype(np.int64)

    # d2 = pd.read_csv(p2). \
    #     set_index(ID_MESA).drop(columns=['X'])
    # d2 = d2[d2['CANDIDATURA'] == 'PRESIDENTE']

    assert d1.index.duplicated().sum() == 0
    # assert d2.index.duplicated().sum() == 0
    return d1, n1


def df_concat(*, d1, d2, n1, n2):
    isin = d2.index.isin(d1.index)
    d2_in_1 = d2[isin].index
    d2_not_in_1 = d2[~isin].index

    l1 = len(d1)
    l2 = len(d2)
    print('len d1', l1)
    print('len d2', l2)
    print('l2-l1', l2 - l1)

    l2_not_in_1 = len(d2_not_in_1)
    print('len d2 not in d1', l2_not_in_1)
    print('len d2', l2)

    if l2 - l1 is not l2_not_in_1:
        print('warning')
    equal = d2.loc[d2_in_1].equals(d1.loc[d2_in_1])
    if not equal:
        print('warning','not equal')

    d2n = d2.loc[d2_not_in_1]
    d1n = d1.loc[d2_in_1]

    # import datetime as dt

    _format = '%Y%m%d_%H%M%S'
    dat1 = pd.to_datetime(n1[-19:-4], format=_format)
    dat2 = pd.to_datetime(n2[-19:-4], format=_format)

    if TIMESTAMP not in d2n.columns:
        d2n[TIMESTAMP] = dat2
    d1n[TIMESTAMP] = dat1

    concat_d = pd.concat([d1n, d2n])
    return concat_d


def _try_open(p):
    try:
        pd.read_csv(p)
        return True
    except:
        return False


# %%
### code

# %%
df = pd.DataFrame(files, columns=[FILE])
df = df.sort_values(FILE)
df = df.reset_index(drop=True)
df.index.name = POS

# %%

df[CAN_OPEN] = df[FILE].apply(_try_open)

# %%
df1 = df[df[CAN_OPEN]]
# %%
df1 = df1.sort_values(FILE)
df_reversed = df1[::-1]
l = len(df_reversed)

d2, n2 = open_df(df_reversed.iloc[0][FILE])
for i in range(l - 1):
    p1 = df_reversed.iloc[i + 1][FILE]
    print(p1)
    d1, n1 = open_df(p1)
    d2 = df_concat(d1=d1, d2=d2, n1=n1, n2=n2)
    n2 = n1

# %%

d3 = d2.sort_values(TIMESTAMP)

tot_hab = d3['HAB'].sum()

d3['P_COMP']=d3['HAB'].cumsum()/tot_hab*100

d3.to_csv(ebu.FULL_COMP_CONCAT_CSV)

#%%

#%%
