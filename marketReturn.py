#%% 8.0 get modules

import os
import gc
import numpy as np
import scipy as sp
import pandas as pd
import random
import requests
from pdb import set_trace as pb
from func_timeout import func_timeout
from matplotlib import pyplot as plt
from urllib.request import urlopen

#%% import DSF and FUNDA data

dataDsfFunda = pd.read_csv('dsf_funda.csv',parse_dates=["DATE"])

dataDsfFunda['TOTALRETURN'] = dataDsfFunda['RET'] * dataDsfFunda['VALUE']

allUniqueDates = dataDsfFunda['DATE'].unique()

#%% get the market return values

print(" Grabbing the Value-Weighted Market Returns")

mkTReturn = np.zeros(allUniqueDates.shape[0])

for index,date in enumerate(allUniqueDates):

    dateInRange = dataDsfFunda.index[dataDsfFunda['DATE'] == date].tolist()
    returns = dataDsfFunda['TOTALRETURN'].iloc[dateInRange].sum()
    weight = dataDsfFunda['VALUE'].iloc[dateInRange].sum()
    mkTReturn[index] = returns / weight

# join the value-weighted returns with the date

mkTReturns = pd.DataFrame({"DATE":allUniqueDates,"MKTRETURN":mkTReturn})

mkTReturns.to_csv("marketReturns.csv", index=False)

######################################################