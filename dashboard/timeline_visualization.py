# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import json

import plotly.graph_objects as go

import plotly.express as px

pd.options.plotting.backend = "plotly"

source = "./Governors Data/governors_draft_4.csv"
# source = "./Chief Minister's Data/CM_Final.csv"

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


states_list = []
for index, row in df.iterrows():
    states_list.append(row["state/ut"])
names_list = []
for index, row in df.iterrows():
    names_list.append(row["name"])
names_list = list(set(names_list))
states_list = list(np.unique(np.array(states_list)))

repeat_governors = {}


def timeline_state(start_year, end_year, states=[]):
    if not states:
        return None
    data = []
    for state in states:
        for index, row in df.iterrows():
            if row["state/ut"] == state:
                # print(type(row["appointment_begin"]))
                start_date = date_get(row["appointment_begin"])
                if row["appointment_end"] != "Current":
                    end_date = date_get(row["appointment_end"])
                else:
                    end_date = "2021-01-13"
                if int(end_date[:4]) >= start_year and int(start_date[:4]) <= end_year:
                    if row["name"] not in repeat_governors:
                        repeat_governors[row["name"]] = [row["state/ut"]]
                    else:
                        repeat_governors[row["name"]].append(row["state/ut"])
                    data.append(
                        {
                            "Name": f'{row["name"]} ({row["state/ut"]})',
                            "Start": start_date,
                            "Finish": end_date,
                            "State": row["state/ut"],
                        }
                    )
    repeats = []
    for name in repeat_governors:
        cur_list = list(set(repeat_governors[name]))
        if len(cur_list) > 1:
            repeats.append({"name": name, "States": ', '.join(cur_list)})
    repeats = pd.DataFrame(repeats)
    data_df = pd.DataFrame(data)
    fig = px.timeline(data_df, x_start="Start",
                      x_end="Finish", y="Name", color="State")
    for index, row in data_df.iterrows():
        row["Name"] = row["Name"].split("(")[0]
    return (fig, data_df, repeats)


# fig = px.timeline(data_df, x_start='Start', x_end='Finish', y='State', color='State')
# fig.show()


def timeline_name(start_year, end_year, names=[]):
    if not names:
        return None
    data = []
    for name in names:
        for index, row in df.iterrows():
            if row["name"] == name:
                # print(type(row["appointment_begin"]))
                start_date = date_get(row["appointment_begin"])
                if row["appointment_end"] != "Current":
                    end_date = date_get(row["appointment_end"])
                else:
                    end_date = "2021-01-13"
                if int(end_date[:4]) >= start_year and int(start_date[:4]) <= end_year:
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
                      x_end="Finish", y="State", color="Name")
    return (fig, data_df)


def gender_data():
    keys = df.groupby(
        ["state/ut"])["Gender"].value_counts(normalize=True).keys().tolist()
    values = df.groupby(
        ["state/ut"])["Gender"].value_counts(normalize=True).tolist()
    ratio = {"State": [], "Ratio": []}
    for ptr in range(len(keys)):
        if keys[ptr][1] == "M":
            ratio["State"].append(keys[ptr][0])
            ratio["Ratio"].append(1 - values[ptr])

    states = json.load(open("./Governors Data/states_india.geojson", "r"))
    states["features"][1]["properties"]
    state = {}
    anomalies = {
        "Arunanchal Pradesh": "Arunachal Pradesh",
        "Andaman & Nicobar Island": "Andaman & Nicobar Islands",
        "Dadara & Nagar Havelli": "Dadra & Nagar Haveli",
        "NCT of Delhi": "Delhi",
    }
    list_states = []
    for f in states["features"]:
        f["id"] = f["properties"]["state_code"]
        s = f["properties"]["st_nm"]
        if s in anomalies:
            s = anomalies[s]
        list_states.append(s)
        state[s] = f["id"]
    ratio = pd.DataFrame(ratio)
    ratio.drop(index=ratio[ratio["State"] == "Ladakh"].index, inplace=True)
    ratio.drop(
        index=ratio[ratio["State"] ==
                    "Dadra & Nagar Haveli & Daman & Diu"].index,
        inplace=True,
    )
    # state['Dadra & Nagar Haveli & Daman & Diu']=state['Dadra & Nagar Haveli']
    # state['Ladakh']=state['Jammu & Kashmir']
    # print(state['Lad'])
    ratio["id"] = ratio["State"].apply(lambda x: state[x])
    flag = False
    # print(ratio.iloc[0]['State'])
    # This is to check if all the states match or not
    for i in range(len(ratio.index)):
        if ratio.iloc[i]["State"] in list_states:
            continue
        else:
            flag = True
    # print(flag)
    fig = px.bar(ratio, x='State', y='Ratio', labels={
        "Ratio": "Percentage of Females"
    })
    # print(ratio)
    return fig


def state_terms(state=""):
    try:
        unique_id = []
        for index, row in df.iterrows():
            if row["state/ut"] == state:
                unique_id.append(row["ID"])

        unique_id = list(np.unique(np.array(unique_id)))
        names = []
        total_dur = []

        for i in unique_id:
            name = ""
            total = 0
            for index, row in df.iterrows():
                if row["state/ut"] == state and row["ID"] == i:
                    total += row["term_duration"]
                    name = row["name"]
            names.append(name), total_dur.append(total)
        fig = go.Figure(
            data=[go.Pie(labels=names, values=total_dur)])
        return fig
    except Exception as e:
        return None
