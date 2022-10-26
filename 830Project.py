import streamlit as st
import pandas as pd
from pandas import Series
from fredapi import Fred
import yfinance as yf
import altair as alt
from PIL import Image 


image =Image.open('title_image.jpg')
st.image(image, use_column_width=True)

st.write("""
# Inflation and  Stock Investment

This project will focus on the following topics:

1. CPI, S&P500 Index, and Nasdaq Composite.
1. Will investing in stock overcome the inflation?
2. Is there any relationship between Stcok maket and inflation?

***

### First, let's loog at the CPI data 💸💸💸
""")

# load the data
fred_key = '5b4374b4423e4bc6a2bccd68c4684772'
fred = Fred(api_key=fred_key)
cpi = fred.get_series(series_id='CPIAUCSL')
cpi_df = pd.DataFrame({'Date':cpi.index,'Index':cpi.values}) 

st.write("CPI Raw Data")
cpi_chart = alt.Chart(cpi_df).mark_line().encode(
    x='Date',
    y='Index',
    color=alt.value("#FFAA00"),
    tooltip=['Index','Date']
).interactive()

st.write(cpi_chart)


# See the change of each month

Cindex = cpi_df['Index']
cdate = cpi_df['Date'].values[1:]
N = Cindex.size

change = Cindex[1:].values - Cindex[:N-1].values
changeData = Series(change, index=cdate)
cpi_month = pd.DataFrame({'Date':changeData.index,'Index':changeData.values})


st.write("Change of each month")
cpi_monthc = alt.Chart(cpi_month).mark_line().encode(
    x='Date',
    y='Index',
    color=alt.value("#FFAA00"),
    tooltip=['Index','Date'],
    ).interactive()
st.write(cpi_monthc)


st.write("Histgram")
hist = alt.Chart(cpi_month).mark_bar().encode(
    x='Index',
    y='count()',
    color=alt.value("#FFAA00")
    )
st.write(hist)
cpiYear = cpi_month.groupby(cpi_month['Date'].dt.year).sum()
cpiDescribe = cpiYear.describe().T
st.write(cpiDescribe)
st.write("""
The mean of change by the end of each month is 0.303173

Over all the money is lossing it's value through time. By 0.3% every month. 
Which is about 3.638076 each Year. 


***

### Now, let's have a look of the S&P500 and Nasdaq Composite 📈 or 📉
""")

sp = yf.Ticker('^GSPC')
sp_df = sp.history(period='max')

nq = yf.Ticker('^IXIC')
nq_df = nq.history(period='max')

st.write("SP500 Index")
st.line_chart(sp_df['Close'])

st.write("Nasdaq Composite")
st.line_chart(nq_df['Close'])

### sp500
st.write("SP500 Closing Percentage Chnage by day")
N = sp_df['Close'].size

change = ((sp_df['Close'][1:].values / sp_df['Close'][:N-1].values) - 1)*100

changeData = Series(change, index=sp_df.index[1:])
sp_day = pd.DataFrame({'Date':changeData.index,'SP_Percent':changeData.values})

sp_chart = alt.Chart(sp_day).mark_line().encode(
    y='SP_Percent',
    x='Date',
    color=alt.value("#FFAA00"),
    tooltip=['SP_Percent','Date'],
    ).interactive()
st.write(sp_chart)

spM = sp_day.groupby(sp_day['Date'].dt.year).sum()
spDescribe = spM.describe().T
st.write(spDescribe)

### nasdaq
st.write("Nasdaq Composite Closing Percentage Chnage by day")
N = nq_df['Close'].size

change = ((nq_df['Close'][1:].values / nq_df['Close'][:N-1].values) - 1)*100

changeData = Series(change, index=nq_df.index[1:])
nq_day = pd.DataFrame({'Date':changeData.index,'NQ_Percent':changeData.values})

nq_chart = alt.Chart(nq_day).mark_line().encode(
    y='NQ_Percent',
    x='Date',
    color=alt.value("#FFAA00"),
    tooltip=['NQ_Percent','Date'],
    ).interactive()
st.write(nq_chart)

nqM = nq_day.groupby(nq_day['Date'].dt.year).sum()
nqDescribe = nqM.describe().T
st.write(nqDescribe)

# Combine together
combine = pd.concat([spM, nqM,cpiYear], axis=1, join='inner')
st.write(combine)
st.line_chart(data=combine)