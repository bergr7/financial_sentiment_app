"""
Parse RSS Feed.

"""

import feedparser

# rss keys -> dict_keys(['title', 'title_detail', 'links', 'link', 'id', 'guidislink', 'published', 'published_parsed', 'sa_author_name', 'media_thumbnail', 'href', 'sa_picture', 'sa_symbol', 'sa_company_name', 'sa_stock'])

def rss_parser(url):
    """
    Seeking Alpha RSS news parser.

    Parameters
    ----------
    url: str, rss feed url

    Returns
    -------
    news: dict, news fed by seeking alpha
    """
    # parse news
    try:
        NewsFeed = feedparser.parse(url)
    except Exception as e:
        print("RSS feed not found.")
        print(e)

    # get entries
    entries = NewsFeed.entries
    n_entries = len(entries)
    if n_entries < 1:
        print("Ticker not found or no news available.")
        return None
    print(f"Number of RSS posts: {n_entries}")

    # dict keys
    keys = ["title", "link", "published", "sa_company_name", "sa_author_name"]

    # store data in dict
    news = dict()
    for idx in range(n_entries):
        # get entry
        entry = entries[idx]
        # save relevant data in dict
        entry_dict = {key: entry[key] for key in keys}
        # save news
        news[idx] = entry_dict
    
    return news

if __name__ == "__main__":
    # seeking alpha RSS feed by stock
    ticker = "dasgafd"
    url = f"https://seekingalpha.com/api/sa/combined/{ticker}.xml"
    news = rss_parser(url)
    print(news)