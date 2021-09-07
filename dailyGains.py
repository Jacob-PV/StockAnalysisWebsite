import pandas as pd
import streamlit as st
import plotly.express as px

class DayOfWeek:
    def __init__(self, name):
        self.name = name
        self.total_percent = 0
        self.percent_gain = 0
        self.total_days = 0
        self.yearly_return = 0

    def new_value(self, percent):
        self.total_percent += percent
        self.total_days += 1
        self.percent_gain = self.total_percent / self.total_days * 100

    def calc_yearly_return(self):
        total = 100
        for i in range(52):
            total *= 1+(self.percent_gain/100)
        self.yearly_return = total - 100

    def display(self):
        self.calc_yearly_return()
        print("{}: {:.2f}% -> {:.2f}%".format(self.name, self.percent_gain, self.yearly_return))

overview = (
"""This study looks at the average daily return of the ticker \"SPY\" (a S&P 500
clone)."""
)

def dailyGains():
    st.title("Periodical Returns")
    st.header("Average Daily Returns")
    st.text(overview)

    st.sidebar.header("Daily")
    time_frame = st.sidebar.radio("Time Frame (Years)", (1, 5, 10, 20, 27), 2)
    month_options = ["All Months","January","February","March","April","May","June",\
                     "July","August","September","October","November","December"]
    month_choice = st.sidebar.selectbox("Month", month_options, 0)

    # init vars
    day_names = ["Monday","M - After Hours","Tuesday","Tu - After Hours","Wednesday","W - After Hours",\
    "Thursday","Th - After Hours","Friday","F - After Hours"]
    days = []
    # last_day = "None"
    for i in day_names:
        days.append(DayOfWeek(i))

    # get stock data
    # time_frame = 27

    file = f"Data/SPY{str(time_frame)}.csv"
    df = pd.read_csv(file)

    # t = 1000
    for i in range(len(df)):
        day = pd.Timestamp(df["Date"][i])
        month = day.month_name()
        day = day.day_name()

        if(month == month_choice or month_choice == "All Months"):
            percent_change = ((df["Close"][i] - df["Open"][i]) / df["Open"][i])
            if(i != 0):
                afterhours_percent_change = (df["Open"][i] - df["Close"][i-1]) / df["Close"][i-1]
            for j in range(len(day_names)):
                if(day == days[j].name):
                    days[j].new_value(percent_change)
                    # after hours
                    if(i != 0):
                        days[j+1].new_value(afterhours_percent_change)

    # total = 0
    # for i in range(len(day_names)):
    #     total += days[i].percent_gain
    #     days[i].display()


    fig = px.bar(x = day_names,
                 y = [x.percent_gain for x in days],
                 labels = {"x": "Timeframe",
                           "y": "Average Percent Change (%)"},
                 title = str(time_frame) + " " + ("Years" if time_frame > 1 else "Year") +
                 "; Average Daily Returns")

    st.plotly_chart(fig)
