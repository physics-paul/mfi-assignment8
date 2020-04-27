#%% 8.0 get modules

import os
import numpy as np
import scipy as sp
import pandas as pd
import random
import requests
from func_timeout import func_timeout
from matplotlib import pyplot as plt
from urllib.request import urlopen
from pdb import set_trace as pb
from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize,sent_tokenize
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#%% 8.1 get word list from mcdonald's words

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                
file_id = '12ECPJMxV2wSalXG8ykMmkpa1fq_ur0Rf'
destination ="wordset/mcdonaldwords.csv"
download_file_from_google_drive(file_id, destination)

path = "wordset/"
worddata = pd.read_csv(path+"mcdonaldwords.csv")

worddata['Word'] = worddata['Word'].str.lower()

# get the positive and negative words

pos = worddata[worddata['Positive'] != 0]['Word'].values
neg = worddata[worddata['Negative'] != 0]['Word'].values

# initialize the positive to negative word analysis

tkBadData = RegexpTokenizer(r"([A-Za-z]{3,}\b\.|[A-Za-z]{3,}\b)")

# initialize the nltk advanced sentiment analysis

sid = SentimentIntensityAnalyzer()

#%% 8.2 download 100 random 8-K's from 1995:Q1-2018:Q4

# number of files to download each quarter

nRandom = 100

# get sec data urls 

startYear = 1995
endYear = 2018

years  = list(range(startYear,endYear+1))
months = ["QTR1","QTR2","QTR3","QTR4"]

secUrl = "https://www.sec.gov/Archives/"

# the masterUrl contains a list of all urls needed for analysis

masterUrl = [secUrl + "edgar/full-index/{0}/{1}/master.idx".format(yr,mn) \
            for yr in years for mn in months]

# create an empty pandas dataframe to store the CIK, DATE, and SENTIMENT ANALYSIS information

column_names = ["year","quarter","date","cik","posWords","nltkSentiment"]

eightKData = pd.DataFrame(columns = column_names)

# search through the master list, where the master list contains the
# directory for all 8-k's in each quarter

for allFileList in masterUrl: # only grab 1-q for analysis
    
    # grab the year and quarter of the 'allFileList'
    
    year = int(allFileList.split("/")[-3])
    quarter = allFileList.split("/")[-2]
    
    # extract the data from the websites
    
    file = urlopen(allFileList)
    file = file.read().decode('iso8859_15')
    
    fileLines = np.array(file.split("\n")[11:])
    fileLines = fileLines[["8-K" in line for line in fileLines]]

    # randomly grab 10 8-k's
    
    firms = np.random.choice(fileLines.shape[0], size=nRandom, replace=False)
    firms = np.array(fileLines[firms])
    
    # grab url's for 8-k's
    
    firmSite = np.array([line.split("|")[-1] for line in firms])
    sites = list(map(lambda x: secUrl+x, firmSite))
    
    # grab cik and dates for 8-k firms
    
    firmCik = [line.split("|")[0] for line in firms]
    firmDate = [line.split("|")[3] for line in firms]

    ###############################################################

    number8K = 0

    posWords = []

    tones = []

    cik = []

    date = []

    for index,geturl in enumerate(sites):
    
        # grab 8-k data, labelling the files by cik and date

        try:

            fileOpen = urlopen(geturl)
    
            fileTextData = func_timeout(3.0,fileOpen.read().decode,['iso8859_15'])
    
        except:

            continue

        # strip the data using BeautifulSoup

        try:

            tree = func_timeout(3.0,BeautifulSoup,[fileTextData,'lxml'])

        except:

            continue

        body = tree.body
    
        # grab all text

        htmlStripped = body.get_text(strip=True).lower()

        # get rid of tab, and newline commands

        htmlStripped = " ".join(htmlStripped.split())

        # get rid of any trash data

        htmlStripped = " ".join(tkBadData.tokenize(htmlStripped))

        # get the words in the information section

        fileWords = np.array(word_tokenize(htmlStripped))

        # consider 8-K's with a little substance

        if len(fileWords) < 100:

            continue

        # get the positive to negative words

        posWord = np.in1d(fileWords,pos).sum()
        negWord = np.in1d(fileWords,neg).sum()

        posWords.append( (posWord - negWord) / len(fileWords) )

        # get the sentences in the nltk analysis

        fileSentences = np.array(sent_tokenize(htmlStripped))

        # run the nltk advanced sentiment analysis

        tone = 0

        for sent in fileSentences:

            tone += sid.polarity_scores(sent)['compound']

        tones.append( tone / len(fileSentences) )

        number8K += 1

        cik.append(firmCik[index])

        date.append(firmDate[index])

    # create a numpy array to store cik, date, site information 
    # for every quarter to be used to append to the main 
    # pandas dataframe

    yearList = np.array([year]*number8K, dtype=float)
    quarterList = np.array([quarter]*number8K, dtype=str)
    
    addEightKData = np.array([yearList,quarterList,date,cik,tones,posWords]).T
    addEightKData = pd.DataFrame(addEightKData,columns=column_names)
    
    eightKData = eightKData.append(addEightKData,ignore_index=True)

    print("{} {} complete".format(year,quarter))

eightKData.to_csv("sentimentAnalysis.csv", index=False)

############################################################
