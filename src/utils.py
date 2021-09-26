"""
Helper functions.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def decode_sentiment(inferences):
    """Decode sentiment."""
    decoded_sentiment = []
    for sentiment in inferences:
        if sentiment == 0:
            decoded_sentiment.append("Positive")
        elif sentiment == 1:
            decoded_sentiment.append("Negative")
        else:
            decoded_sentiment.append("Neutral")

    return decoded_sentiment

def get_data(news, sentiments, inferences, ticker):
    """Extract and prepare price and sentiment data for charts."""
    # merge sentiment and inferences with news in a df
    dates = []
    titles = []
    links = []
    for i in range(len(news)):
        item = news[i]
        dates.append(item["published"][:-15])
        titles.append(item["title"])
        links.append(item["link"])
    
    data = pd.DataFrame([dates, titles, links]).T
    data = data.rename(columns={0: "date", 1: "title", 2: "link"})
    data["date"] = data["date"].map(lambda x: pd.to_datetime(x))
    data["sentiment"] = sentiments
    data["sentiment_int"] = inferences
    # map to -1, 0 or 1
    def map_sent(x):
        if x == 0:
            return 1
        elif x == 1:
            return -1
        else:
            return 0

    data["sentiment_int"] = data["sentiment_int"].map(map_sent)

    # get indicators data
    sent_dates = []
    n_news_list = []
    sent_scores = [] 
    for date in data.date.sort_values().unique():
        news_subset = data.loc[data.date == date]
        sentiment_score = news_subset.sentiment_int.sum() / news_subset.shape[0]
        n_news = news_subset.shape[0]
        sent_dates.append(date)
        n_news_list.append(n_news)
        sent_scores.append(sentiment_score)

    ind_data = pd.DataFrame([sent_dates, sent_scores, n_news_list]).T.rename(columns={0: "date", 1: "day_score", 2: "no_news"})

    # get daily close price and volume of the last month
    price_data = yf.download(
        tickers=ticker,
        period="1mo",
        interval="1d"
    )
    close_volume = price_data.loc[:, ["Close", "Volume"]]
    close_volume = close_volume.reset_index()
    close_volume = close_volume.rename(columns={"Date": "date", "Close": "close", "Volume": "volume"})

    return close_volume, ind_data


def volume_sent_chart(close_volume, ind_data):
    """Creates a chart showing volume and daily sentiment of the last month."""
    dates_plot = np.array([pd.to_datetime(date, format="%Y-%m-%d") for date in close_volume.date.values])
    dates_labels =  [str(date)[:-9] for date in dates_plot]
    volume = close_volume.loc[:, "volume"]
    dates_sent = ind_data.loc[ind_data.date >= dates_plot.min()].date.values
    sentiment_scores = ind_data.loc[ind_data.date >= dates_plot.min()].day_score.values
    
    fig = plt.figure(figsize=(20,4))

    ax1 = plt.subplot(121)
    ax2 = ax1.twinx()

    # conditional color scatter
    pos_idx = sentiment_scores > 0
    neg_idx = sentiment_scores < 0
    neu_idx = sentiment_scores == 0

    b = ax1.bar(dates_plot, volume, color="lightblue")
    s = ax2.scatter(dates_sent[pos_idx], sentiment_scores[pos_idx], color="green")
    s2 = ax2.scatter(dates_sent[neg_idx], sentiment_scores[neg_idx], color="red")
    s3 = ax2.scatter(dates_sent[neu_idx], sentiment_scores[neu_idx], color="gray")

    ax1.set_xticks(dates_plot)
    ax1.set_xticklabels(dates_labels, rotation=90)
    ax1.set_ylabel("Volume")
    ax2.set_ylabel("Sentiment score")

    ax2.axhline(0, 0, 1, color="gray", linestyle="--")
    plt.title("Daily sentiment score and traded volume of the last month")

    return fig

def close_sent_chart(close_volume, ind_data):
    """Creates a chart showing close price and daily sentiment of the last month."""
    dates_plot = np.array([pd.to_datetime(date, format="%Y-%m-%d") for date in close_volume.date.values])
    dates_labels =  [str(date)[:-9] for date in dates_plot]
    close = close_volume.loc[:, "close"]
    dates_sent = ind_data.loc[ind_data.date >= dates_plot.min()].date.values
    sentiment_scores = ind_data.loc[ind_data.date >= dates_plot.min()].day_score.values

    fig = plt.figure(figsize=(20,4))

    ax1 = plt.subplot(121)
    ax2 = ax1.twinx()

    # conditional color
    pos_idx = sentiment_scores > 0
    neg_idx = sentiment_scores < 0

    l = ax1.plot(dates_plot, close, color="black", lw=1.5)
    b = ax2.bar(dates_sent[pos_idx], sentiment_scores[pos_idx], color="palegreen", alpha=0.5)
    b2 = ax2.bar(dates_sent[neg_idx], sentiment_scores[neg_idx], color="indianred", alpha=0.5)

    ax1.set_xticks(dates_plot)
    ax1.set_xticklabels(dates_labels, rotation=90)
    ax1.set_ylabel("Price Close")
    ax2.set_ylabel("Sentiment score")

    ax2.axhline(0, 0, 1, color="gray", linestyle="--")
    plt.title("Daily sentiment score and close price of the last month")

    return fig
