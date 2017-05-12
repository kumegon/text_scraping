#coding:utf-8

import csv   #csvモジュールをインポートする
import re
import unicodedata

f = open('named_entity_report_csv_20170510_105557.csv', 'rU')

dataReader = csv.reader(f)
term = u'(([0-9０-９一二三四五六七八九十〇]*|数)(週間|時間|日|[かヶ]?月|年)(間|[.]*((前|頃|ころ)(から|より))))|([0-9０-９一二三四五六七八九十〇]+[歳才][.]*(から|より))|((今|去|昨|先)(晩|日|月|年)[.]*(から|より))'
for row in dataReader:
  text = ''.join(row[2:]).decode('utf-8')
  if re.findall(term,text):
    print(row[0] + ':' + re.search(term,text).group(0).encode('utf-8'))
