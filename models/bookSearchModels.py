class BookSearchModel:
    def __init__(
        self, title, author, year, lang, f_type, image, b_id, pages, size, pub
    ):

        self.title = title
        self.author = author
        self.year = year
        self.language = lang
        self.file_type = f_type
        self.image = image
        self.book_id = b_id
        self.pages = pages
        self.size = size
        self.publisher = pub


class SearchResult:
    def __init__(
        self,
        books=[],
        totalPages=0,
        totalFiles=0,
        limit=25,
        status=404,
        message="success",
    ):

        self.books = books
        self.totalPages = totalPages
        self.totalFiles = totalFiles
        self.limit = limit
        self.status = status
        self.message = message
