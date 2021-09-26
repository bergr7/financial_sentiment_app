import streamlit as st
from parser import rss_parser
from inference import run_inference
from utils import volume_sent_chart, close_sent_chart, get_data

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

    # get data for charts
    close_volume, ind_data = get_data(news, sentiments, inferences, ticker)

    # write news data on left col from news json file
    for i in range(len(news)):
        item = news[i]
        left_col.write(item["published"][:-6])
        left_col.write(item["title"])
        left_col.write(f"Sentiment: {sentiments[i]}")
        left_col.write(":link: " + "*" + item["link"] + "*")
        left_col.write("******")

    # Plot indicators charts
    right_col.pyplot(volume_sent_chart(close_volume, ind_data))
    right_col.pyplot(close_sent_chart(close_volume, ind_data))