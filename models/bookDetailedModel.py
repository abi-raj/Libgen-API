class BookDetailedModel:
    def __init__(self, description, link):
        self.description = description
        self.download_link = link
        

class BookDetailedResult:
    def __init__(self, book, message = "success", status = 200,):
        self.bookData = vars(book)
        self.message = message
        self.status = status
        