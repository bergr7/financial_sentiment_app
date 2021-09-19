import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from parser import rss_parser
from inference import run_inference
import matplotlib.pyplot as plt

## basic setup and app layout
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Indicadores de sentimiento")
st.markdown("Fuente de noticias: [Seeking Alpha](https://seekingalpha.com/)")
st.sidebar.title("Panel de control")
left_col, right_col = st.columns(2)

# user inputs on the control panel
st.sidebar.subheader("Ticker")
# input ticker
ticker = st.sidebar.text_input("Introducir ticker. e.g. AAPL: ")
run_button = st.sidebar.button("Extraer noticias")

# news col
left_col.subheader("Noticias")
# indicators col
right_col.subheader("Indicadores")

if run_button:

    with st.spinner("Parsing news and extracting sentiment..."):
        # parse news
        url = f"https://seekingalpha.com/api/sa/combined/{ticker}.xml"
        news = rss_parser(url)

         # sentiment -> call inference
        sentiments, inferences = run_inference(news)
        st.success("Extraction completed.")

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
    data["sentiment_int"] = inferences  # TODO - map to -1, 0 ans 1

    # write news data on left col from news json file
    for i in range(len(news)):
        item = news[i]
        left_col.write(item["published"][:-6])
        left_col.write(item["title"])
        left_col.write(f"Sentiment: {sentiments[i]}")
        left_col.write(":link: " + "*" + item["link"] + "*")
        left_col.write("******")

    # get daily close price and volume of the last month
    price_data = yf.download(
        tickers=ticker,
        period="1mo",
        interval="1d"
    )
    close_volume = price_data.loc[:, ["Close", "Volume"]]
    close_volume = close_volume.reset_index()
    close_volume = close_volume.rename(columns={"Date": "date", "Close": "close", "Volume": "volume"})


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

    # chart
    dates_plot = np.array([pd.to_datetime(date, format="%Y-%m-%d") for date in ind_data.date.values])
    dates_labels =  [str(date)[:-9] for date in dates_plot]
    volume = close_volume.loc[close_volume.date >= min(dates_plot), "volume"]
    sentiment_scores = ind_data.day_score.values

    fig = plt.figure(figsize=(20,4))

    ax1 = plt.subplot(121)
    ax2 = ax1.twinx()

    # conditional color scatter
    pos_idx = sentiment_scores > 0
    neg_idx = sentiment_scores < 0
    neu_idx = sentiment_scores == 0

    b = ax1.bar(dates_plot, volume, color="lightblue")
    s = ax2.scatter(dates_plot[pos_idx], sentiment_scores[pos_idx], color="green")
    s2 = ax2.scatter(dates_plot[neg_idx], sentiment_scores[neg_idx], color="red")
    s3 = ax2.scatter(dates_plot[neu_idx], sentiment_scores[neu_idx], color="gray")

    ax1.set_xticks(dates_plot)
    ax1.set_xticklabels(dates_labels, rotation=90)
    ax1.set_ylabel("Volume")
    ax2.set_ylabel("Sentiment score")

    ax2.axhline(0, 0, 1, color="gray", linestyle="--")
    plt.title("Daily sentiment score compared to traded volume")

    right_col.pyplot(fig)