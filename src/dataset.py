"""
FinBERT dataset.
"""

import config
import torch

class FinBERTDataset:
    def __init__(self, title, target=None):
        self.title = title
        self.target = target    # list of number: 0 or 1
        self.tokenizer = config.TOKENIZER
        self.max_len = config.MAX_LEN

    def __len__(self):
        return len(self.title)

    def __getitem__(self, item):  # takes a item and returns your items in the dataset
        title = str(self.title[item])
        title = " ".join(title.split())

        inputs = self.tokenizer.encode_plus(
            title,
            None,   # second string is None in this case
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True
        )

        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        token_type_ids = inputs["token_type_ids"]

        if self.target:
            return {
                'ids': torch.tensor(ids, dtype=torch.long),
                'mask': torch.tensor(mask, dtype=torch.long),
                'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
                'target': torch.tensor(self.target[item], dtype=torch.float)
            }
        else:
            return {
                'ids': torch.tensor(ids, dtype=torch.long),
                'mask': torch.tensor(mask, dtype=torch.long),
                'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
            }



