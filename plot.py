print("1. Starting... importing modules (this can take 10-20s on Pi/Zero)")
import requests
print("2. Requests imported. Importing Pandas...")
import pandas as pd
print("3. Pandas imported. Importing Plotly...")
import plotly.express as px
from io import StringIO
print("4. All imports done.")

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vREwRSmi8uPgu2glLQr1q8SFiquPADCfJW2NxeZcboY_-J0THzcJq8Q1yfklQ_cUha8f1RwApOYGWi_/pub?output=csv"

print("5. Attempting to download data from Google...")
try:
    # Reduced timeout to 5 seconds to force a fail if network is bad
    r = requests.get(sheet_url, timeout=5)
    r.raise_for_status()
    print("6. Download successful.")
except Exception as e:
    print(f"CRITICAL ERROR during download: {e}")
    exit()

csv_text = r.text
print(f"7. Data received.")

# Check for Google Login HTML trap
if "<!DOCTYPE html>" in csv_text or "<html" in csv_text[:100]:
    print("ERROR: Google returned a Login Page, not CSV. Check 'Publish to Web' settings.")
    exit()

print("8. Parsing CSV with Pandas...")
try:
    df = pd.read_csv(StringIO(csv_text), header=None)
    print(f"9. DataFrame created with shape: {df.shape}")
except Exception as e:
    print(f"Pandas Error: {e}")
    exit()

df.columns = ["Timestamp"]
print("10. Converting dates...")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df["Value"] = 1

print("11. Generating Plot...")

latest = df["Timestamp"].max().strftime("%Y-%m-%d %H:%M:%S")

fig = px.scatter(df, x="Timestamp", y="Value")

fig.update_layout(
    title=f"<b>Test Plot</b><br><sup>Last entry: {latest}</sup>"
)

print("12. Saving HTML file...")
fig.write_html("graph.html")
print("13. SUCCESS: Script finished.")