from flask import Flask, render_template, request, jsonify, Response
import mysql.connector

app = Flask(__name__, static_url_path='/static')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="novel_recommender"
)
        
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/get_title', methods = ['GET', 'POST'])
def get_title():
    if request.method == 'POST':
        title = request.form['book']
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT title FROM books WHERE books.title LIKE '%{title}%' LIMIT 20")
        myresult = mycursor.fetchall()
        
        titleList = []
        for book in myresult:
            titleList.append(book[0])
        
        return jsonify({
            "data": titleList
            })
    
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)