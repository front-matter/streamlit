import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, date
import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv();

st.title('Publications by Martin Fenner')

# ORCID ID does exist
API_KEY = os.environ.get("API_KEY")
ORCID = "0000-0003-1419-2405"

url = f'https://api.researchgraph.ai/v1/orcid/{ORCID}?subscription-key={API_KEY}'
r = requests.get(url)
print(r)
df = pd.DataFrame(r.json()[0]["nodes"]["publications"], columns=['doi', 'publication_year', 'title'])
df = df.dropna()
df = df.drop_duplicates(subset=['publication_year', 'title'])

plot_title = alt.TitleParams(f'{researcher["full_name"]} (ORCID {ORCID})', subtitle=['Publications by Year'])
alt.Chart(df, title=plot_title).mark_bar(color='#49B1F4').properties(width=500).encode(
    x=alt.X("publication_year:O", axis=alt.Axis(title='Publication Year', labelAngle=0, labelSeparation=10)),
    y=alt.Y("count:Q", impute=alt.ImputeParams(value=0, keyvals={"start": int(min(df['publication_year'].tolist())), "stop": datetime.now().year }), axis=alt.Axis(title=None))
).transform_aggregate(
    count='count(publication_year)',
    groupby=["publication_year"]
).configure_title(
    fontSize=18
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)