import os
import numpy as np

# create `network_processed` directory if it doesn't exist
if not os.path.exists("network_processed"):
    os.makedirs("network_processed")

import pandas as pd

df = pd.read_csv(
    "tgn/data/wikipedia.csv",
    skiprows=1,
    header=None,
)
df.columns = ["user_id", "item_id", "timestamp", "state_label"] + [
    f"feature {i}" for i in range(len(df.columns) - 4)
]

df.head()

roles = pd.read_csv("node_role.csv")

# get the role of user i in game game_id
roles[(roles["game_id"] == game_id) & (roles["user_id"] == i)]["role"].values[0]

# game is a numpy array with shape (t, from, to) where t is the time step

game_id = meta_row["NETWORK"]
game = loadGame(game_id)

records = []
for timestep, frame in enumerate(game):
    print(f"timestep {timestep} {frame}")
    # record: user_id, item_id, timestamp, state_label, feature
    # get max index of each row
    max_index = np.argmax(frame, axis=1)
    for i, item_id in enumerate(max_index):
        # get the role of user i in game game_id
        role = roles[
            (roles["node"] == f"P{i+1}") & (roles["ID"] == meta_row["NETWORK"])
        ]["role"].values
        records.append([i + 1, item_id, timestep, role, 0])
    records.append()
    # frame is a numpy array with shape (from, to)
