from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df_st = pd.read_csv("data_small/stations.txt", skiprows=17)
df_st = df_st[["STAID", "STANAME                                 "]][:20]


@app.route("/")
def home():
    return render_template("home.html", data=df_st.to_html(index=False))


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == f"{date}"]["   TG"].squeeze()/10
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


@app.route("/api/v1/<station>")
def all_records(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df[:50].to_dict(orient="records")
    return result


@app.route("/api/v1/year/<station>/<year>")
def annual_data(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)
