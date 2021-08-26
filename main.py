import streamlit as st
from bestDayPay import bestDay, allChart
from bollingerBands import bb
from redditBuzz import reddit
from adjustedStockComp import stockComp

st.sidebar.title("Stock Analysis")
page = st.sidebar.selectbox("Page", ("Monthly Investments", "Percent Return Stock Comparison", "Reddit Buzz"), 1)

if(page == "Monthly Investments"):
    bestDay()
    allChart()
elif(page == "Percent Return Stock Comparison"):
    stockComp()
elif(page == "Reddit Buzz"):
    reddit()
