## ASSIGNMENT 8: Event Studies and Sentiment Analysis using Python

This project seeks to analyze the sentiment of 8-Ks for each year-quarter from the SEC webite from 1995-2018. The goal is to see if any correlation exists between the sentiment, or tone, of the 8-K and the subsequent abnormal trading volume or abnormal returns around the actual event date. This task is divided into three parts: 1. Downloading the Data, 2. Event Studies, 3. Rudimentary Sentiment Analysis, and 4. Advanced Sentiment Analysis. 

### 1. Downloading the Data

There were a few main sources of data used for this project:

  a. 8-K Texts : This was downloaded from the SEC webside, and all 8-Ks starting from 1995 Q1 to 2018 Q4 was obtained, and each company was labeled by their unique CIK number. For each quarter, 100 random 8-K's were selected to analyze. This results in over 9500+ documents to analyze.
  b. DSF : The daily stock returns and volume, along with shares outstanding, were obtained by analyzing the DSF SAS file which was obtained through the QCF server. This data file had company information in the form of the CUSIP number.
  c. FUNDA : This company-specific data information file contained the link between CUSIP and the CIK number, which was used to relate the 8-K texts to the DSF data file. This document was found as well through the QCF server.
  d. Bill McDonald's Word List : This data file assigned a positive and negative value to each word, and it was used to determine the overall tone in the rudimentary sentiment analysis.
  
In actually downloading the data, I used Python for this section to grab the information from each URL and extract the text from the file using the module 'Beautiful Soup'.



### Event Studies



### Rudimentary Sentiment Analysis
