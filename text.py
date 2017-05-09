#!/usr/bin/python
# coding: UTF-8
import re
import unicodedata
import csv

'''
出力ファイルは
age_from,age_to,gender,relation,original_text
gender = {1:male, 2:female, -1:unknown}
relation = {1:自分, 2:配偶者, 3:子, 4:親, 5:祖父母, 6:孫, 7:義父母, 8:恋人, 9:知人・友人}
'''

f = open("person.txt")
lines = f.readlines()
f.close()

def str2int(s
        , piriod='.'    #小数点:[u'.', u'・', u'٫', u'・']
        , comma=','     #桁区切:[u',', u'٬', u'，', u' ', u'.', u'、']
        ):
    """
    漢数字、全角数字、半角数字文字列の整数化
    【仕様】
     1. 拾, 百, 千, 万, 億等が数字の頭にあるときは頭の一が省略されたものと看做す
     2. 数字でない余計な文字を含まないこと(現在は、含むと単にpassする)
        「、・」等をはさんでいる場合の解釈をどうするか詰めてから対処の予定
    """
    #千以下の相対位の刻み
    kizami_dic = {u'拾':10,u'十':10
                , u'百':100, u'陌':100, u'佰':100
                , u'千':1000, u'阡':1000, u'仟':1000}
    #万以上の絶対位
    kurai_dic = { u'万':10000, u'萬':10000
                , u'億':100000000
                , u'兆':1000000000000
                , u'京':10000000000000000
                , u'垓':100000000000000000000
                , u'予':1000000000000000000000000
                , u'穣':10000000000000000000000000000
                , u'溝':100000000000000000000000000000000
                , u'潤':1000000000000000000000000000000000000
                , u'正':10000000000000000000000000000000000000000}
    # 10進数の数字0～9に当たる全文字に対する整数値の辞書
    knum_dic = {  '0':0, '1':1, '2':2, '3':3, '4':4
                , '5':5, '6':6, '7':7, '8':8, '9':9
                , u'０':0, u'１':1, u'２':2, u'３':3, u'４':4
                , u'５':5, u'６':6, u'７':7, u'８':8, u'９':9
                #漢数字
                , u'〇':0, u'一':1, u'二':2, u'三':3, u'四':4
                , u'五':5, u'六':6, u'七':7, u'八':8, u'九':9
                , u'〇':0, u'壱':1, u'弐':2, u'参':3
                #日本の旧大字
                , u'零':0, u'壹':1, u'貮':2, u'貳':2, u'參':3
                , u'肆':4, u'伍':5, u'陸':6, u'柒':7, u'漆':7
                , u'質':7, u'捌':8, u'玖':9
                #中国の大字
                , u'零':0, u'壹':1, u'贰':2, u'貳':2, u'叁':3, u'參':3
                , u'肆':4, u'伍':5, u'陆':6, u'陸':6
                , u'柒':7, u'柒':7, u'漆':7, u'捌':8, u'玖':9
                #アラビア・インド数字
                , u'٠':0, u'١':1 , u'٢':2, u'٣':3, u'٤':4
                , u'٥':5, u'٦':6 , u'٧':7, u'٨':8, u'٩':9
                #タイ数字
                , u'๐':0, u'๑':1, u'๒':2, u'๓':3, u'๔':4
                , u'๕':5, u'๖':6, u'๗':7, u'๘':8, u'๙':9
                }
    r = reverse(s)                          #末尾文字から解釈するので文字列を反転
    ketaage = k3 = k4 = 1                   #各桁上げ変数を1に初期化
    n = 0                                   #桁刻みの数の計算用
    p = ''                                  #次の処理の為一つ前の文字の区分を記録
    for i in r:                             #末尾より一文字ずつ
        if i in knum_dic:                   #  漢数字0～9なら
            if p=='n':                      #    もし、一つ前もそうなら
                ketaage *= 10               #      kizamiに依存せず一桁上げ
                n += (k3 * k4 * ketaage     #      拾百千の桁刻みが省かれているものとして
                            * knum_dic[i])  #      一桁桁上げして加算
            else:                           #    でないなら
                n += k3 * k4 * knum_dic[i]  #      万以上の位と千以下の刻みをかけて加算
            p = 'n'                         #    次の処理の為一つ前が数字文字だったと記録
        elif i in kizami_dic:               #  千百十の刻みなら
            k3 = kizami_dic[i]              #    千以下の刻み桁数を代入: 千=1000, 百=100, 拾=10
            ketaage = 1                     #    漢数字0～9連続時の桁上げをクリア
            p = 'z'                         #    次の処理の為一つ前が千以下の刻み文字だったと記録
        elif i in kurai_dic:                #  万以上の絶対位の文字なら
            k4 = kurai_dic[i]               #    万以上の絶対位の桁数を代入: 万=10000
            k3 = 1                          #    千以下の刻み桁数をクリア
            ketaage = 1                     #    漢数字0～9連続時の桁上げをクリア
            p = 'k'                         #    次の処理の為一つ前が万以上の位文字だったと記録
        else:                               #  それ以外は
            return -1        #    取り敢えず、画面表示してpassしておく …(2)
    if p=='z' or p=='k':                    #最後の未処理分は
        n += k3 * k4                        #  頭の一が省略されたものと看做し処理     …(1)
    return n                                #結果を返す

def reverse(s):
    """Unicode文字列用の降順並替関数(python2.x系のunicode型にはreverse()メソッドがない)"""
    st = list(s)      #いきなりlist化
    st.reverse()
    return u''.join(st)


def which_gender(line):
  female = u'母|娘|女|妻'
  male = u'父|息子|男|夫|主人'
  if re.findall(female, line):
    return 2
  elif re.findall(male, line):
    return 1
  else:
    return -1

def which_rel(line):
  rel = {1:u"自分", 2:u"妻|主人|夫", 3:u"子|娘", 4:u"父|母", 5:u"祖", 6:u"孫", 7:u"義", 8:u"恋|彼", 9:u"知人|友"}
  for i in range(2,10):
    if re.findall(rel[i], line):
      return i
  return 1

def get_grade(str):
  number = u'[1-6１-６一二三四五六]'
  if re.findall(number, str):
    return str2int(re.findall(number, str)[0]) - 1
  else:
    return -1

def get_range_grade(str):
  low = u'低'
  middle = u'中'
  high = u'高'
  if re.findall(low, str):
    return 2
  elif re.findall(middle, str):
    return 4
  elif re.findall(high, str):
    return 6
  else:
    return 0



def get_number(str):
  return str.split(u'代')[0].split(u'歳')[0].split(u'才')[0]

def range_age(line):
  age1 = u'[0-9０-９一二三四五六七八九十〇]+[歳才]?代'
  age2 = u'[0-9０-９一二三四五六七八九十〇]+[歳才]'
  age_from = 0
  age_to = 0
  if re.findall(age1, line):
    age_from = str2int(get_number(re.findall(age1,line)[0]))
    former = u'前'
    latter = u'後'
    middle = u'半'
    if re.findall(former, line):
      print('前')
      age_to = age_from + 4
    elif re.findall(latter, line):
      print('後')
      age_from += 5
      age_to = age_from + 4
    elif re.findall(middle, line):
      print('半')
      age_from += 3
      age_to = age_from + 5
    else:
      age_to = age_from + 9
  elif re.findall(age2, line):
    age_from = str2int(get_number(re.findall(age2,line)[0]))
    age_to = age_from
  elif re.findall(u'高',line):
    age_from = 16
    grade = get_grade(line)
    if grade >= 0:
      age_to = age_from + grade
      age_from = age_to
    else:
      age_to = 18
  elif re.findall(u'中',line):
    age_from = 13
    grade = get_grade(line)
    if grade >= 0:
      age_to = age_from + grade
      age_from = age_to
    else:
      age_to = 15
  elif re.findall(u'小',line):
    age_from = 7
    grade = get_grade(line)
    range_grade = get_range_grade(line)
    if grade >= 0:
      age_to = age_from + grade
      age_from = age_to
    elif range_grade > 0:
      age_to = age_from + range_grade
      age_from = age_to - 2
    else:
      age_to = 12
  elif re.findall(u'幼稚園|保育園',line):
    age_from = 3
    age_to = 6
  elif re.findall(u'月',line):
    age_from = 0
    age_to = 1
  elif re.findall(u'年[生]?', line):
    if(re.findall(u'[1-6１-６一二三四五六]', line)):
      grade = str2int(re.findall(u'[1-6１-６一二三四五六]', line)[0])
      age_from = 6 + grade
      age_to = age_from
    else:
      age_from = -1
      age_to = -1
  elif re.findall(u'成人', line):
    age_from = 20
    age_to = -1
  else:
    age_from = -1
    age_to = -1
  return [age_from, age_to]


g = open('person.csv','wb')
writer = csv.writer(g, lineterminator='', quoting=csv.QUOTE_NONE)
for line in map(lambda x: x.decode("utf-8"),lines):
  age = range_age(line)
  gender = which_gender(line)
  rel = which_rel(line)
  tup = [age[0],age[1],gender,rel,line.encode('utf-8')]
  writer.writerow(tup)
g.close()
