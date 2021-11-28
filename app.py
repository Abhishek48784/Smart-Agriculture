from flask import Flask, render_template,request
from flask.templating import render_template
import matplotlib 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def submit():
    detail = {}
    if request.method == "POST":
        state = request.form["state"]
        district = request.form["district"]
        season = request.form["season"]

        # actual processing code

        data = pd.read_csv("./crop-production.csv")
        data.fillna(method="ffill")
        df = data.loc[
            (data["State_Name"] == state)
            & (data["District_Name"] == district)
            & ((data["Season"] == season) | ((data["Season"] == "Whole Year")))
        ]
        gen_mean_prod = df.Production.mean()
        
        unique_crop = df.Crop.unique()
        production = np.array([])
        crop_name = np.array([])
        
        for i in unique_crop:
            dff = df.loc[df["Crop"] == i]
            mean_prod = dff.Production.mean()
            if mean_prod >= gen_mean_prod:
                detail[i] = mean_prod
                crop_name = np.append(crop_name, i)
                production = np.append(production, mean_prod)
        # pie char of crops in demand
        if pd.notna(gen_mean_prod):
            plt.pie(production, labels=crop_name)
            plt.show()

        # graph of production in a particular year 
        # d = df.Crop_Year.unique()
        # x = np.array([])
        # for i in d:
        #     x = np.append(x, i)
        # x.sort()
        # y = np.array([])
        # for i in x:
        #     y = np.append(y, data.loc[(data["Crop_Year"] == i)].Production.mean())
        # plt.xlabel("Years")
        # plt.ylabel("Production (Tons)")
        # plt.title("Production per year in district", size=13, color="blue")
        # plt.plot(x, y, marker="o", c="green", mfc="r")
        # plt.legend()
        # plt.show()
    return render_template('index.html',detail=detail)
    
@app.route("/about")
def about():
    return render_template('about.html',name='Abhi')

if __name__ == "__main__":
    app.run(debug=True)
