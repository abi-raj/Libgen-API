import requests as req
from bs4 import BeautifulSoup as Bs
from models.bookSearchModels import BookSearchModel, SearchResult

LIMIT = 25  # maximum number of results per page. values can be either 25,50,100 only


class BookSearch:
    # Default query parameter vaules
    baseUrl = "http://libgen.rs/search.php"
    query = 'abc'
    column = 'def'
    sort = 'def'
    orderBy = 'ASC'
    page = '1'

    def __init__(self, query, column, sort, sortOrder, page):

        """
        Applies the given query parameter vaules in the URL. If not provided, default ones are used.
        """
        
        self.query = self.query if query is None else (query if " " not in query else query.replace(" ", "+")) # book named 'Hello World' will be 'Hello+World'
        self.column = self.column if column is None else column
        self.sort = self.sort if sort is None else sort
        self.orderBy = self.orderBy if sortOrder is None else sortOrder
        self.page = self.page if page is None else page
        self.searchUrl = self.baseUrl + "?&req=" + self.query + "&res=" + str(
            LIMIT) + "&phrase=1&view=detailed" + "&column=" + self.column + "&sort=" + self.sort + "&page=" + self.page + "&sortmode=" + self.orderBy
        

    def parse(self): 

        """
        Request the page from web and convert it into a BeautifulSoup object.
        extract() function is then called to extract the required fields from the object.
        """

        response = req.get(self.searchUrl).content
        obj = Bs(response, 'html.parser', from_encoding="utf-8")
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

        # array containing all the resultant book objects
        allBooks = []
        
        for i in range(len(titles)):
            # creating a book object
            book = BookSearchModel (title=titles[i], author=authors[i], year=years[i], lang = langs[i], f_type=types[i], image=images[i],
                               b_id = prelinks[i], pages = pagesCount[i], size=sizes[i], pub = publishers[i])
            allBooks.append(vars(book))

        result = SearchResult(books = allBooks, totalPages = totalPageCount, totalFiles = totalFileCount, limit = LIMIT, status = 200)
        return vars(result)

    def splitTotal(self, given):
        
        if len(given) == 0:
            return 0, 0
        else:
            for string in given: # takin only the first tag
                return self.totalCompute(int(string.text.split(' ')[0])) # Example string.text = "89 files found"

    def totalCompute(self, total):
        """ Compute total number of pages that can be present """
        totMax = LIMIT if total // LIMIT >= LIMIT else total // LIMIT # the max number of pages for pagination is set to 25. if calculated value is lesser, that is taken.
        if not total % LIMIT == 0: 
            return total, totMax + 1 # 51 books % 25 per page =  2+1 pages 
        else:
            return total, totMax # 50 % 25 = 2

    def sizeSplit(self, string):

        arr = string.text.split(' ') # Example string = 3 Mb (2840045)
        result = arr[0] + " " + arr[1]
        return result


def defaultBookResult():
    # if the api request is invalid , returning the below object. dict['result'] is based on the uses
    resultDict = {'books': [], 'totalPages': 0, 'totalFiles': 0, 'limit': str(LIMIT), "status": 400}
    return resultDict
