import glob
import pandas as pd
import json


def to_jsdate(s):
    ret = ''
    more = 0
    lt = s.split(' ')
    if lt[1] == "PM" and lt[2].split(':')[0] != '12':
        more = 12

    for i in range(len(lt[0])):
        if lt[0][i] == '/':
            ret += '-'
        else:
            ret += lt[0][i]

    clk = lt[2].split(':')
    ret += ' ' + str(int(clk[0]) + more) + ':' + clk[1] + ':' + clk[2]

    return ret


jsn = []
res = pd.DataFrame()

for i in glob.glob('*.xlsx'):
    df = pd.read_excel(i, skiprows=3, sheet_name='Sheet1').dropna(how='all').dropna(how='all', axis=1)
    print(df.shape)
    res = res.append(df, ignore_index=False)

res = res.drop_duplicates(keep=False)
res = res.loc[:, ~res.columns.str.contains('^Unnamed')]
# res.columns = ['scan_date', 'barcode', 'status', 'prefix_three', 'national_isbn', 'booknum_isbn', 'check_isbn', 'papernum_issn', 'check_issn', 'presymbol_issn', 'publisher', 'sign']

# for i in range(len(res)):
#     res['scan_date'].values[i] = tojsdate(res['scan_date'].values[i])

# print(res.shape)
# print(res.head())
#
# res.to_csv('/home/nicotina04/result.csv', index=False, sep=',', na_rep='NaN')

for i in range(len(res)):
    input = dict()
    if type(res.iloc[i, 0]) != str:
        break

    input["scan_date"] = to_jsdate(res.iloc[i, 0])
    try:
        input["id"] = str(int(res.iloc[i, 1]))
    except:
        input["id"] = str(res.iloc[i, 1])

    tmpbit = 0
    # 1번 : ISBN, 2번 : ISSN, 3번 : 국내책인가
    print(res.iloc[i, 2])
    if res.iloc[i, 2] is True:
        tmpbit = 1
    if res.iloc[i, 2] == '해외서적':
        tmpbit = 1
        tmpbit |= (1 << 2)
    if res.iloc[i, 2] == 'ISSN':
        tmpbit |= (1 << 1)
    input["status"] = tmpbit

    jsn.append(input)

f = open('db.json', 'w')
f.write(json.dumps(jsn, indent='  '))
f.close()
print(jsn)
