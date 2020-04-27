## ASSIGNMENT 8: Event Studies and Sentiment Analysis using Python

This project seeks to analyze the sentiment of 8-Ks for each year-quarter from the SEC webite from 1995-2018. The goal is to see if any correlation exists between the sentiment, or tone, of the 8-K and the subsequent abnormal trading volume or abnormal returns around the actual event date. This task is divided into three parts: 1. Downloading the Data, 2. Event Studies, 3. Rudimentary Sentiment Analysis, and 4. Advanced Sentiment Analysis. 

### 1. Downloading the Data

There were a few main sources of data used for this project:

  a. 8-K Texts : This was downloaded from the SEC webside, and all 8-Ks starting from 1995 Q1 to 2018 Q4 was obtained, and each company was labeled by their unique CIK number. For each quarter, 100 random 8-K's were selected to analyze. This results in over 9500+ documents to analyze.
  
  b. DSF : The daily stock returns and volume, along with shares outstanding, were obtained by analyzing the DSF SAS file which was obtained through the QCF server. This data file had company information in the form of the CUSIP number.
  
  c. FUNDA : This company-specific data information file contained the link between CUSIP and the CIK number, which was used to relate the 8-K texts to the DSF data file. This document was found as well through the QCF server.
  
  d. Bill McDonald's Word List : This data file assigned a positive and negative value to each word, and it was used to determine the overall tone in the rudimentary sentiment analysis.
  
In actually downloading the data, Python was used for the data extraction to grab the information from each URL, specifically using the 'requests' module. Since each of the 8-K's was in the form of an html script, the module 'Beautiful Soup' was used in order to parse through the html and only grab the body of the document.

The Python script can be seen in the GitHub pages as 'sentimentAnalysis.py'. It was put here because the code runs more smoothly to go ahead an perform the Sentiment Analysis in the next sections while downloading the data.

### Event Studies

This task sought to look at the CIK and filing date pair from the previous section to determine the cumulative abnormal return (CAR) and cumulative abnormal volume (CAV) for each CIK/filing date pair. The abnormal return (AR) is defined as the return in excess of the CAPM market return, regressed from -315 to -91 days from the event or filing date. The 'cumulative' part of the definition arises from summing the rolling window of abnormal returns around the event date. For instance, the three-day window consists of the day prior to the event date, the event date, and the day after the event date. The one-day, three-day, and five-day rolling window was calculated for both CAR and CAV.

$$\log \sum{1}$$

We can define the CAV as the normalized trading volume, calibrated to -115 to -91 days before the event date and taken on a log scale. For clarification, suppose the range of -115 to -91 days was not quite a volatile range of trading, while the cumulative three-day rolling window around the event date was very volatile, then the CAV would be a large number, scaled by a standard deviation or more from the mean of the past -115 to -91 day rolling window.

The table below shows the descriptive statistics for the CAR and CAV rolling windows over the sample period.

Additionally we can plot the distribution of both measures, given by:

This Python script can be seen in the GitHub pages as 'eventStudies.py'. Be cautioned though, this code takes around ~1hr to run, because of the intensive process in calculating the CAV and CAR for each event study. 

This code produces the final 'sentimentAnalysisAndEventStudies.csv' data file to obtain all information for each event study.

### Rudimentary Sentiment Analysis

The main task for this section was to compute the abnormal stock returns and abnormal trading volume around 8-K filings, and study how these measure vary depending on the number of positive and negative words included in the filing.

In obtaining the positivity and negativity of the document, these results can be sorted into quintiles. If we calculate the descriptive statistics for the CAR and CAV in the highest vs. lowest percentile, we obtain the following table:

This Python script can be seen in the GitHub pages as 'sentimentAnalysis.py', and is combined with the section below.

### Advanced Sentiment Analysis

In this section, a more thorough analysis of the 'tone' of the 8-K is performed by looking at the tonality of each sentence in the document, rather than merely counting positive and negative words. The natural language toolkit provided by the 'NLTK' module in Python was an excellent resource to complete this task.

The first thing to notice in this section is difficult in cleaning up an html file. Even with the best tools, it can sill be an imprecise tool. However, how I went about this task was to clean the html string in a series of steps:

1. Use the 'BeautifulSoup' module to remove all white spaces in the document and only extract the body of the html file.
2. Use the 'RegexpTokenAnalyzer' function in the NLTK toolkit to grab only words and words which ended with a standard sentence ending (.!?).
3. Use the 'sent_tokenize' function in the NLTK toolkit to split the string into sentences.
4. Assign a tonality to each sentence by the ' ' function in the NLTK toolkit to analyze the tonality of each sentence.
5. Sum up the overall tonality and divide by the total number of sentences to grab the offical 'tone' of the 8-K.

After this, it was relatively easy to sort the 8-K documents into quintiles and generate the descriptive statistics for the upper and lower quintile. The result is:


This Python script can be seen in the GitHub pages as 'sentimentAnalysis.py'. Be cautioned though, this code takes around ~1hr to run, due to the time-intensive process of analyzing each 8-K.

This code produces the 'sentimentAnalysis.csv' data file, which is used by the 'eventStudies.py' script in order to obtain the final output.
