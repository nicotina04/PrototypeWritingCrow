import json
import requests
import time
import naverapi

url = "https://openapi.naver.com/v1/search/book_adv?d_isbn="
f = open('db.json', 'r')
jsn = json.load(f)
f.close()

book = dict()

for i in jsn:
    if (i['status'] & 1) == 0 or i['id'] in book.keys():
        continue
    isbn = i['id']

    res = requests.get(url + isbn, headers=naverapi.header)
    body = json.loads(res.text)
    print(body)
    book[isbn] = dict()

    try:
        info = body['items'][0]
        try:
            book[isbn]['title'] = info['title']
        except:
            book[isbn]['title'] = '정보 없음'
        try:
            book[isbn]['author'] = info['author']
        except:
            book[isbn]['author'] = '정보 없음'
        try:
            book[isbn]['publisher'] = info['publisher']
        except:
            book[isbn]['publisher'] = '정보 없음'
        try:
            book[isbn]['price'] = info['price']
        except:
            book[isbn]['price'] = '정보 없음'
    except:
        book[isbn]['title'] = '정보 없음'
        book[isbn]['author'] = '정보 없음'
        book[isbn]['publisher'] = '정보 없음'
        book[isbn]['price'] = '정보 없음'

    time.sleep(0.4)

f = open('isbn.json', 'w', encoding='utf-8')
f.write(json.dumps(book, indent='  '))
f.close()
