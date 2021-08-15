"""
Helper functions.
"""

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