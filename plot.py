import pandas as pd
import plotly.express as px

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vREwRSmi8uPgu2glLQr1q8SFiquPADCfJW2NxeZcboY_-J0THzcJq8Q1yfklQ_cUha8f1RwApOYGWi_/pub?output=csv"

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
