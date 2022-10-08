import pickle

with open('jobs_dict.pickle','rb') as f:
    dict = pickle.load(f)

len(dict)

import pandas as pd

pd.DataFrame(dict).transpose()