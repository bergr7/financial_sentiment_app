"""
Config file.
"""

import transformers
from torch import cuda

MAX_LEN = 512
BATCH_SIZE = 64

FINBERT_PATH = "ProsusAI/finbert"
TOKENIZER = transformers.BertTokenizer.from_pretrained("ProsusAI/finbert")

# dataloader params
PARAMS = {'batch_size': BATCH_SIZE,
          'shuffle': False,
          'num_workers': 4
        }

# Setting up the device for GPU usage if available
DEVICE = 'cuda' if cuda.is_available() else 'cpu'