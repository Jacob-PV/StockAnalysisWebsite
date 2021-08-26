import yfinance as yf
import yfinance.shared as shared
import streamlit as st
import pandas as pd

def stockComp():
    # get numbr of tickers to display
    if "num_tickers" not in st.session_state:
        st.session_state.num_tickers = 1

    def addTicker():
        st.session_state.num_tickers += 1

    def removeTicker():
        st.session_state.num_tickers -= 1

    num_tickers = st.session_state.num_tickers

    st.title("Percent Return Stock Comparison")

    # ticker inputs
    tickers = []
    for i in range(num_tickers):
        tickers.append(st.sidebar.text_input(label = "Ticker " + str(i+1), key = str(i), value = "AAPL"))

    # add/remove tickers
    st.sidebar.button("Add Ticker", on_click = addTicker)
    if(num_tickers > 1):
        st.sidebar.button("Remove Ticker", on_click = removeTicker)


    start = st.sidebar.date_input("Start",
                                  min_value = pd.to_datetime("1993-01-01"),
                                  max_value = pd.to_datetime("today"),
                                  value = pd.to_datetime("2021-08-01"))
    end = st.sidebar.date_input("End",
                                min_value = pd.to_datetime("1993-01-01"),
                                max_value = pd.to_datetime("today"),
                                value = pd.to_datetime("today"))

    ticker = ""
    for i in range(len(tickers)):
        if i == 0:
            ticker += str(tickers[i])
        else:
            ticker += ", " + str(tickers[i])

    def relativeReturn(df):
        rel = df.pct_change()
        current = ((1+rel).cumprod() - 1) * 100
        current = current.fillna(0)
        return current

    df = relativeReturn(yf.download(tickers, start, end)["Adj Close"])

    if(len(list(shared._ERRORS.keys())) == 0):
        st.subheader(ticker)
        st.line_chart(df)
    else:
        st.write(f"\"{ticker}\" data could not be found")


    # get stock stats
    stock_stats = ["marketCap", "trailingPE", "trailingEps", "trailingAnnualDividendYield"]
    yf_tickers = []
    stat_dict = {}
    for i in range(len(tickers)):
        yf_tickers.append(yf.Ticker(tickers[i]))
        stat_dict[tickers[i]] = []
        for j in range(len(stock_stats)):
            try:
                stat_dict[tickers[i]].append(yf_tickers[i].info[stock_stats[j]])
            except:
                stat_dict[tickers[i]].append(None)

    # display stock stats
    df2 = pd.DataFrame(stat_dict)
    df2.index = ["Market Cap", "P/E", "EPS", "Dividend Yield"]
    st.table(df2)


    df2 = pd.DataFrame()
    df2.append

if (__name__ == "__main__"):
    stockComp()
