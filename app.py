from flask import Flask, render_template, request, jsonify, Response
import pandas as pd
import re

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/get_title', methods=['GET', 'POST'])
def get_title():
    if request.method == 'POST':
        title = request.form['book']
        mask = books['Book-Title'].str.contains(title)
        myresult = books[mask]
        myresult = myresult.iloc[:99]
        titleList = []
        for book in myresult["Book-Title"]:
            titleList.append(book)

        return jsonify({
            "data": titleList
        })


@app.route('/get_recommend', methods=['GET', 'POST'])
def get_recommend():
    if request.method == 'POST':
        title = request.form['book']

        print(title)

        return jsonify({
            "data": "Data received"
        })


@app.route('/get_popular')
def get_popular():
    popular = popular_books(df)
    popList = []
    
    for i in range(len(popular["Book-Title"].tolist())):
        title = popular["Book-Title"].tolist()[i]
        url = df.loc[df["Book-Title"]==popular["Book-Title"].tolist()[i],"Image-URL-L"][:1].values[0]
        rating = round(df[df["Book-Title"]==popular["Book-Title"].tolist()[i]]["Book-Rating"].mean(),2)
        popList.append([title, rating, url])

    return jsonify({
        "data": popList
    })


def popular_books(df, n=4):
    rating_count = df.groupby(
        "Book-Title").count()["Book-Rating"].reset_index()
    rating_count.rename(columns={"Book-Rating": "NumberOfVotes"}, inplace=True)

    rating_average = df.groupby(
        "Book-Title")["Book-Rating"].mean().reset_index()
    rating_average.rename(
        columns={"Book-Rating": "AverageRatings"}, inplace=True)

    popularBooks = rating_count.merge(rating_average, on="Book-Title")

    def weighted_rate(x):
        v = x["NumberOfVotes"]
        R = x["AverageRatings"]

        return ((v*R) + (m*C)) / (v+m)

    C = popularBooks["AverageRatings"].mean()
    m = popularBooks["NumberOfVotes"].quantile(0.90)

    popularBooks = popularBooks[popularBooks["NumberOfVotes"] >= 250]
    popularBooks["Popularity"] = popularBooks.apply(weighted_rate, axis=1)
    popularBooks = popularBooks.sort_values(by="Popularity", ascending=False)
    return popularBooks.iloc[:n]


if __name__ == '__main__':
    books = pd.read_csv("model/data/Books.csv", delimiter=":::")
    ratings = pd.read_csv("model/data/Ratings.csv")
    users = pd.read_csv("model/data/Users.csv")

    books_data = books.merge(ratings, on="ISBN")
    df = books_data.copy()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=["Year-Of-Publication",
                     "Image-URL-S", "Image-URL-M"], axis=1, inplace=True)
    df.drop(index=df[df["Book-Rating"] == 0].index, inplace=True)
    df["Book-Title"] = df["Book-Title"].apply(
        lambda x: re.sub("[\W_]+", " ", x).strip())

    app.run(host="localhost", port=5000, debug=True)
