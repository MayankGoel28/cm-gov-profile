import streamlit as st
import numpy as np
import pandas as pd
import traceback
from dashboard.total_terms import governors_days
from dashboard.timeline_visualization import state_terms, timeline_name, timeline_state, gender_data, names_list, states_list

# from fuzzywuzzy import fuzz, process

# Str_A = "FuzzyWuzzy is a lifesaver!"
# Str_B = "fuzzy wuzzy is a LIFE SAVER."
# ratio = fuzz.ratio(Str_A.lower(), Str_B.lower())
# st.title(ratio)

st.sidebar.write("Parameters")
start_year, end_year = st.sidebar.slider(
    "Select applicable years for timeline visualizations", 1930, 2021, value=(1930, 2021))
show_df = st.sidebar.checkbox("Show dataframes")

st.title("CM Governor Dataset Visualizations")
with st.beta_expander("Average Days"):
    st.plotly_chart(governors_days())
with st.beta_expander("Gender Data"):
    st.plotly_chart(gender_data())


state_options = st.sidebar.multiselect(
    "States for timeline visualization", states_list, None)
with st.beta_expander("Timeline Visualized by State"):
    try:
        (fig, df, repeats) = timeline_state(
            start_year, end_year, state_options)
        st.plotly_chart(fig)
        if show_df:
            st.dataframe(df)
            if len(repeats):
                st.write('Governors who have represented more than one state')
                st.dataframe(repeats)
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        "*Select one or more states to begin.*"
    if len(state_options) == 1:
        "State Based Terms"
        st.plotly_chart(state_terms(state_options[0]))
    else:
        "*Select only one State to get term visualization*"

name_options = st.sidebar.multiselect("Names", names_list, None)
with st.beta_expander("Timeline Visualized by Governors"):
    try:
        fig, df = timeline_name(start_year, end_year, name_options)
        st.plotly_chart(fig)
        if show_df:
            if len(df) > 1:
                st.dataframe(df)
    except Exception as e:
        "*Select one or more Governors to begin.*"
        traceback.print_tb(e.__traceback__)
