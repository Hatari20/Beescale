import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Google Sheet CSV export link ---
sheet_url = "https://docs.google.com/spreadsheets/d/1FpWyWsq2x3Wi3O4StBruyxllo32JwrcXfFr5gy5CAas/export?format=csv"

# Read sheet
df = pd.read_csv(sheet_url)

# Convert timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%Y-%m-%d %H:%M:%S")

# Add dummy value if missing
if 'Value' not in df.columns:
    df['Value'] = 1

# --- Plot ---
fig = px.scatter(df, x='Timestamp', y='Value', text='Timestamp',
                 title="ESP32 Data Over Time",
                 labels={"Value": "Dummy Value"})

fig.update_traces(marker=dict(size=8, color='red'),
                  textposition='top center')

# Save interactive HTML to repo
fig.write_html("graph.html")
print("Graph updated!")
