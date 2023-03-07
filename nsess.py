import streamlit as st
import pandas as pd, numpy as np
from nsetools import Nse
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from nsepy import get_history

# !pip install plotly==5.2.1

# In[5]:

nse = Nse()

# In[27]:

adv_dec = nse.get_advances_declines()
df = pd.DataFrame(adv_dec)

top_gainers = nse.get_top_gainers()
dftg = pd.DataFrame(top_gainers)
dftg = dftg.drop(
    ['series', 'previousPrice', 'netPrice', 'tradedQuantity', 'turnoverInLakhs', 'lastCorpAnnouncementDate',
     'lastCorpAnnouncement'], axis=1)

top_losers = nse.get_top_losers()
dftl = pd.DataFrame(top_losers)
dftl = dftl.drop(
    ['series', 'previousPrice', 'netPrice', 'tradedQuantity', 'turnoverInLakhs', 'lastCorpAnnouncementDate',
     'lastCorpAnnouncement'], axis=1)

# In[18]:


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('Stock Dashboard')
qt = pd.DataFrame(nse.get_stock_codes().items(), columns=['SYMBOL', 'NAME OF COMPANY'])
qt = qt.iloc[1:]

selectedstk = st.sidebar.selectbox('Select Stock', qt["SYMBOL"])
selectedindex = st.sidebar.selectbox('Select Index', nse.get_index_list())

with st.sidebar:
    add_radio = st.radio(
        "Select option",
        ("Stock", "Index")
    )

st.sidebar.markdown('''
---
Made by Saksham Mathur
sammathur4@gmail.com
''')

if add_radio == "Stock":
    stkchg = nse.get_quote(selectedstk)['change']
    compnm = nse.get_quote(selectedstk)['companyName']
    currprice = nse.get_quote(selectedstk)['lastPrice']
    dayHigh = nse.get_quote(selectedstk)['dayHigh']
    dayLow = nse.get_quote(selectedstk)['dayLow']
    yrHigh = nse.get_quote(selectedstk)['high52']
    yrLow = nse.get_quote(selectedstk)['low52']

    # Row A
    st.title(compnm)
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", currprice, stkchg)
    col2.metric("Day High", dayHigh)
    col2.metric("Day Low", dayLow)
    col3.metric("52 week high", yrHigh)
    col3.metric("52 week low", yrLow)

    dfstk = get_history(symbol=selectedstk,
                        start=date(2023, 1, 15),
                        end=date(2023, 2, 3))

    fig = go.Figure(data=[go.Candlestick(x=dfstk.index,
                                         open=dfstk['Open'], high=dfstk['High'],
                                         low=dfstk['Low'], close=dfstk['Close'])
                          ])

    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

if add_radio == "Index":
    df1 = df[df['indice'] == selectedindex]
    currprice = nse.get_index_quote(selectedindex)['lastPrice']
    idxchg = nse.get_index_quote(selectedindex)['change']
    st.title(selectedindex)
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", currprice, idxchg)
    col2.metric("Advances", df1["advances"])
    col3.metric("Declines", df1["declines"])
    tab1, tab2 = st.tabs(["Gainer", "Losers"])
    with tab1:
        st.header("Top Gainers")
        st.dataframe(dftg.style.highlight_max(axis=0))
    with tab2:
        st.header("Top Losers")
        st.dataframe(dftl.style.highlight_max(axis=0))