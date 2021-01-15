import json
import requests
import time


# Can be edited
keywords = [
    '알고리즘',
    '미적분학',
    '한국사',
    '토플',
    '토익스피킹',
    'ncs',
    'c#',
    'c++',
    '파이썬',
    '코틀린',
    '비트코인',
    '미분기하학',
    '집합론',
    '머신러닝',
    '텐서플로',
    '파이토치',
    'pytorch',
    'tensorflow',
    '수능',
    '정수론',
    'nlp',
    'java',
    'react',
    '역학',
    '유체역학',
    '전자기학',
    '통계학',
    '확률론',
    '조합론',
    '항공역학',
    '기하학',
    '자바',
    '자료구조',
    '네트워크',
    '데이터베이스',
    '일반화학',
    '일반물리',
    '유기화학',
    '인적성'
]


def query_and_save():
    url = "https://openapi.naver.com/v1/search/book.json?query="
    apikey = ""  # Write your naver api key here
    secret = ""  # Write your naver api secret key here
    header = {
        "X-Naver-Client-Id": apikey,
        "X-Naver-Client-Secret": secret
    }

    f = open('isbn.json', 'r')
    myisbn = json.load(f)
    f.close()

    for i in keywords:
        res = requests.get(url + i + '&display=100', headers=header)
        resbody = json.loads(res.text)
        for j in resbody['items']:
            try:
                isbn13 = j['isbn'].split(' ')[1]
            except:
                continue

            if isbn13 in myisbn:
                continue

            input = dict()
            input['title'] = j['title'].replace('<b>', '').replace('</b>', '')
            input['author'] = j['author'].replace('<b>', '').replace('</b>', '')
            input['publisher'] = j['publisher'].replace('<b>', '').replace('</b>', '')
            input['price'] = j['price']

            myisbn[isbn13] = input
        time.sleep(0.4)

    f = open('isbn.json', 'w', encoding='utf-8')
    f.write(json.dumps(myisbn, indent='  '))
    f.close()


if __name__ == "__main__":
    query_and_save()
