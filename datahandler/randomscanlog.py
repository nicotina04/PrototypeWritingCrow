import randomdate
import random as rd
import json
import re


def valid_isbn(s: str):
    pat = re.compile(
        '^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$'
    )

    if pat.match(s) is None:
        return 0
    else:
        return 1


class Scanlogger:
    def __init__(self, _start_year: int, _end_year: int, _start_month: int, _end_month: int, _path: str):
        self.start_year = _start_year
        self.end_year = _end_year
        self.start_month = max(1, _start_month)
        self.end_month = min(12, _end_month)
        self.path = _path

    def set_year(self, start: int, end: int):
        self.start_year = start
        self.end_year = end

    def get_year(self):
        return {"start": self.start_year, "end": self.end_year}

    def set_month(self, start: int, end: int):
        self.start_month = start
        self.end_month = end

    def get_month(self):
        return {"start": self.start_month, "end": self.end_month}

    def date_to_second(self, s: str):
        ret = 0
        d, c = s.split(' ')
        d = d.split('-')
        c = c.split(':')
        ret += int(d[0]) * 31284000
        ret += int(d[1]) * 2772000
        ret += int(d[2]) * 86400
        ret += int(c[0]) * 60 * 60
        ret += int(c[1]) * 60
        ret += int(c[2])
        return ret

    def generate_log(self, count: int = 1):
        f = open(self.path, 'r')
        myisbn = json.load(f)
        f.close()
        ret = []
        for i in range(count):
            tmp = dict()
            k = rd.choice(list(myisbn.keys()))

            tmp['scan_date'] = randomdate.generate_date(self.start_year, self.end_year, self.start_month, self.end_month)
            tmp['id'] = k
            tmp['status'] = valid_isbn(k)
            ret.append(tmp)
        return ret


if __name__ == "__main__":
    x = Scanlogger(2020, 2020, 7, 12, 'isbn.json')
    lt = x.generate_log(11000)

    f = open('db.json', 'r')
    res = json.load(f)
    f.close()
    res.extend(lt)
    res = sorted(res, key=lambda e: x.date_to_second(e['scan_date']))
    f = open('db.json', 'w')
    f.write(json.dumps(res, indent='  '))
