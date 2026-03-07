import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = "mwtmurphy-f1-rating-system"


@st.cache_resource
def _get_client() -> bigquery.Client:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return bigquery.Client(credentials=credentials, project=PROJECT_ID)


@st.cache_data(ttl=600)
def run_query(sql: str) -> pd.DataFrame:
    return _get_client().query(sql).to_dataframe()
