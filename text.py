#!/usr/bin/python
# coding: UTF-8
import re
import unicodedata

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
            print i, u':数字外の文字'         #    取り敢えず、画面表示してpassしておく …(2)
    if p=='z' or p=='k':                    #最後の未処理分は
        n += k3 * k4                        #  頭の一が省略されたものと看做し処理     …(1)
    return n                                #結果を返す

def reverse(s):
    """Unicode文字列用の降順並替関数(python2.x系のunicode型にはreverse()メソッドがない)"""
    st = list(s)      #いきなりlist化
    st.reverse()
    return u''.join(st)


def which_gender(line):
  female = r'母|娘|女|妻'
  male = r'父|息子|男|夫|主人'
  if re.findall(female, line):
    print(2)
  elif re.findall(male, line):
    print(1)
  else:
    print(-1)

def which_rel(line):
  rel = {2:"妻|主人|夫", 3:"子|娘", 4:"父|母", 5:"祖", 6:"孫", 7:"義", 8:"恋|彼", 9:"知人|友"}
  flag = True
  for i in range(2,10):
    if re.findall(rel[i], line):
      print(i)
      flag = False
      break
  if flag:
    print(1)

def range_age(line):
  char2dec = {'二十':20,}
  number = r'[0-9０-９一二三四五六七八九十]+'
  age1 = r'[0-9]+[歳]*代'
  age2 = r'[０-９]{3,6}[歳]*代'
  age3 = r'[一二三四五六七八九十〇]{6}[歳]*代'
  age4 = r'十[歳]*代'
  if re.findall(age1, line):
    age_from = str2int(re.findall(age1,line)[0].split('代')[0].split('歳')[0])
    age_to = age_from + 9
    print(str(age_from) + ', ' + str(age_to))
  elif re.findall(age2, line):
    age_from = str2int(re.findall(age2,line)[0].split('代')[0].split('歳')[0].decode('utf-8'))
    age_to = age_from + 9
    print(str(age_from) + ', ' + str(age_to))
  elif re.findall(age3, line):
    age_from = str2int(re.findall(age3,line)[0].split('代')[0].split('歳')[0].decode('utf-8'))
    age_to = age_from + 9
    print(str(age_from) + ', ' + str(age_to))
  elif re.findall(age4, line):
    age_from = 9
    age_to = age_from + 9
    print(str(age_from) + ', ' + str(age_to))
for line in lines:
  range_age(line)
