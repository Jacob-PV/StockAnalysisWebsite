import pandas as pd
import stockReuse as sr
import streamlit as st
import plotly.express as px
import csv

overview = (
"""This study looks at past data from the ticker \"SPY\" (a S&P 500 clone). It
finds the most profitable day to set your montly investmens on based on when you
get paid. Conditions can be adjusted on the sidebar"""
)
notes = (
"""This data assumes that money cant't be invested until the day after you've been
paid. It also assumes that the money is invested at the market's opening price."""
)
extra_info = (
"""The chart below finds the best investing day for each payday based off the last
27 years of data. If you get paid on multiple days you can check the chart below
on each of those days and see which one ends with a larger balance. Pick the
suggested investing day from that payday. If you have an irregular payday or
already have a lummp sum of cash you want to invest over time, use the most
succesful investing day out of all the paydays."""
)

def dateSuffixFinder(day):
    if(day == 1):
        suffix = "st"
    elif(day == 2):
        suffix = "nd"
    elif(day == 3):
        suffix = "rd"
    else:
        suffix = "th"
    return suffix

# display 27 year chart with best investing day for each payday
def allChart():
    investing_day = []
    end_balance = []
    # get chart from saved file
    with open("bestDayAllSaved.txt", "r") as file:
        data = csv.reader(file)
        for line in data:
            for i in range(31):
                investing_day.append(line[i])
            for i in range(31,len(line)):
                end_balance.append(line[i])

    # create and display df
    df = pd.DataFrame({'Payday': [x for x in range(1, 32)],
                       'Investing Day': [x for x in investing_day],
                       'Ending Balance': [x for x in end_balance]},
                       index = ["" for x in range(31)])

    st.header("Irregular or Multiple Paydays/Lump Sum of Money")
    st.text(extra_info)
    st.table(df)
    best_day = investing_day[end_balance.index(max(end_balance))]
    st.write(f"The largest end balance: ${max(end_balance)} is on the\
    {best_day}{dateSuffixFinder(int(best_day))}")


def bestDay():
    # into text
    st.title("Monthly Investments")
    st.header("Overview")
    st.text(overview)

    # user adjustable vars
    payday = st.sidebar.slider("Payday", 1, 31, 1)
    time_frame = st.sidebar.radio("Time Frame (Years)", (1, 5, 10, 20, 27), 2)
    file = f"Data/SPY{str(time_frame)}.csv"
    payout = st.sidebar.number_input("Monthly Contribution", 1, value=1000)

    df = pd.read_csv(file)

    # set up days
    funds = []
    for i in range(31):
        funds.append(0)

    shares = []
    for i in range(31):
        shares.append(0)

    do_trade = []
    for i in range(31):
        do_trade.append(False)


    # set up days
    for i in range(31):
        funds[i] = 0

    for i in range(31):
        shares[i] = 0

    for i in range(31):
        do_trade[i] = False

    # do trading
    real_day = 1
    trading_day = 0
    while(trading_day < len(df)):
        # trade on current day
        do_trade[real_day-1] = True

        # get current date
        date = int(df["Date"][trading_day].split("-")[2])
        stock_price = float(df["Open"][trading_day])

        # check if real day was a trading day
        if(real_day == date):
            trading_day += 1

        # invest
        for i in range(31):
            if(do_trade[i]):
                shares[i] += sr.buy(funds[i], stock_price)
                funds[i] = 0
                do_trade[i] = False

        # pay on payday (ex: if paid on 1st cant spend till 2nd)
        if(real_day == payday):
            for i in range(31):
                funds[i] += payout

        # increment real day
        real_day += 1
        if(real_day > 31):
            real_day = 1

    # find total money based on each day and get largest
    end_money = []
    largest_value = [0,0]

    for i in range(31):
        end_money.append(round(sr.sell(shares[i], stock_price), 2))
        if(end_money[i] > largest_value[1]):
            largest_value[0] = i+1
            largest_value[1] = end_money[i]

    # suffix for graph title
    suffix = dateSuffixFinder(payday)

    #output graph
    fig = px.line(x = [x for x in range(1, 32)],
                  y = [x for x in end_money],
                  labels={"x": "Day of the Month",
                          "y":"End Balance ($)"},
                  title = str(time_frame) + " " + ("Years" if time_frame > 1 else "Year") +
                          f", Payday: {payday}{suffix}, ${round(payout,0)} Monthly Contribution")
    st.plotly_chart(fig)

    # output text
    st.write(f"Best investing day {[x+1 for x in range(31) if end_money[x] ==max(end_money)]}: ${max(end_money)}")
    st.write(f"Diffence between best investing day {[x+1 for x in range(31) if end_money[x] ==max(end_money)]} \
    and worst investing day {[x+1 for x in range(31) if end_money[x] == min(end_money)]}: \
    ${round(max(end_money)-min(end_money), 2)}")

    st.header("Notes")
    st.text(notes)

if(__name__ == "__main__"):
    bestDay()
