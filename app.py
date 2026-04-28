import streamlit as st
from triage import triage

st.set_page_config(page_title="AI Incident Triage", layout="centered")

st.title("AI DevOps Triage Agent")

log_input = st.text_area("Paste your logs or error:")

if st.button("Analyze"):
    if log_input:
        with st.spinner("Analyzing..."):
            result = triage(log_input)

        st.subheader("Result")

        if "raw" in result:
            st.json(result)
        else:
            st.success(f"Category: {result['category']}")
            st.info(f"Root Cause: {result['root_cause']}")
            st.warning(f"Fix: {result['fix']}")