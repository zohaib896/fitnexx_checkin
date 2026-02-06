import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. SETTINGS & BRANDING ---
# This setup makes the app look professional for any gym
st.set_page_config(page_title="Gym Digital Logbuch", page_icon="💪")

# Using a generic title so you can show it to Fitnexx AND other gyms
st.title("Digitales Check-in System 📝")
st.markdown("### Partner-Programm Logbuch (DSGVO-konform)")

# --- 2. THE CHECK-IN FORM ---
with st.form("checkin_form", clear_on_submit=True):
    name = st.text_input("Vollständiger Name")

    # NEW: Dropdown to handle all partner apps in one place
    programm = st.selectbox("Programm auswählen", ["Egym Wellpass", "Hansefit", "Gympass", "Sonstiges"])

    firm = st.text_input("Firma / Arbeitgeber")

    submitted = st.form_submit_button("Einchecken")

    if submitted:
        if name and firm:
            new_entry = {
                "Zeit": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Programm": programm,
                "Name": name,
                "Firma": firm
            }
            df = pd.DataFrame([new_entry])

            # Save to the CSV file
            if not os.path.isfile('log.csv'):
                df.to_csv('log.csv', index=False)
            else:
                df.to_csv('log.csv', mode='a', header=False, index=False)

            st.success(f"Check-in für {programm} erfolgreich! Viel Spaß beim Training.")
        else:
            st.error("Bitte füllen Sie alle Felder aus.")

# --- 3. ADMIN / MANAGER SECTION ---
st.sidebar.title("Studio-Verwaltung")
st.sidebar.info("Passwortgeschützter Bereich für das Management.")

pw = st.sidebar.text_input("Kennwort eingeben", type="password")

# Using 'gym2026' as a generic password for your demos
if pw == "gym2026":
    st.sidebar.write("---")
    st.sidebar.subheader("Manager Bereich")

    if os.path.isfile('log.csv'):
        data = pd.read_csv('log.csv')
        st.sidebar.write("Aktuelle Check-ins (dieser Monat):")
        st.sidebar.dataframe(data)

        # Export Button
        csv = data.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Monatsliste Exportieren (CSV)",
            data=csv,
            file_name=f"gym_log_{datetime.now().strftime('%Y_%m')}.csv",
            mime='text/csv'
        )

        st.sidebar.write("---")
        # Danger Zone: Resetting the list
        if st.sidebar.button("Liste für neuen Monat löschen"):
            os.remove('log.csv')
            st.sidebar.success("Die Liste wurde erfolgreich gelöscht!")
            st.rerun()
    else:
        st.sidebar.info("Noch keine Check-ins vorhanden.")

elif pw != "":
    st.sidebar.error("Falsches Kennwort")