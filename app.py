from pymongo import MongoClient
import streamlit as st
import pandas as pd
import altair as alt
import os
import argparse

## Yak shaving for getting connection uri from command line or from env variable.
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--uri")
args = parser.parse_args()

uri = args.uri or os.getenv("MONGO_URI")

if not uri:
    raise TypeError(
        """Missing MongoDB URI. Please eitehr pass it on command line using `--uri ...` or 
                    set the environment variable MONGO_URI."""
    )


## Demo Starts Here!

### Set page content title (markdown accepted!)
st.title("~Spice~ Data Is Life")

sample_size = st.slider("Sample Size", min_value=1, max_value=1000, value=256)

### Get data from MongoDB

db = MongoClient(uri).get_database("demo")

### Query out can be simple or a whole aggregation pipeline
docs = db["computers"].aggregate(
    [
        {"$sample": {"size": sample_size}},
        {
            "$project": {
                "date": "$in_service",
                "health": "$status",
                "make": "$computer.make",
                "model": {"$concat": ["$computer.make", "-", "$computer.model"]},
            }
        },
        {"$sample": {"size": sample_size}},
    ],
)

df = pd.DataFrame(docs)
st.write(df.shape)


if st.checkbox("Show data table?", value=False):
    st.write(df)


if st.checkbox("Show chart?", value=True):
    model = st.radio("Drill down", options=("make", "model"), horizontal=True)

    st.write(
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("health"),
            y=alt.Y(f"count({model})").scale(type="log", base=2),
            color=model,
        )
    )
