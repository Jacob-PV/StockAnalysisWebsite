import pandas as pd
import streamlit as st
import plotly.express as px

class Month:
    def __init__(self, name):
        self.name = name
        self.current = False
        self.open = 0
        self.close = 0
        self.total_percent = 0
        self.percent_gain = 0
        self.total_months = 0

    def calculate(self):
        self.total_percent += (self.close - self.open) / self.open * 100
        self.total_months += 1
        self.percent_gain = self.total_percent / self.total_months

    def add_open(self, value):
        self.open = value
        self.current = True

    def add_close(self, value):
        self.close = value
        self.current = False
        self.calculate()

overview = (
"""This study looks at the average montly return of the ticker \"SPY\" (a S&P 500
clone)."""
)

def monthlyGains():
    st.header("Average Montly Returns")
    st.text(overview)

    st.sidebar.subheader("Monthly")
    time_frame = st.sidebar.radio("Time Frame (Years)", (1, 5, 10, 20, 27), 2, key = "1")
    # time_frame = 27
    file = f"Data/SPY{str(time_frame)}.csv"
    df = pd.read_csv(file)

    month_options = ["January","February","March","April","May","June", "July",\
                     "August","September","October","November","December"]
    months = []
    for i in range(len(month_options)):
        months.append(Month(month_options[i]))

    for i in range(len(df)):
        day = pd.Timestamp(df["Date"][i])
        month = day.month_name()

        # check for start of month
        for j in range(len(month_options)):
            if(month == months[j].name and not months[j].current):
                months[j].add_open(df["Open"][i])
        #check for end of month
        for j in range(len(month_options)):
            if(month != months[j].name and months[j].current):
                months[j].add_close(df["Close"][i-1])

    # close any open months
    for i in range(len(month_options)):
        if(months[i].current):
            months[i].add_close(df["Close"].iloc[-1])

    fig = px.bar(x = month_options,
                 y = [x.percent_gain for x in months],
                 labels = {"x": "Month",
                           "y": "Average Percent Change (%)"},
                 title = str(time_frame) + " " + ("Years" if time_frame > 1 else "Year") +
                 "; Average Montly Returns")

    st.plotly_chart(fig)

if(__name__ == "__main__"):
    monthlyGains()
