from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    # Drop duplicates and limit to 100 to prevent the browser from crashing
    all_books = books.drop_duplicates('Book-Title').head(100)
    return render_template('index.html',
                           book_name=list(all_books['Book-Title'].values),
                           author=list(all_books['Book-Author'].values),
                           image=list(all_books['Image-URL-M'].values)
                           )

@app.route('/popular')
def popular():
    # This is your old index route, now moved to its own tab
    return render_template('popular.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input').strip()

    if user_input not in pt.index:
        return render_template(
            'recommend.html',
            error="Book not found! Please enter a valid book title."
        )

    index = pt.index.get_loc(user_input)

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:5]

    data = []

    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')

        item = [
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ]

        data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)