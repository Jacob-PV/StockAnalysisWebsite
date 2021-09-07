# stock symbol data from https://institutional.vanguard.com/web/c1/investments/product-details/fund/0970

import praw
import csv
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import streamlit as st
# from reddit_keys import user_agent, client_id, client_secret

overview = (
"""This page grabs some of most talked about posts relating to stocks off of reddit."""
)

def reddit():
    st.title("Reddit Buzz")
    st.header("Overview")
    st.text(overview)

    # toggle reddit call
    call_reddit = True
    sentiment_on = False
    sentiment = 0
    subreddits = ['wallstreetbets','investing','stocks','stockMarket','wallstreetdd',
        'algotrading','stockaday','SecurityAnalysis']
    # subreddits = ["stocks"]

    # symbols that break the system
    common_symbols = ['A','DD','PE','RTX','PB','EV','LOB','ON','BIG','FOR','TA','GO',
        'RH','HEAR','IBKR','PSA','LIVE','HAS','SP','B','NOW','SO','IT','BE','AI','OUT',
        'GOOD','EVER','CASH','SIX']
    bad_stocks = ['GME','AMC']

    # get all stock symbols
    symbols = {}
    with open("clean_symbols.csv","r") as file:
        for line in file:
            symbols[line.replace("\n","")] = 0

    # call reddittitle
    if call_reddit:
        # init reddit call
        reddit = praw.Reddit(
            user_agent=st.secrets["user_agent"],
            client_id=st.secrets["client_id"],
            client_secret=st.secrets["client_secret"],
            # only need username and password to post
            #username="USERNAME",
            #password="PASSWORD"
        )

        # search subreddits
        articles = {}
        for subreddit in subreddits:
            #print(f"->r/{subreddit}<-")
            for submission in reddit.subreddit(subreddit).top(limit=25,time_filter="day"):
                iteration = 0
                for word in submission.selftext.split() and submission.title.split():
                    # clean words
                    replace = ['$','(',')',':','NYSE','NASDAQ',',','/']
                    for ch in replace:
                        word.replace(ch, '')
                    # check for word in db
                    if word.upper() in symbols.keys() and (word not in common_symbols) and (word not in bad_stocks):
                        if sentiment_on:
                            opinion = TextBlob(submission.selftext, analyzer=NaiveBayesAnalyzer())
                            sentiment = opinion.sentiment[1]-opinion.sentiment[2]
                        articles[submission.url + iteration*' '] = [word, submission.title, subreddit, sentiment, submission.upvote_ratio]
                        try:
                            symbols[word] += submission.score
                        except:
                            Exception
                        iteration+=1

        # order findings
        findings = []
        print_order = []
        for (k, v) in symbols.items():
            if v > 0 and v not in findings:
                findings.append(int(v))
        findings.sort(reverse=True)
        for value in findings:
            for (k, v) in symbols.items():
                if v == value:
                    print_order.append(k)
        # print articles
        for sym in print_order:
            st.header(sym)
            for (k, v) in articles.items():
                if v[0] == sym:
                    st.write(f"(r/{v[2]}; Upvote Ratio: {v[4]}) {v[1]}\nLink: {k}")
        # print ranks
        st.subheader("Total Upvotes")
        for sym in print_order:
            for (k, v) in symbols.items():
                if k == sym:
                    st.write(k, v)

    # check if symbol is in db
    # print("AAPL" in symbols)
    # print("SE" in symbols)
    # print("DD" in symbols)

if(__name__ == "__main__"):
    reddit()
