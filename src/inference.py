"""
Function to make inference.
"""

import config
import dataset

import numpy as np

import torch
from torch.utils.data import DataLoader
import transformers

from tqdm import tqdm

from utils import decode_sentiment

def run_inference(news):
    """
    Runs inference on data.

    Parameters
    ----------
    news: json file, news from RSS feed

    Returns
    -------
    inferences: list, sentiment for each title
    """
    # convert json to list of news
    news_list = [news[k]["title"] for k in news.keys()] # TODO - error here
    # create torch dataset and dataloader
    inference_set = dataset.FinBERTDataset(news_list)
    data_loader = DataLoader(inference_set, **config.PARAMS)
    # load model
    model = transformers.BertForSequenceClassification.from_pretrained(config.FINBERT_PATH)
    model.eval()
    device = torch.device(config.DEVICE)
    model.to(device)
    # inference
    outputs_list = []
    with torch.no_grad():
        for _, d in tqdm(enumerate(data_loader), total=len(data_loader)):
            ids = d['ids']
            mask = d['mask']
            token_type_ids = d["token_type_ids"]


            # send them to the cuda device we are using
            ids = ids.to(torch.device(device), dtype=torch.long)
            mask = mask.to(torch.device(device), dtype=torch.long)
            token_type_ids = token_type_ids.to(torch.device(device), dtype=torch.long)

            outputs = model(
                input_ids=ids,
                attention_mask=mask,
                token_type_ids=token_type_ids
            )

            outputs_list.extend(torch.softmax(outputs.logits, dim=1).cpu().detach().numpy().tolist())

    # get most probable class
    inferences = np.argmax(outputs_list, axis=1)

    # decode sentiment
    sentiments = decode_sentiment(inferences)

    return sentiments, inferences