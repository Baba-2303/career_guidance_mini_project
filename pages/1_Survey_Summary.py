import pandas as pd
import streamlit as st

from config import secret
from scoring import CAREERS
from storage import load_responses

st.set_page_config(page_title="Survey Summary", page_icon="📊", layout="centered")
st.page_link("app.py", label="Back to survey", icon=":material/arrow_back:")
st.title("Survey Summary")

password = secret("SUMMARY_PASSWORD")
if password and not st.session_state.get("summary_ok"):
    entered = st.text_input("Volunteer password", type="password")
    if entered != password:
        if entered:
            st.error("Wrong password.")
        st.stop()
    st.session_state.summary_ok = True

try:
    df = load_responses()
except Exception as e:
    st.error(f"Could not load responses: {e}")
    st.stop()

if df.empty:
    st.write("No responses yet.")
    st.stop()

names = {code: c["name"]["en"] for code, c in CAREERS.items()}
df["Top career area"] = df["top1"].map(names)

c1, c2, c3 = st.columns(3)
c1.metric("Students surveyed", len(df))
c2.metric("Schools", df["school"].nunique())
c3.metric("AI messages", f'{(df["source"] == "ai").mean():.0%}')

st.subheader("Top career area")
st.bar_chart(df["Top career area"].value_counts(), horizontal=True)

st.subheader("Preferred route after Class 10")
st.bar_chart(df["route"].value_counts().reindex(["SHORT", "MEDIUM", "LONG"], fill_value=0))

st.subheader("Top career area by class")
st.bar_chart(pd.crosstab(df["Top career area"], df["grade"]), horizontal=True)

st.subheader("All responses")
st.dataframe(df.drop(columns=["Top career area"]), hide_index=True)
st.download_button("Download CSV (opens in Excel)",
                   df.drop(columns=["Top career area"]).to_csv(index=False).encode("utf-8-sig"),
                   "survey_responses.csv", "text/csv")
