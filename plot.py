import pandas as pd
import plotly.express as px

sheet_url = "https://docs.google.com/spreadsheets/d/1YevAQ8w_BIZRZ_E2TfZh4e-4-ElVZRGXX49S_DvTirY/export?format=csv"

# Fetch the sheet
try:
    df = pd.read_csv(sheet_url, header=None)
    if df.empty:
        print("Sheet is empty! Exiting.")
        exit()
except Exception as e:
    print("Error fetching sheet:", e)
    exit()

# Name the first column "Timestamp"
df.columns = ["Timestamp"]

# Convert to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

# Add dummy value for plotting
df["Value"] = 1

# Plot
fig = px.scatter(df, x="Timestamp", y="Value", text="Timestamp",
                 title="ESP32 Data Over Time",
                 labels={"Value": "Dummy Value"})
fig.update_traces(marker=dict(size=8, color="red"),
                  textposition="top center")

# Save HTML
fig.write_html("graph.html")
print("Graph updated!")
