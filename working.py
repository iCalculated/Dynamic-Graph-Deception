import os

# create `network_processed` directory if it doesn't exist
if not os.path.exists("network_processed"):
    os.makedirs("network_processed")

# open wikipedia.csv as a dataframe with first columns labeled
import pandas as pd

df = pd.read_csv(
    "wikipedia.csv",
    header=0,
    names=["user_id", "item_id", "timestamp", "state_label", "features"],
)
