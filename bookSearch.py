import requests as req
from bs4 import BeautifulSoup as Bs


class BookSearch:
    baseUrl = "http://libgen.rs/search.php"
    query = 'abc'
    column = 'def'
    sort = 'def'
    sortMode = 'ASC'
    page = '1'

    def __init__(self, query, column, sort, sortMode, page):
        self.query = self.query if query is None else (query if " " not in query else query.replace(" ", "+"))
        self.column = self.column if column is None else column
        self.sort = self.sort if sort is None else sort
        self.sortMode = self.sortMode if sortMode is None else sortMode
        self.page = self.page if page is None else page
        self.searchUrl = self.baseUrl + "?&req=" + self.query + "&res=25&phrase=1&view=detailed" + "&column=" + self.column + "&sort=" + self.sort + "&sortmode=" + self.sortMode + "&page=" + self.page

    def parse(self):
        response = req.get(self.searchUrl).content
        obj = Bs(response, 'html.parser', from_encoding="utf-8")
        return self.extract(obj)

    def extract(self, obj):

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

        # titles=authors=years=langs=types=images=prelinks=pagesCount=sizes=publishers=[]
        resultDict = {}
        resultDict["result"] = "OK"
        resultDict["totalFiles"] = totalFileCount
        resultDict["totalPages"] = totalPageCount
        titles = [t.text for t in allTitle]
        authors = [auth.text for auth in allAuthor]
        years = [year.text for year in allYear]
        langs = [lang.text for lang in allLanguage]
        types = [ext.text for ext in allType]
        images = ["http://libgen.rs"+img['src'] for img in allImage]
        prelinks = [link['href'].split("=")[1] for link in allPreLink]
        pagesCount = [pc.text for pc in allPagesCount]
        # print(allSize)
        sizes = [self.sizeSplit(siz) for siz in allSize]
        publishers = [pub.text for pub in allPublisher]
        allBooks = []
        for i in range(len(titles)):
            book = {}
            book["title"] = titles[i]
            book["author"] = authors[i]
            book["year"] = years[i]
            book["language"] = langs[i]
            book["type"] = types[i]
            book["image"] = images[i]
            book["id"] = prelinks[i]
            book["pages"] = pagesCount[i]
            book["size"] = sizes[i]
            book["publisher"] = publishers[i]
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
        if not total % 25 == 0:
            totMax = 25 if total // 25 >= 25 else total // 25
            print(totMax)
            return total, totMax + 1
        else:
            totMax = 25 if total // 25 >= 25 else total // 25
            return total, totMax

    def sizeSplit(self, string):
        arr = string.text.split(' ')
        result = arr[0] + " " + arr[1]
        #  print(result)
        return result
