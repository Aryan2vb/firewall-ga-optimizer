from flask import Flask, render_template, send_from_directory
import os
import pandas as pd

app = Flask(__name__)

PLOT_DIR = "results/plots"
RULES_PATH = "data/processed/firewall_rules.csv"   # update with your actual file
rules_df = pd.read_csv(RULES_PATH)

@app.route("/")
def dashboard():
    plots = os.listdir(PLOT_DIR)
    plots = [f for f in plots if f.endswith(".png")]

    # TOP 20 RULES for table
    top20 = rules_df.sort_values("HitCount", ascending=False).head(20)
    top20_rules = top20.to_dict(orient="records")

    return render_template("dashboard.html", plots=plots,top_rules=top20_rules)

@app.route("/plots/<filename>")
def plot_file(filename):
    return send_from_directory(PLOT_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
