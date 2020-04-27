#%% import modules

import os
import numpy as np
import scipy as sp
import pandas as pd
import random
import requests
from pdb import set_trace as pb
from func_timeout import func_timeout
from matplotlib import pyplot as plt
from urllib.request import urlopen

#%% import sentiment analysis and event studies

dataOutput = pd.read_csv('sentimentAnalysisAndEventStudies.csv')

#%% event studies

dataOutput.iloc[:,6:].describe()

#%% distribution in time

dataOutput.groupby('year').mean().iloc[:,3:6].plot()

dataOutput.groupby('year').mean().iloc[:,6:].plot()

#%% sort rudimentary sentiment analysis into quintiles

def upper_thresh_filter(obj, sort_variable, target_variable, q=0.80, stat='describe'):
    thresh = obj[sort_variable].quantile(q=q)
    return getattr(obj[obj[sort_variable] >= thresh][target_variable],stat)()

def lower_thresh_filter(obj, sort_variable, target_variable, q=0.20, stat='describe'):
    thresh = obj[sort_variable].quantile(q=q)
    return getattr(obj[obj[sort_variable] <= thresh][target_variable],stat)()

# car0

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'posWords','car0'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'posWords','car0'))
upperLowerMean = pd.DataFrame({'CAR(0) Upper Quintile':upper.iloc[:,1],'CAR(0) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

# car5

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'posWords','car5'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'posWords','car5'))
upperLowerMean = pd.DataFrame({'CAR(5) Upper Quintile':upper.iloc[:,1],'CAR(5) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

# cav0

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'posWords','cav0'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'posWords','cav0'))
upperLowerMean = pd.DataFrame({'CAV(0) Upper Quintile':upper.iloc[:,1],'CAV(0) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

# cav5

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'posWords','cav5'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'posWords','cav5'))
upperLowerMean = pd.DataFrame({'CAV(5) Upper Quintile':upper.iloc[:,1],'CAV(5) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

#%% sort advanced sentiment analysis into quintiles

def upper_thresh_filter(obj, sort_variable, target_variable, q=0.80, stat='describe'):
    thresh = obj[sort_variable].quantile(q=q)
    return getattr(obj[obj[sort_variable] >= thresh][target_variable],stat)()

def lower_thresh_filter(obj, sort_variable, target_variable, q=0.20, stat='describe'):
    thresh = obj[sort_variable].quantile(q=q)
    return getattr(obj[obj[sort_variable] <= thresh][target_variable],stat)()

# car0

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'nltkSentiment','car0'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'nltkSentiment','car0'))
upperLowerMean = pd.DataFrame({'CAR(0) Upper Quintile':upper.iloc[:,1],'CAR(0) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

# car5

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'nltkSentiment','car5'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'nltkSentiment','car5'))
upperLowerMean = pd.DataFrame({'CAR(5) Upper Quintile':upper.iloc[:,1],'CAR(5) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

# cav0

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'nltkSentiment','cav0'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'nltkSentiment','cav0'))
upperLowerMean = pd.DataFrame({'CAV(0) Upper Quintile':upper.iloc[:,1],'CAV(0) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

# cav5

upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'nltkSentiment','cav5'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'nltkSentiment','cav5'))
upperLowerMean = pd.DataFrame({'CAV(5) Upper Quintile':upper.iloc[:,1],'CAV(5) Lower Quintile': lower.iloc[:,1]})

upperLowerMean.plot()

#%% generate advanced sentiment analysis into quintiles

def upper_thresh_filter(obj, sort_variable, target_variable, q=0.80, stat='describe'):
    thresh = obj[sort_variable].quantile(q=q)
    return getattr(obj[obj[sort_variable] >= thresh][target_variable],stat)()

# car5
upper = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'nltkSentiment','car5'))
lower = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'nltkSentiment','car5'))

meanUpper = ( upper['count'] * upper['mean'] ).sum() / upper['count'].sum()
meanLower = ( lower['count'] * lower['mean'] ).sum() / lower['count'].sum()

stdUpper = ( upper['count'] * upper['std'] ).sum() / upper['count'].sum()
stdLower = ( lower['count'] * lower['std'] ).sum() / lower['count'].sum()

# cav5

upperCAV = dataOutput.groupby('year').apply(lambda x: upper_thresh_filter(x,'nltkSentiment','cav5'))
lowerCAV = dataOutput.groupby('year').apply(lambda x: lower_thresh_filter(x,'nltkSentiment','cav5'))

meanUpperCAV = ( upperCAV['count'] * upperCAV['mean'] ).sum() / upperCAV['count'].sum()
meanLowerCAV = ( lowerCAV['count'] * lowerCAV['mean'] ).sum() / lowerCAV['count'].sum()

stdUpperCAV = ( upperCAV['count'] * upperCAV['std'] ).sum() / upperCAV['count'].sum()
stdLowerCAV = ( lowerCAV['count'] * lowerCAV['std'] ).sum() / lowerCAV['count'].sum()