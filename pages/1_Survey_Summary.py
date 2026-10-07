from html import escape

import pandas as pd
import streamlit as st

from config import secret
from scoring import CAREERS
from storage import load_responses

st.set_page_config(page_title="Survey Summary", page_icon="📊", layout="centered")
st.html("""<style>
.hbar { margin: .2rem 0 .75rem; }
.hbar .top { display: flex; justify-content: space-between; font-weight: 600; }
.hbar .track { height: 12px; background: #E5E9F2; border-radius: 999px; overflow: hidden; margin-top: .25rem; }
.hbar .fill { height: 100%; border-radius: 999px; }
</style>""")


def bars(counts, colors=None):
    """Horizontal bars with full labels — st.bar_chart truncates long labels on phones."""
    total = max(counts.sum(), 1)
    rows = "".join(
        f'<div class="hbar"><div class="top"><span>{escape(str(label))}</span><span>{n} · {n * 100 // total}%</span></div>'
        f'<div class="track"><div class="fill" style="width:{n * 100 / total}%;background:{(colors or {}).get(label, "#1D4ED8")}"></div></div></div>'
        for label, n in counts.items())
    st.html(rows)

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
colors = {c["name"]["en"]: c["color"] for c in CAREERS.values()}
df["Top career area"] = df["top1"].map(names)

c1, c2, c3 = st.columns(3)
c1.metric("Students surveyed", len(df))
c2.metric("Schools", df["school"].nunique())
c3.metric("AI messages", f'{(df["source"] == "ai").mean():.0%}')

st.subheader("Top career area")
bars(df["Top career area"].value_counts(), colors)

st.subheader("Preferred route after Class 10")
bars(df["route"].value_counts().reindex(["SHORT", "MEDIUM", "LONG"], fill_value=0)
     .rename({"SHORT": "Short — skill, earn soon", "MEDIUM": "Medium — 12th + diploma/degree",
              "LONG": "Long — professional degree"}))

st.subheader("Top career area by class")
st.dataframe(pd.crosstab(df["Top career area"], df["grade"]).rename(columns=lambda g: f"Class {g}"))

st.subheader("All responses")
st.dataframe(df.drop(columns=["Top career area"]), hide_index=True)
st.download_button("Download CSV (opens in Excel)",
                   df.drop(columns=["Top career area"]).to_csv(index=False).encode("utf-8-sig"),
                   "survey_responses.csv", "text/csv")
