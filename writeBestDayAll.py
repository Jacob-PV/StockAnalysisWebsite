import pandas as pd
import stockReuse as sr

def saveBestDayAll():
    payday = 1
    payout = 1000
    payday_list = []
    largest_date = []
    largest_money = []
    file = "Data/SPY27.csv"
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

    # invest with each day being a payday
    while(payday < 32):
        # reset days
        for i in range(31):
            funds[i] = 0

        for i in range(31):
            shares[i] = 0

        for i in range(31):
            do_trade[i] = False

        real_day = 1
        trading_day = 0
        while(trading_day < len(df)):
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

            # pay on payday (if paid on 1st cant spend till 2nd)
            if(real_day == payday):
                for i in range(31):
                    funds[i] += payout

            # increment real day
            real_day += 1
            if(real_day > 31):
                real_day = 1

        # store largest end balance info
        end_money = []
        largest_value = [0,0]

        for i in range(31):
            end_money.append(round(sr.sell(shares[i], stock_price), 2))
            if(end_money[i] > largest_value[1]):
                largest_value[0] = i+1
                largest_value[1] = end_money[i]

        largest_date.append(largest_value[0])
        largest_money.append(largest_value[1])

        payday += 1

    # write to file
    with open("bestDayAllSaved.txt", "w") as file:
        for i in range(31):
            file.write(str(largest_date[i]))
            file.write(",")
        for i in range(31):
            file.write(str(largest_money[i]))
            if(i!=30):
                file.write(",")

if(__name__ == "__main__"):
    saveBestDayAll()
