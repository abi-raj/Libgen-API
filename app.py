# imports
from flask import Flask, request, jsonify

from bookDetailed import BookDetailed
from bookSearch import BookSearch, defaultBookResult

app = Flask(__name__)


def defaultParams():
    sortBy = request.args.get('sortBy')
    orderBy = request.args.get('order')
    page = request.args.get('page')
    return {"sortBy": sortBy, "orderBy": orderBy, "page": page}


# routes
@app.route('/')
def home():
    return "<h1>home</h1>"





@app.route('/api/default')
def search():
    query = request.args.get("query")
    other_params = defaultParams()
    if query is None:
        return jsonify({"result": "invalid query, at least should be 3 characters"})
    books = BookSearch(str(query), None, other_params['sortBy'], other_params['orderBy'], other_params['page']).parse()
    return jsonify(books)


@app.route('/api/title')
def titleSearch():
    title = request.args.get('query')
    other_params = defaultParams()
    # validating
    if title is None or len(title) < 2:
        resultDict = defaultBookResult()
        resultDict['result'] = "Title should be at-least 2 characters"
        return resultDict
    books = BookSearch(str(title), 'title', other_params['sortBy'], other_params['orderBy'], other_params['page']).parse()
    return jsonify(books)


@app.route('/api/author')
def authorSearch():
    author = request.args.get('query')
    other_params = defaultParams()
    # validating
    if author is None or len(author) < 2:
        resultDict = defaultBookResult()
        resultDict['result'] = "Author name should be at-least 2 characters"
        return resultDict
    books = BookSearch(str(author), 'author', other_params['sortBy'], other_params['orderBy'],
                       other_params['page']).parse()
    return jsonify(books)


@app.route('/api/publisher')
def publisherSearch():
    publisher = request.args.get('query')
    other_params = defaultParams()
    # validating
    if publisher is None or len(publisher) < 2:
        resultDict = defaultBookResult()
        resultDict['result'] = "Publisher name should be at-least 2 characters"
        return resultDict
    books = BookSearch(str(publisher), 'publisher', other_params['sortBy'], other_params['orderBy'],
                       other_params['page']).parse()
    return jsonify(books)


@app.route('/api/isbn')
def isbnSearch():
    isbn_number = request.args.get('query')

    other_params = defaultParams()
    if len(isbn_number) == 10 or len(isbn_number) == 13:  # validating the ISBN number
        books = BookSearch(str(isbn_number), 'identifier', other_params['sortBy'], other_params['orderBy'],
                       other_params['page']).parse()
        return jsonify(books)
    else:
        resultDict = defaultBookResult()
        resultDict['result'] = "Enter a Valid ISBN number"
        return resultDict

@app.route('/api/book')  # query parameter - id
def bookDetails():
    id = request.args.get("id")
    if id is None:
        resultDict = {}
        resultDict['result'] = 'Invalid id'
        resultDict['description'] = 'none'
        resultDict['download'] = 'none'
        return jsonify(resultDict)
    else:
        book = BookDetailed(str(id)).parse()
        return jsonify(book)

if __name__ == "__main__":
    app.run(debug=True)
