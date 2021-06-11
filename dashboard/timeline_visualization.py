# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date

import plotly.graph_objects as go

import plotly.express as px

pd.options.plotting.backend = "plotly"

source = "./Governors Data/governors_draft_4.csv"

df = pd.read_csv(source)
df = df.replace(np.nan, "", regex=True)

# print(df)


states = []
for index, row in df.iterrows():
    states.append(row["state/ut"])

states = list(np.unique(np.array(states)))

# print(states, len(states))


data = []


def date_get(s):
    return s[6] + s[7] + s[8] + s[9] + "-" + s[3] + s[4] + "-" + s[0] + s[1]


def timeline_state(state='West Bengal'):
    for index, row in df.iterrows():
        if row["state/ut"] == state:
            # print(type(row["appointment_begin"]))
            start_date = date_get(row["appointment_begin"])
            if row["appointment_end"] != "Current":
                end_date = date_get(row["appointment_end"])
            else:
                end_date = "2021-01-13"
            data.append(
                {
                    "Name": row["name"],
                    "Start": start_date,
                    "Finish": end_date,
                    "State": row["state/ut"],
                }
            )
    data_df = pd.DataFrame(data)
    fig = px.timeline(data_df, x_start="Start",
                      x_end="Finish", y="Name")
    return fig


# fig = px.timeline(data_df, x_start='Start', x_end='Finish', y='State', color='State')
# fig.show()


def timeline_name():
    pass
#     fig = px.timeline(data_df, x_start="Start",
#                       x_end="Finish", y="State", color="State")
#     return fig
