# imports
from flask import Flask, request, jsonify

from bookDetailed import BookDetailed
from bookSearch import BookSearch

app = Flask(__name__)


# routes
@app.route('/')
def home():
    return "<h1>home</h1>"


@app.route('/book')
def bookDetails():
    id = request.args.get("id")
    if id is None:
        return jsonify({"result": "Invalid url"})
    else:
        book = BookDetailed(str(id)).parse()
        return jsonify(book)


@app.route('/search')
def search():
    query=request.args.get("query")
    if query is None :
        return jsonify({"result":"invalid query, at least should be 3 characters"})
    column=request.args.get('queryBy') #def
    sort=request.args.get('sortby') #def
    sortMode=request.args.get('order') #ASC #desc
    page=request.args.get('page')
    books = BookSearch(str(query),column,sort,sortMode,page).parse()
    return jsonify(books)


if __name__ == "__main__":
    app.run(debug=True)
