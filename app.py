# In the last module, we added code to allow users to add books to our store

# In this module, we will go ahead and start adding code to allow users to update books already
# in our store

from flask import Flask, jsonify, json, request, Response
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
connection = psycopg2.connect(user="postgres",
                                      password="pg@123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
cursor = connection.cursor(cursor_factory=RealDictCursor)

def retrieve_pgaccount():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="pg@123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        # Print PostgreSQL Connection properties
        # print(connection.get_dsn_parameters(), "\n")
        #
        # # Print PostgreSQL version
        cursor.execute("SELECT * from public.\"account\"")
        record = json.dumps(cursor.fetchall(), indent=2)
        print("record is - ", record, "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)



books = [
    {
        'name': 'A',
        'price': 7.99,
        'isbn': 9780394800165
    },
    {
        'name': 'B',
        'price': 6.99,
        'isbn': 9792371000193
    },
    {
        'name': 'C',
        'price': 7.99,
        'isbn': 9800394800165
    },
    {
        'name': 'D',
        'price': 6.99,
        'isbn': 9812371000193
    },
    {
        'name': 'E',
        'price': 7.99,
        'isbn': 9820394800165
    },
    {
        'name': 'F',
        'price': 6.99,
        'isbn': 9832371000193
    },
    {
        'name': 'G',
        'price': 7.99,
        'isbn': 9840394800165
    },
    {
        'name': 'H',
        'price': 6.99,
        'isbn': 9852371000193
    },
    {
        'name': 'I',
        'price': 7.99,
        'isbn': 9860394800165
    },
    {
        'name': 'K',
        'price': 6.99,
        'isbn': 9872371000193
    },
    {
        'name': 'L',
        'price': 7.99,
        'isbn': 9880394800165
    },
    {
        'name': 'M',
        'price': 6.99,
        'isbn': 9892371000193
    },
    {
        'name': 'N',
        'price': 7.99,
        'isbn': 9900394800165
    },
    {
        'name': 'O',
        'price': 6.99,
        'isbn': 9912371000193
    },
    {
        'name': 'P',
        'price': 7.99,
        'isbn': 9920394800165
    },
    {
        'name': 'Q',
        'price': 6.99,
        'isbn': 9932371000193
    },
    {
        'name': 'R',
        'price': 7.99,
        'isbn': 9940394800165
    },
    {
        'name': 'S',
        'price': 6.99,
        'isbn': 9952371000193
    }
]

DEFAULT_PAGE_LIMIT = 3;


# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)


# GET /books/page/<int:page_number>
@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
    return jsonify({'books': books[page_number * LIMIT - LIMIT:page_number * LIMIT]})


def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 9780394800165 }"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response;

# PUT /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    pass

#route to retrieve psql data
@app.route('/accVal', methods=['GET'])
def retrieve_pgaccount():
    print(connection.get_dsn_parameters(), "\n")
    cursor.execute("SELECT * from public.\"account\"")
    record = json.dumps(cursor.fetchall(), indent=2)
    print("record is - ", record, "\n")
    return record;

#app port
app.run(port=5000)

