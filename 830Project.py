import streamlit as st
import pandas as pd
from pandas import Series
from fredapi import Fred
import yfinance as yf
import altair as alt
from PIL import Image 

##################
# The title page #
##################
image =Image.open('title_image.jpg')
st.image(image, use_column_width=True)

st.write("""
# Inflation and  Stock Investment

This project will focus on the following topics:

1. CPI, S&P500 Index, and Nasdaq Composite.
1. Will investing in stock overcome the inflation?
2. Is there any relationship between Stcok maket and inflation?""")


st.markdown("""
### First, let's look at the CPI data 💸💸💸
A consumer price index (CPI) is a price index, the price of a weighted average market basket of consumer goods and services purchased by households. CPI track changes in prices over time.
[link](https://en.wikipedia.org/wiki/Consumer_price_index)

***
""")

#################
# load the data #
#################
fred_key = '5b4374b4423e4bc6a2bccd68c4684772'
fred = Fred(api_key=fred_key)
cpi = fred.get_series(series_id='CPIAUCSL')
cpi_df = pd.DataFrame({'Date':cpi.index,'Index':cpi.values}) 

#########################
# Plot the Raw CPI Data #
#########################
st.write("**CPI Raw Data From FRED API**")
cpi_chart = alt.Chart(cpi_df).mark_line().encode(
    x='Date',
    y='Index',
    color=alt.value("#FFAA00"),
    tooltip=['Index','Date']
).interactive().properties(
    width=600,
    height=300)

st.write(cpi_chart)

################################
# See the change of each month #
################################

Cindex = cpi_df['Index'] 
cdate = cpi_df['Date'].values[1:]
N = Cindex.size

change = Cindex[1:].values - Cindex[:N-1].values
changeData = Series(change, index=cdate)
cpi_month = pd.DataFrame({'Date':changeData.index,'Index':changeData.values})
#cpi_month is the change percentage of each month

######################################
# Plot the line of month change rate #
######################################
st.write("Change of each month")
cpi_monthc = alt.Chart(cpi_month).mark_line().encode(
    x='Date',
    y='Index',
    color=alt.value("#FFAA00"),
    tooltip=['Index','Date'],
    ).interactive().properties(
    width=600,
    height=300
)
st.write(cpi_monthc)

###############################
# Plot a Histgram of the data #
###############################
st.write("Histgram Showing Monthly CPI Changes")
hist = alt.Chart(cpi_month).mark_bar().encode(
    x='Index',
    y='count()',
    color=alt.value("#FFAA00")
    ).properties(
    width=600,
    height=300)
st.write(hist)

##############################################
# Describe() of the CPI data in unit of Year #
##############################################
st.markdown(""" 
***
#### Let's have a look of the CPI Yearly Change using `describe()` 
""")
cpiYear = cpi_month.groupby(cpi_month['Date'].dt.year).sum()
cpiDescribe = cpiYear.describe().T
st.write(cpiDescribe)

st.write("and the monthly change")
cpiMonthDescribe = cpi_month.describe().T
st.write(cpiMonthDescribe)

##########################
# Simple Summary for CPI #
##########################
st.write("""
**In last 76 years, the CPI increase about 3.6% every year. Which is about 0.3% increase every month**

* Feel free to interact with the plot and see for example CPI after 2008 finicial crisis
""")

#################
# Stock Section #
#################
st.write("""
***
### Now, let's have a look of the S&P500 and Nasdaq Composite 📈 or 📉
""")

st.markdown("""The Standard and Poor's 500, or simply the S&P 500, is a stock market index tracking the stock performance of 500 large companies listed on stock exchanges in the United States.
[link](https://en.wikipedia.org/wiki/S%26P_500)

The Nasdaq Composite (ticker symbol ^IXIC) is a stock market index that includes almost all stocks listed on the Nasdaq stock exchange. Along with the Dow Jones Industrial Average and S&P 500, it is one of the three most-followed stock market indices in the United States.
[link](https://en.wikipedia.org/wiki/Nasdaq_Composite)
""")
#load sp500 data
sp = yf.Ticker('^GSPC')
sp_df = sp.history(period='max')

#load nasdaq data
nq = yf.Ticker('^IXIC')
nq_df = nq.history(period='max')

#######################
# Plot Raw SP500 Data #
#######################
st.markdown("""#### SP500 Index""")
st.line_chart(sp_df['Close'])
st.write("You can see the circuit breaker in 2021, and current Bear market")

########################
# Plot Raw Nasdaq Data #
########################
st.markdown("""
***
#### Nasdaq Composite""")
st.line_chart(nq_df['Close'])

# sp500 daily closing #
st.write("SP500 Closing Percentage Chnage by day")
N = sp_df['Close'].size
#change = ((sp_df['Close'][1:].values / sp_df['Close'][:N-1].values) - 1)*100
change = (sp_df['Close'][1:].values - sp_df['Close'][:N-1].values)*100/sp_df['Close'][:N-1].values
changeData = Series(change, index=sp_df.index[1:])
sp_day = pd.DataFrame({'Date':changeData.index,'SP_Percent':changeData.values})

###########################
# Plot SP500 Daily Change #
###########################
sp_chart = alt.Chart(sp_day).mark_line().encode(
    y='SP_Percent',
    x='Date',
    color=alt.value("#FFAA00"),
    tooltip=['SP_Percent','Date'],
    ).interactive().properties(
    width=600,
    height=300)
st.write(sp_chart)

###############################
# Desribe SP500 Yearly Change #
###############################
spY = sp_day.groupby(sp_day['Date'].dt.year).sum()
spDescribe = spY.describe().T
st.write("Desribe SP500 Yearly Change")
st.write(spDescribe)

### nasdaq daily closing
st.markdown("""
***
Nasdaq Composite Closing Percentage Chnage by day
""")
N = nq_df['Close'].size
change = ((nq_df['Close'][1:].values / nq_df['Close'][:N-1].values) - 1)*100
changeData = Series(change, index=nq_df.index[1:])
nq_day = pd.DataFrame({'Date':changeData.index,'NQ_Percent':changeData.values})

############################
# Plot Nasdaq Daily Change #
############################
nq_chart = alt.Chart(nq_day).mark_line().encode(
    y='NQ_Percent',
    x='Date',
    color=alt.value("#FFAA00"),
    tooltip=['NQ_Percent','Date'],
    ).interactive().properties(
    width=600,
    height=300)
st.write(nq_chart)

################################
# Desribe Nasdaq Yearly Change #
################################
nqY = nq_day.groupby(nq_day['Date'].dt.year).sum()
nqDescribe = nqY.describe().T
st.write("Desribe Nasdaq Yearly Change")
st.write(nqDescribe)

#########################################
# Move on to combine CPI, SP500, Nasdaq #
#########################################
# Combine change together
#spM = sp_day.groupby(sp_day['Date'].dt.strftime('%Y-%m')).sum()
#nqM = nq_day.groupby(nq_day['Date'].dt.strftime('%Y-%m')).sum()
#cpiM = cpi_month['Index']
st.markdown("""
### Now, let put these data together 🥸
(using `pd.concat()`)
""")
combine = pd.concat([spY, nqY,cpiYear], axis=1, join='inner')
st.write(combine)
combineD = combine.describe().T
st.write(combineD)
#st.write("Compare Yearly Change")
#st.line_chart(data=combine)

# Acculmate change rate
sp_addup = sp_day['SP_Percent'].cumsum(axis=0)
nq_addup = nq_day['NQ_Percent'].cumsum(axis=0)


#st.line_chart(sp_addup)
st.write("SP&NQ")
addup_combine = pd.concat([sp_addup,nq_addup],axis=1, join='inner')
st.line_chart(addup_combine)
add_up_describe = addup_combine.describe().T
#st.write(add_up_describe)

# CPI change rate/year
cpi_df = pd.DataFrame({'Date':cpi.index,'cpi':cpi.values}) 
cpi_index = cpi_df['cpi']
cpi_date = cpi_df['Date'].values

cpi_date = cpi_date[1:] # this will return the date for your index 
N = cpi_index.size

change = cpi_index[1:].values - cpi_index[:N-1].values

changeData = Series(change, index=cdate)
cpi_month = pd.DataFrame({'Date':changeData.index,'cpi':changeData.values})

cpi_year = cpi_month.groupby(cpi_month['Date'].dt.year).sum()

cpiYear_rate = cpi_year/100
#cpiYear_rate

# SP500 change rate/year
N = sp_df['Close'].size

change = ((sp_df['Close'][1:].values / sp_df['Close'][:N-1].values) - 1)

changeData = Series(change, index=sp_df.index[1:])
sp_day = pd.DataFrame({'Date':changeData.index,'SP_Percent':changeData.values})

spYear = sp_day.groupby(sp_day['Date'].dt.year).sum()
spYear_rate = spYear
#spYear_rate
# NQ change rate/year
N = nq_df['Close'].size

change = ((nq_df['Close'][1:].values / nq_df['Close'][:N-1].values) - 1)

changeData = Series(change, index=nq_df.index[1:])
nq_day = pd.DataFrame({'Date':changeData.index,'NQ_Percent':changeData.values})
nqYear = nq_day.groupby(nq_day['Date'].dt.year).sum()
nqYear_rate = nqYear
#nqYear_rate

# combine in one df
dataframe = pd.concat([spYear_rate, nqYear_rate,cpiYear_rate], axis=1, join='outer')
df = dataframe.fillna(0)[0:73]
st.write("Change rate of SP, NQ, CPI over Years")
st.line_chart(df)
st.write(df.describe().T)

st.markdown("""
### Summary: 
* The Stock Market in long-term overcomes the inflation. SP500 is more stable than NQ
* When Inflation Increase, the stock market drop most time.
##### Tools:
* mainly used Pandas to cleaning and analyze the data
* I used Altair, and streamlit chart for visulation
##### Resources
* The data are from yfinance (Yahoo Finance) and [FRED](https://fred.stlouisfed.org) api

*** 
#### Thank You for Listening 😊
#### Yuhan Zhu 
#### Date: Oct. 2022
""")