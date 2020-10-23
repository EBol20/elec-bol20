#%%
import elec_bol20.util as ebu
from elec_bol20 import *


df20 = ebu.get_dataframe_2020()
df19 = ebu.open_combine_2019()
df = pd.merge(
    df19, df20, left_on='ID_MESA', right_on='ID_MESA',
    suffixes=['_19', '_20'],
    how='outer'
)

print(len(df))
print(len(df20))
print(len(df19))

df.to_csv(os.path.join(ebu.DATA_PATH1_2020,'z110_concat_19_20.csv'))