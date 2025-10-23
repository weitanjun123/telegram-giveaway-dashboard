import streamlit as st
import json
import pandas as pd

# === Load giveaway data from the same folder ===
def load_data():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"rounds": {}}

st.set_page_config(page_title="Giveaway Dashboard", page_icon="🎉", layout="wide")

st.title("🎁 Telegram Giveaway Dashboard")

data = load_data()

if not data["rounds"]:
    st.warning("No giveaway rounds found yet. Run your bot first!")
else:
    for round_name, round_data in data["rounds"].items():
        st.subheader(f"🏆 {round_name}")

        participants = round_data.get("participants", [])
        winners = round_data.get("winners", [])

        col1, col2 = st.columns(2)

        with col1:
            st.write("👥 **Participants:**")
            if participants:
                st.dataframe(pd.DataFrame(participants, columns=["Username"]))
            else:
                st.write("No participants yet.")

        with col2:
            st.write("🥇 **Winners:**")
            if winners:
                st.dataframe(pd.DataFrame(winners, columns=["Username"]))
            else:
                st.write("No winners yet.")

    st.success("✅ Data loaded successfully!")

if st.button("🔄 Refresh Data"):
    st.rerun()

# === 📤 Export CSV Button ===
if data["rounds"]:
    all_rows = []
    for round_name, round_data in data["rounds"].items():
        participants = ", ".join(round_data.get("participants", []))
        winners = ", ".join(round_data.get("winners", []))
        all_rows.append({
            "Round": round_name,
            "Participants": participants,
            "Winners": winners
        })

    df = pd.DataFrame(all_rows)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📤 Export Giveaway Data (CSV)",
        data=csv,
        file_name="giveaway_data.csv",
        mime="text/csv"
    )

