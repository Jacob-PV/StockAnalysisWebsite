import streamlit as st
from bestDayPay import bestDay, allChart
from bollingerBands import bb
from redditBuzz import reddit
from adjustedStockComp import stockComp
from dailyGains import dailyGains
from monthlyGains import monthlyGains


st.sidebar.title("Stock Analysis")
page = st.sidebar.selectbox("Page", ("Monthly Investments", \
"Percent Return Stock Comparison", "Reddit Buzz", "Periodical Returns"), 3)

if(page == "Monthly Investments"):
    bestDay()
    allChart()
elif(page == "Percent Return Stock Comparison"):
    stockComp()
elif(page == "Reddit Buzz"):
    reddit()
elif(page == "Periodical Returns"):
    dailyGains()
    monthlyGains()
