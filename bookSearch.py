import requests as req
from bs4 import BeautifulSoup as Bs

LIMIT = 25  # maximum number of results per page. values can be either 25,50,100 only


class BookSearch:
    # list of default values , if not parameters value are not provided
    baseUrl = "http://libgen.rs/search.php"
    query = 'abc'
    column = 'def'
    sort = 'def'
    orderBy = 'ASC'
    page = '1'

    def __init__(self, query, column, sort, sortOrder, page):
        # print(column)
        self.query = self.query if query is None else (query if " " not in query else query.replace(" ", "+"))
        self.column = self.column if column is None else column
        self.sort = self.sort if sort is None else sort
        self.orderBy = self.orderBy if sortOrder is None else sortOrder
        self.page = self.page if page is None else page
        self.searchUrl = self.baseUrl + "?&req=" + self.query + "&res=" + str(
            LIMIT) + "&phrase=1&view=detailed" + "&column=" + self.column + "&sort=" + self.sort + "&page=" + self.page + "&sortmode=" + self.orderBy
        # print(self.searchUrl)

    def parse(self):
        response = req.get(self.searchUrl).content
        obj = Bs(response, 'html.parser', from_encoding="utf-8")
        #print(obj)
        return self.extract(obj)

    def extract(self, obj):
        # BeautifulSoup operations to retrieve data from the tags
        allTitle = obj.select("td:nth-child(3) b a")
        allAuthor = obj.select("tr:nth-child(3) td+ td")
        allYear = obj.select("tr:nth-child(6) td:nth-child(2)")
        allLanguage = obj.select("tr:nth-child(7) td:nth-child(2)")
        allType = obj.select("tr:nth-child(10) td:nth-child(4)")
        allImage = obj.select("img", {"alt": "Download"})
        allPreLink = obj.select("tbody tr:nth-child(2) td:nth-child(1) a")
        allPagination = obj.select("#paginator_example_top~ table tr:nth-child(1) td:nth-child(1) font")
        totalFileCount, totalPageCount = self.splitTotal(allPagination)

        allPagesCount = obj.select("tr:nth-child(7) td:nth-child(4)")
        allSize = obj.select("tr:nth-child(10) td:nth-child(2)")
        allPublisher = obj.select("tr:nth-child(5) td:nth-child(2)")
       
        # iterating each value and appending them into lists after conversion
        titles = [t.text for t in allTitle]
        authors = [auth.text for auth in allAuthor]
        years = [year.text for year in allYear]
        langs = [lang.text for lang in allLanguage]
        types = [ext.text for ext in allType]
        images = ["http://libgen.rs" + img['src'] for img in allImage]
        prelinks = [link['href'].split("=")[1] for link in allPreLink]
        pagesCount = [pc.text for pc in allPagesCount]
        sizes = [self.sizeSplit(siz) for siz in allSize]
        publishers = [pub.text for pub in allPublisher]
        totalFileCount = len(titles) if totalFileCount<=25 else totalFileCount
        # JSON array containing all the resultant books
        allBooks = []
         # result as a Dictionary
        resultDict = {"status": 200, "result": "success", "totalFiles": totalFileCount, "totalPages": totalPageCount,
                      "limit": LIMIT}
        for i in range(len(titles)):
            # creating a book json object
            book = {"title": titles[i], "author": authors[i], "year": years[i], "language": langs[i], "type": types[i],
                    "image": images[i], "id": prelinks[i], "pages": pagesCount[i], "size": sizes[i],
                    "publisher": publishers[i]}
            # appending them into the JSON Array
            allBooks.append(book)
        resultDict["books"] = allBooks
        return resultDict

    def splitTotal(self, given):
        # print(given)
        if len(given) == 0:
            return 0, 0
        else:
            for string in given:
                return self.totalCompute(int(string.text.split(' ')[0]))

    def totalCompute(self, total):
        totMax = LIMIT if total // LIMIT >= LIMIT else total // LIMIT
        if not total % LIMIT == 0:
            print(totMax)
            return total, totMax + 1
        else:
            return total, totMax

    def sizeSplit(self, string):
        # just normal string operation
        arr = string.text.split(' ')
        result = arr[0] + " " + arr[1]
        return result


def defaultBookResult():
    # if the api request is invalid , returning the below object. dict['result'] is based on the uses
    resultDict = {'books': [], 'totalPages': 0, 'totalFiles': 0, 'limit': str(LIMIT), "status": 400}
    return resultDict
