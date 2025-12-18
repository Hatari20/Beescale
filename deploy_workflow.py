import os

# --- 1. Create directories ---
os.makedirs(".github/workflows", exist_ok=True)

# --- 2. Write requirements.txt ---
with open("requirements.txt", "w") as f:
    f.write("""pandas
plotly
""")

# --- 3. Write plot.py ---
with open("plot.py", "w") as f:
    f.write("""import pandas as pd
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
""")

# --- 4. Write GitHub Actions workflow ---
with open(".github/workflows/plot.yml", "w") as f:
    f.write("""name: Update ESP32 Graph

on:
  schedule:
    - cron: '*/30 * * * *'   # every 30 minutes
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Generate Plot
        run: |
          python plot.py

      - name: Commit and push graph
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add graph.html
          git commit -m "Update graph [skip ci]" || echo "No changes"
          git push
""")

# --- 5. Initialize git if not already ---
if not os.path.exists(".git"):
    os.system("git init")
    os.system("git add .")
    os.system('git commit -m "Initial commit"')
    print("Git repository initialized. Now add remote and push manually if needed.")
else:
    os.system("git add .")
    os.system('git commit -m "Add workflow files" || echo "No changes"')
    print("Workflow files added and committed. Push to GitHub to deploy.")
