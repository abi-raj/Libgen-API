# Libgen-API

A simple **Flask** app which scrapes books and their download links from the popular ***[Library Genesis](http://libgen.rs/)*** website and returns the response.

### Installation

Install with pip:

```
$ pip install -r requirements.txt
$ python app.py
```
Visit : [http://127.0.0.1:5000/](#)

## Endpoints:
### Search:
1) Default:
```http
GET http://127.0.0.1:5000/api/default?query=flutter
```
2) Title:
```http
GET http://127.0.0.1:5000/api/title?query=Three.js Essentials
```
3) Author:
```http
GET http://127.0.0.1:5000/api/author?query=gayle laakmann mcdowell
```
4) Publisher:
```http
GET http://127.0.0.1:5000/api/publisher?query=oreilly
```
5) ISBN:
```http
GET http://127.0.0.1:5000/api/isbn?query=9780262032933
```
#### Common response:
```javascript
{
    "books": [
        {
            "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
            "id": "FD8631D3830BFA7A3D2D305A99A011F2",
            "image": "http://libgen.rs/covers/183000/ACAAA8958B27468B7286F4C577A967E2-d.jpg",
            "language": "English",
            "pages": "1202",
            "publisher": "The MIT Press",
            "size": "16 Mb",
            "title": "Introduction to algorithms",
            "type": "djvu",
            "year": "2001"
        },
    ],
    "limit": 25,
    "result": "success",
    "status": "200",
    "totalFiles": 1,
    "totalPages": 1
}
```
### Other search params:
1)sortBy = def,author,title,publisher<br>
2)orderBy = ASC,DESC<br>
3)page = 1,2,3.... (to total Pages available)<br>

Example:
```http
GET http://127.0.0.1:5000/api/title?query=node js&sortBy=title&orderBy=DESC&page=2
```
### Download link:
```http
GET http://127.0.0.1:5000/api/book?id=FD8631D3830BFA7A3D2D305A99A011F2
```
Response:

```javascript
{
    "bookData": {
        "description": "Explore what Flutter has to offer, where it came from, and where it’s going. Mobile development is progressing at a fast rate and with Flutter – an open-source mobile application development SDK created by Google – you can develop applications for Android and iOS, as well as Google Fuchsia.Learn to create three apps (a personal information manager, a chat system, and a game project) that you can install on your mobile devices and use for real.",
        "download": "http://31.42.184.140/main/2406000/227f03b36ad6b1b4c6c1af4ca444c27d/Frank%20Zammetti%20-%20Practical%20Flutter_%20Improve%20your%20Mobile%20Development%20with%20Google%E2%80%99s%20Latest%20Open-Source%20SDK-Apress%20%282019%29.pdf"
    },
    "result": "success",
    "status": "200"
}
```
