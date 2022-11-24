from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
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
        mask = books['title'].str.contains(f".{title}.", flags=re.IGNORECASE)
        myresult = books[mask]
        titleList = []
        
        for book in myresult["title"]:
            titleList.append(book)

        return jsonify({
            "data": titleList
            })


@app.route('/get_recommend', methods=['GET', 'POST'])
def get_recommend():
    if request.method == 'POST':
        title = request.form['book']
        mode = request.form['mode']

        if mode == '1':
            result = content_based(title)
        elif mode == '2':
            result = item_based(title)
        
        recommend = result["data"]
        recList = []
        if recommend != None:
            for i in range(len(recommend)):
                title = recommend[i]
                url = df.loc[df["title"]==recommend[i],"image_l"][:1].values[0]
                rating = round(df[df["title"]==recommend[i]]["Book-Rating"].mean(),2)
                recList.append([title, rating, url])
        
        return jsonify({
            "book-status": result["status"],
            "data": recList
        })


@app.route('/get_popular')
def get_popular():
    popular = popular_books(df)
    popList = []
    
    for i in range(len(popular["title"].tolist())):
        title = popular["title"].tolist()[i]
        url = df.loc[df["title"]==popular["title"].tolist()[i],"image_l"][:1].values[0]
        rating = round(df[df["title"]==popular["title"].tolist()[i]]["Book-Rating"].mean(),2)
        popList.append([title, rating, url])

    return jsonify({
        "data": popList
    })


def popular_books(df, n=4):
    rating_count = df.groupby(
        "title").count()["Book-Rating"].reset_index()
    rating_count.rename(columns={"Book-Rating": "NumberOfVotes"}, inplace=True)

    rating_average = df.groupby(
        "title")["Book-Rating"].mean().reset_index()
    rating_average.rename(
        columns={"Book-Rating": "AverageRatings"}, inplace=True)

    popularBooks = rating_count.merge(rating_average, on="title")

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


def content_based(bookTitle):
    bookTitle = str(bookTitle)

    if bookTitle in df["title"].values:
        rating_count = pd.DataFrame(df["title"].value_counts())
        rare_books = rating_count[rating_count["title"] <= 200].index
        common_books = df[~df["title"].isin(rare_books)]

        if bookTitle in rare_books:
            most_common = pd.Series(
                common_books["title"].unique()).sample(4).values
            return {"status": "rare", "data": most_common.tolist()}
        else:
            common_books = common_books.drop_duplicates(subset=["title"])
            common_books.reset_index(inplace=True)
            common_books["index"] = [i for i in range(common_books.shape[0])]
            targets = ["title", "author", "publisher"]
            common_books["all_features"] = [" ".join(
                common_books[targets].iloc[i, ].values) for i in range(common_books[targets].shape[0])]
            vectorizer = CountVectorizer()
            common_booksVector = vectorizer.fit_transform(
                common_books["all_features"])
            similarity = cosine_similarity(common_booksVector)
            index = common_books[common_books["title"]
                                 == bookTitle]["index"].values[0]
            similar_books = list(enumerate(similarity[index]))
            similar_booksSorted = sorted(
                similar_books, key=lambda x: x[1], reverse=True)[1:6]
            books = []
            for i in range(len(similar_booksSorted)):
                books.append(common_books[common_books["index"] ==
                             similar_booksSorted[i][0]]["title"].item())

            return {"status": "normal", "data": books[:4]}

    else:
        return {"status": "na", "data": None}


def item_based(bookTitle):
    bookTitle = str(bookTitle)

    if bookTitle in df["title"].values:
        rating_count = pd.DataFrame(df["title"].value_counts())
        rare_books = rating_count[rating_count["title"] <= 200].index
        common_books = df[~df["title"].isin(rare_books)]

        if bookTitle in rare_books:
            most_common = pd.Series(
                common_books["title"].unique()).sample(4).values
            return {"status": "rare", "data": most_common.tolist()}
        else:
            common_books_pivot = common_books.pivot_table(
                index=["User-ID"], columns=["title"], values="Book-Rating")
            title = common_books_pivot[bookTitle]
            recommendation_df = pd.DataFrame(common_books_pivot.corrwith(
                title).sort_values(ascending=False)).reset_index(drop=False)

            if bookTitle in [title for title in recommendation_df["title"]]:
                recommendation_df = recommendation_df.drop(
                    recommendation_df[recommendation_df["title"] == bookTitle].index[0])
            less_rating = []
            for i in recommendation_df["title"]:
                if df[df["title"] == i]["Book-Rating"].mean() < 5:
                    less_rating.append(i)
            if recommendation_df.shape[0] - len(less_rating) > 5:
                recommendation_df = recommendation_df[~recommendation_df["title"].isin(
                    less_rating)]

            recommendation_df = recommendation_df[0:5]
            recommendation_df.columns = ["title", "Correlation"]
            ret = recommendation_df["title"].tolist()
            return {"status": "normal", "data": ret[:4]}
    else:
        return {"status": "na", "data": None}

if __name__ == '__main__':
    books = pd.read_csv("model/data/book-new.csv", delimiter='\t')
    books.rename(columns= {'isbn':'ISBN'}, inplace=True)
    ratings = pd.read_csv("model/data/Ratings.csv")
    
    books_data = books.merge(ratings, on="ISBN")
    df = books_data.copy()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=["publication_year",
                     "image_s", "image_m"], axis=1, inplace=True)
    df.drop(index=df[df["Book-Rating"] == 0].index, inplace=True)
    df["title"] = df["title"].apply(
        lambda x: re.sub("[\W_]+", " ", x).strip())

    app.run(host="localhost", port=5000, debug=True)
