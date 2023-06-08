import requests as req
from bs4 import BeautifulSoup as Bs
from models.bookDetailedModel import BookDetailedModel, BookDetailedResult

class BookDetailed:
    baseUrl = "http://libgen.rs/get?&md5="

    def __init__(self, queryUrl):
        self.bookUrl = self.baseUrl + queryUrl

    def parse(self):
        response = req.get(self.bookUrl).content

        obj = Bs(response, 'html.parser')

        downloadLink = obj.select("h2 a")
        description = obj.select("p+ div")

        if len(description) == 0 and len(downloadLink) == 0:
            
            book = BookDetailedModel(description="Server Error.But you can download the book from the website by clicking below.", link = "{}".format(self.bookUrl))
            bookResult = BookDetailedResult(book = book, message = "Server Overload")

        else:
            
            for desc in description:
                desc = desc.text.split("Description:")[1]
            d_link = downloadLink[0]['href']
            book = BookDetailedModel(description = desc, link = d_link)
            bookResult = BookDetailedResult(book = book)

        return vars(bookResult)
