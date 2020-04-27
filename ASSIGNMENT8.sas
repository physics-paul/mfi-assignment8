/* SAS DATA WRANGLING */
/* MFI ASSIGNMENT #8  */

/********************************************/
/* WRANGLE DSF                              */
/********************************************/

libname path "C:\Users\psanders8\Documents\SASDATASETS"; /* fill with your path */

%let VARIABLES = PRC CUSIP DATE RET VOL SHROUT;

DATA DSF_WRANGLED;
	SET path.dsf(keep = &VARIABLES);
	IF CMISS(of _all_) then DELETE;
	IF RET ^= 0;
	YEAR = YEAR(DATE);
	IF 1993 <= YEAR <= 2018;
	IF SHROUT > 0;
	SHROUT = SHROUT*1000;
	PRC = ABS(PRC);
	VALUE = SHROUT*PRC;
	TURNOVER = VOL / SHROUT + 0.0000001;
	DROP YEAR VOL PRC SHROUT;
RUN;

/********************************************/
/* WRANGLE FUNDA                            */
/********************************************/

libname path "C:\Users\psanders8\Documents\SASDATASETS"; /* fill with your path */

%let VARIABLES = CUSIP CIK INDFMT DATAFMT POPSRC CONSOL;

DATA FUNDA_WRANGLED;
	set path.FUNDA(keep = &variables);
	if INDFMT = 'INDL' and DATAFMT = 'STD' and POPSRC = 'D' and CONSOL = 'C';
	CUSIP = SUBSTRN(CUSIP,1,8);
	DROP INDFMT DATAFMT POPSRC CONSOL;
	if CMISS(of _all_) THEN DELETE;
RUN;

/********************************************/
/* MERGE FUNDA WITH DSF ON CUSIP            */
/********************************************/
	
PROC SORT data=DSF_WRANGLED; BY CUSIP; RUN;
PROC SORT data=FUNDA_WRANGLED; BY CUSIP; RUN;
	
DATA DSF_FUNDA;
	MERGE DSF_WRANGLED(in=A KEEP=CUSIP DATE RET VALUE TURNOVER)
		FUNDA_WRANGLED(in=B)
		;
		BY CUSIP;
		IF A AND B;
	DROP CUSIP;
RUN;

PROC SORT data=DSF_FUNDA; BY DATE CIK; RUN;

PROC DELETE data=DSF_WRANGLED;
RUN;

PROC DELETE data=FUNDA_WRANGLED;
RUN;

/********************************************/
/* EXPORT TO CSV                            */
/********************************************/

PROC EXPORT DATA = DSF_FUNDA OUTFILE = "C:\Users\psanders8\Documents\SASDATASETS\dsf_funda.csv" dbms = csv replace;
RUN;
