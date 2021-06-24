import streamlit as st
import numpy as np
import pandas as pd
from dashboard.total_terms import governors_days, total_duration_gov
from dashboard.timeline_visualization import state_terms, timeline_name, timeline_state, gender_data, names_list, states_list

# from fuzzywuzzy import fuzz, process

# Str_A = "FuzzyWuzzy is a lifesaver!"
# Str_B = "fuzzy wuzzy is a LIFE SAVER."
# ratio = fuzz.ratio(Str_A.lower(), Str_B.lower())
# st.title(ratio)

st.title("CM Governor Dataset Visualizations")
"Average Days"
st.plotly_chart(governors_days())
"Duration of Governors"
st.plotly_chart(total_duration_gov())
"Gender Data"
st.plotly_chart(gender_data())

state_options = st.multiselect("States", states_list, None)
"Timeline Visualized by State"
try:
    (fig, df, repeats) = timeline_state(state_options)
    st.plotly_chart(fig)
    st.dataframe(df)
    if len(repeats):
        st.write('Governors who have represented more than one state')
        st.dataframe(repeats)
except Exception as e:
    print(e)
    "*Select one or more states to begin.*"
if len(state_options) == 1:
    "State Based Terms"
    st.plotly_chart(state_terms(state_options[0]))
else:
    "*Select only one State to get term visualization*"

name_options = st.multiselect("Names", names_list, None)
"Timeline Visualized by Governors"
try:
    fig, df = timeline_name(name_options)
    st.plotly_chart(fig)
    if len(df) > 1:
        st.dataframe(df)
except Exception as e:
    "*Select one or more Governors to begin.*"
