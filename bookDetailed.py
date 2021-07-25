import requests as req
from bs4 import BeautifulSoup as Bs

#detailed book object
class BookDetailed:
    baseUrl = "http://libgen.rs/get?&md5="

    def __init__(self, queryUrl):
        self.bookUrl = self.baseUrl + queryUrl

    def parse(self):
        response = req.get(self.bookUrl).content

        obj = Bs(response, 'html.parser')

        downloadLink = obj.select("h2 a")
        description = obj.select("p+ div")
        resultDict = {}
        # if website is overloaded it returns a empty list
        if len(description) == 0 and len(downloadLink) == 0:
            book={}
            resultDict['result'] = "Server Overload"
            book['description'] = "Server Error.But you can download the book from the website by clicking below."
            book['download'] = "{}".format(self.bookUrl)
            resultDict['status'] = "500"
            resultDict['bookData']=book #added on 11th july
        else:
            book = {}
            for desc in description:
                book['description'] = desc.text.split("Description:")[1]
            for link in downloadLink:
                book['download'] = link['href']

            resultDict['bookData'] = book
            resultDict['result'] = "success"
            resultDict['status'] = "200"

        return resultDict
