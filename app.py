from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
client = MongoClient(mongo_uri)
db = client["books_db"]  # Database name
books_collection = db["books"]  # Collection name

# Initial books data
initial_books = [
    {
        "id": 0,
        "author": "chinua",
        "language": "english",
        "title": "Things fall apart",
    },
    {
        "id": 1,
        "author": "nikhil",
        "language": "telugu",
        "title": "fairy tales",
    },
    {
        "id": 2,
        "author": "prudhvi",
        "language": "urdu",
        "title": "ficciones",
    },
    {
        "id": 3,
        "author": "prudhvi",
        "language": "urdu",
        "title": "ficciones",
    },
    {
        "id": 4,
        "author": "nagaprudhvi",
        "language": "tamil",
        "title": "information",
    },
    {
        "id": 5,
        "author": "nagaprudhvi",
        "language": "tamil",
        "title": "information",
    },
]

# Function to initialize the database with initial books
def initialize_books():
    if books_collection.count_documents({}) == 0:
        books_collection.insert_many(initial_books)

initialize_books()  # Call the function to insert initial books

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == "GET":
        books = list(books_collection.find({}, {'_id': False}))  # Fetch all books, exclude '_id'
        if books:
            return jsonify(books)
        else:
            return "Nothing Found", 404

    if request.method == 'POST':
        new_book = {
            'author': request.json['author'],
            'language': request.json['language'],
            'title': request.json['title']
        }

        # Generate new ID based on the current highest ID
        highest_id = books_collection.find_one(sort=[("id", -1)])
        new_book['id'] = highest_id['id'] + 1 if highest_id else 0

        result = books_collection.insert_one(new_book)
        inserted_book = books_collection.find_one({'_id': result.inserted_id}, {'_id': False})
        return jsonify(inserted_book), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

