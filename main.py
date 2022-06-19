from flask import Flask, redirect, url_for, render_template, request, flash
import pandas as pd
from numpy import nan

app = Flask(__name__)


def calc(df, currency):
    df = df.fillna(0)
    weightsum = 0
    pricebyweight = 0
    for index, row in df.iterrows():
        if row["Credit Currency"] == currency:
            weightsum += row["Amount Debited"]
            pricebyweight += (row["Amount Debited"] * row["Buy / Sell Rate"])
        # if row["Debit Currency"] == currency:
        #     weightsum -= row["Amount Credited"]
        #     pricebyweight -= (row["Amount Credited"] * row["Buy / Sell Rate"])

    return pricebyweight / weightsum


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == '':
            return render_template("index.html", error="No File Selected")
        if not file.filename.endswith('.csv'):
            return render_template("index.html", error="Incorrect file type, please submit .csv")
        df = pd.read_csv(file)
        if not ("Transaction Type" in df) or not ("Amount Debited" in df) or not ("Amount Credited" in df) or not ("Credit Currency" in df) or not ("Buy / Sell Rate" in df):
            return render_template("index.html", error = "Incorrect File Type, ensure you are using file from shakepay")
        btc_val = calc(df, "BTC")
        eth_val = calc(df, "ETH")
        return render_template("index.html", btc=f"Your average BTC rate is: {btc_val}", eth=f"Your average ETH rate is: {eth_val}")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
