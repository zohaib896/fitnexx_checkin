import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Professional German Interface
st.set_page_config(page_title="Fitnexx Wellpass Log", page_icon="💪")
st.title("Fitnexx Check-in 📝")
st.markdown("### Digitales Wellpass-Logbuch (DSGVO-konform)")

with st.form("checkin_form", clear_on_submit=True):
    name = st.text_input("Vollständiger Name")
    firm = st.text_input("Firma / Arbeitgeber")
    submitted = st.form_submit_button("Einchecken")

    if submitted and name and firm:
        new_entry = {
            "Zeit": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Firma": firm
        }
        df = pd.DataFrame([new_entry])
        # Save locally in the cloud
        if not os.path.isfile('log.csv'):
            df.to_csv('log.csv', index=False)
        else:
            df.to_csv('log.csv', mode='a', header=False, index=False)
        st.success(f"Check-in erfolgreich! Viel Spaß beim Training, {name}.")

# Admin Section (Hidden in Sidebar)
st.sidebar.title("Admin")
pw = st.sidebar.text_input("Kennwort", type="password")
if pw == "fitnexx2026":
    if os.path.isfile('log.csv'):
        data = pd.read_csv('log.csv')
        st.sidebar.write("### Manager Area")
        st.sidebar.dataframe(data)

        # The Export Button
        st.sidebar.download_button("Excel Export (CSV)", data.to_csv(index=False), "wellpass_log.csv")

        # The Reset Button for the new month
        if st.sidebar.button("Clear List for New Month"):
            os.remove('log.csv')
            st.sidebar.success("The list has been cleared for the next month!")
            st.rerun()