import streamlit as st
import numpy as np
import pandas as pd

from parser import rss_parser
from inference import run_inference


st.title("News Feed")
st.header("RSS by Seeking Alpha")
st.subheader("Author: Bernardo Garcia")



# input ticker
ticker = st.text_input("Input ticker. e.g. AAPL: ")

if st.button("Run"):

    with st.spinner("Parsing news and extracting sentiment..."):
        # parse news
        url = f"https://seekingalpha.com/api/sa/combined/{ticker}.xml"
        news = rss_parser(url)

         # sentiment -> call inference
        sentiments = run_inference(news)
    st.success("Extraction completed.")
    st.balloons()

    #st.json(news)
    for i in range(len(news)):
        item = news[i]
        st.write(item["published"][:-6])
        st.write(item["title"])
        st.write(f"Sentiment: {sentiments[i]}")
        st.write(":link: " + "*" + item["link"] + "*")
        st.write("******")