#%% 8.0 get modules

import os
import numpy as np
import scipy as sp
import pandas as pd
import random
import requests
import statsmodels.api as sm
from pdb import set_trace as pb
from func_timeout import func_timeout
from matplotlib import pyplot as plt
from urllib.request import urlopen

############################################################

#%% grab the sentiment analysis data

print(" Completing the Sentiment Analysis")

path = "/home/paul/Documents/COURSEWORK/FIRST SEMESTER/MANAGEMENT OF" \
    " FINANCIAL INSTITUTIONS/ASSIGNMENT8/"

columnNames = ["year","quarter","date","cik","posWords","nltkSentiment"]

dType = {'year': int, 'quarter': str, 'cik': int, 'posWords': float, 'nltkSentiment': float}

dataSentiment = pd.read_csv(path+'sentimentAnalysis.csv', parse_dates=['date'], dtype=dType)

dataSentiment = dataSentiment[columnNames].sort_values(by=['date','cik'])

dataSentiment = dataSentiment.reset_index(drop=True)

#%% grab the dsf and funda data

print(" Grabbing the DSF and FUNDA Data")

dataDsfFunda = pd.read_csv('dsf_funda.csv',parse_dates=["DATE"])

dataDsfFunda['TOTALRETURN'] = dataDsfFunda['RET'] * dataDsfFunda['VALUE']

#%% grab the total market return

print(" Grabbing the Total Market Return")

mkTReturn = pd.read_csv('marketReturns.csv',parse_dates=['DATE'])

#%% run a for loop over all dataSentiment dates to grab car and cav rolling window

print(" Calculating the CAR and CAV")

car = np.zeros((dataSentiment.shape[0],3))
cav = np.zeros((dataSentiment.shape[0],3))

for index,value in dataSentiment.iterrows():

    # get unusual returns CAR

    # run the regression for alpha and beta

    firstDateRegress = value['date'] + pd.DateOffset(days=-345)
    secondDateRegress = value['date'] + pd.DateOffset(days=-91)

    dataDSFIndexPAST = (dataDsfFunda['DATE'] >= firstDateRegress) \
        & (dataDsfFunda['DATE'] <= secondDateRegress) \
        & (dataDsfFunda['CIK'] == value['cik'])
        
    datesPAST = dataDsfFunda['DATE'][dataDSFIndexPAST]

    if datesPAST.shape[0] <= 20:

        car[index] = "NaN"

        cav[index] = "NaN"

        continue

    pastCIKReturns = dataDsfFunda['RET'][dataDSFIndexPAST].values

    pastMKTReturns = mkTReturn['MKTRETURN'][mkTReturn['DATE'].isin(datesPAST)].values
    
    pastMKTReturns = sm.add_constant(pastMKTReturns)

    model = sm.OLS(pastCIKReturns,pastMKTReturns)

    parms = model.fit().params

    alpha = parms[0]

    beta = parms[1]

    # calculate the CAR (-5,+5) date window

    carMinusFive = value['date'] + pd.DateOffset(days=-5)
    carPlusFive = value['date'] + pd.DateOffset(days=+5)

    dataDSFIndexWINDOW = (dataDsfFunda['DATE'] >= carMinusFive) \
        & (dataDsfFunda['DATE'] <= carPlusFive) \
        & (dataDsfFunda['CIK'] == value['cik'])
        
    datesWINDOW = dataDsfFunda['DATE'][dataDSFIndexWINDOW]

    if datesWINDOW.shape[0] <= 1:

        car[index] = "NaN"

        cav[index] = "NaN"

        continue

    windowCIKReturns = dataDsfFunda['RET'][dataDSFIndexWINDOW].values

    windowMKTReturns = mkTReturn['MKTRETURN'][mkTReturn['DATE'].isin(datesWINDOW)].values

    carVals =  windowCIKReturns - (parms[0] + parms[1]*windowMKTReturns)

    # calculate three windows: 0, and +-1, and +-5

    midIndex = int(0.5*carVals.shape[0])

    car[index] = [carVals[midIndex].sum(),carVals[midIndex-1:midIndex+2].sum(),carVals.sum()]
        
    # get unusual returns CAV

    firstDateCAV = value['date'] + pd.DateOffset(days=-71)
    secondDateCAV = value['date'] + pd.DateOffset(days=-11)

    dataDSFIndexPAST = (dataDsfFunda['DATE'] >= firstDateCAV) \
        & (dataDsfFunda['DATE'] <= secondDateCAV) \
        & (dataDsfFunda['CIK'] == value['cik'])

    pastCIKTurnover = np.log(dataDsfFunda['TURNOVER'][dataDSFIndexPAST].values)
    pastCIKTurnoverMean = pastCIKTurnover.mean()
    pastCIKTurnoverStd = pastCIKTurnover.std()

    # calculate the CAV (-5,+5) date window

    cavMinusFive = value['date'] + pd.DateOffset(days=-5)
    cavPlusFive = value['date'] + pd.DateOffset(days=+5)

    windowCIKTurnover = np.log(dataDsfFunda['TURNOVER'][dataDSFIndexWINDOW].values)
    
    cavVals = (windowCIKTurnover - pastCIKTurnoverMean) / pastCIKTurnoverStd  

    # calculate three windows: 0, and +-1, and +-5

    midIndex = int(0.5*cavVals.shape[0])

    cav[index] = [cavVals[midIndex].sum(),cavVals[midIndex-1:midIndex+2].sum(),cavVals.sum()]
 
    print(index)
    
dataSentiment['car0'],dataSentiment['car1'],dataSentiment['car5'] = car.T
dataSentiment['cav0'],dataSentiment['cav1'],dataSentiment['cav5'] = cav.T

dataSentiment.to_csv("sentimentAnalysisAndEventStudies.csv", index=False)

print(" CAR and CAV calculation complete")

####################################################