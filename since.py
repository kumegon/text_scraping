#coding:utf-8

import csv   #csvモジュールをインポートする
import re
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


#base_dateに登校時の時間を入れる


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
                , u'〇':0, u'壱':1, u'弐':2, u'参':3, u'数':3, u'何':3
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




def get_number(str):
  return str.split(u'代')[0].split(u'歳')[0].split(u'才')[0]

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


def since_age(line):
  age = None
  if re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]?代', line):
    age = str2int(get_number(re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]?代',line)[0]))
    former = u'前'
    latter = u'後'
    middle = u'半'
    if re.findall(former, line):
      age += 3
    elif re.findall(latter, line):
      age += 8
    elif re.findall(middle, line):
      age += 5
    else:
      age += 5
  elif re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]', line):
    age = str2int(get_number(re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]',line)[0]))
  elif re.findall(u'高[校]?[1-3１-３一二三]?',line):
    age = 16
    grade = get_grade(line)
    if grade >= 0:
      age += grade
    else:
      age += 1
  elif re.findall(u'中[学]?[1-3１-３一二三]?',line):
    age = 13
    grade = get_grade(line)
    if grade >= 0:
      age += grade
    else:
      age += 1
  elif re.findall(u'小[学]?[1-6１-６一二三四五六]?',line):
    age = 7
    grade = get_grade(line)
    range_grade = get_range_grade(line)
    if grade >= 0:
      age += grade
    elif range_grade > 0:
      age += range_grade
    else:
      age += 3
  elif re.findall(u'幼稚園|保育園|幼|小さ',line):
    age = 4
  #elif re.findall(u'[かヶケヵ]?月',line):
  #  age = 0

  #elif re.findall(u'[1-6１-６一二三四五六]年[生]?', line):
  #  if(re.findall(u'[1-6１-６一二三四五六]', line)):
  #    grade = str2int(re.findall(u'[1-6１-６一二三四五六]', line)[0])
  #    age = 6 + grade
  #  else:
  #    age = -1
  elif re.findall(u'少[年女]|子供|子ども|こども', line):
    age = 10
  elif re.findall(u'青年', line):
    age = 18
  elif re.findall(u'中年', line):
    age = 35
  elif re.findall(u'老年', line):
    age = 56
  elif re.findall(u'高齢', line):
    age = 70
  elif re.findall(u'成人', line):
    age = 20
  elif re.findall(u'社会人', line):
    age = 22
  elif re.findall(u'大学|学生', line):
    age = 20
  return age



def none2zero(arg):
  if arg:
    return arg
  else:
    return 0

def since_date(line):
  base_date = datetime.now()
  is_since_date = False #since_dateに関する表記がある場合はTrue
  ago_hour = None
  ago_day = None
  ago_week = None
  ago_month = None
  ago_year = None
  set_hour = None
  set_day = None
  set_week = None
  set_month = None
  set_year = None
  how_ago = None
  #具体的なdateが決まっているか
  #8/5みたいな表記
  if re.findall(u'[0-9０-９一二三四五六七八九十〇]+/[0-9０-９一二三四五六七八九十〇]+',line):
    text = re.search(u'[0-9０-９一二三四五六七八九十〇]+/[0-9０-９一二三四五六七八九十〇]+',line).group(0).split('/')
    set_month = str2int(text[0])
    set_day = str2int(text[1])
  #16年10月みたいな表記
  if re.findall(u'([0-9０-９]{4}年)?([0-9０-９]{1,2}月)?' , line):
    if re.findall(u'[0-9０-９]{4}年', line):
      set_year = str2int(re.search(u'[0-9０-９]{4}年', line).group(0).split(u'年')[0])
      if set_year <= base_date.year - 2000:
        set_year += 2000
      elif set_year < 100:
        set_year += 1900
    if re.findall(u'[0-9０-９]{1,2}月', line):
      set_month = str2int(re.search(u'[0-9０-９]{1,2}月', line).group(0).split(u'月')[0])
  #平成28年６月頃からみたいな表記
  if u'前' not in line and re.findall(u'(H|h|S|s|平成|昭和)?([0-9０-９一二三四五六七八九十〇]+(時|日|月|年).*).*(|頃|ころ|ごろ)?.*(から|より)',line):
    not_ago_year = False
    text = re.search(u'(H|S|平成|昭和)?([0-9０-９一二三四五六七八九十〇]+(時|日|月|年).*).*(|頃|ころ|ごろ)?.*(から|より)',line).group(0)
    if u'高校' in line or u'中学' in line or u'小学' in line:
      not_ago_year = True
    text = re.search(u'(H|S|平成|昭和)?(([0-9０-９一二三四五六七八九十〇]+(時|日|月|年).*))+', line).group(0)
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)時', text)):
      set_hour = str2int(re.search(u'[0-9０-９一二三四五六七八九十〇]+時', text).group(0).split(u'時')[0])
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)日', text)):
      set_day = str2int(re.search(u'[0-9０-９一二三四五六七八九十〇]+日', text).group(0).split(u'日')[0])
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)月', text)):
      set_month = str2int(re.split(u'月', re.search(u'[0-9０-９一二三四五六七八九十〇]+月', text).group(0))[0])
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)年', text) and not not_ago_year):
      set_year = str2int(re.search(u'[0-9０-９一二三四五六七八九十〇]+年', text).group(0).split(u'年')[0])
      if re.findall(u'(H|h|平成)', text):
        ago_year = datetime.now().year - 1988 - set_year
        set_year = 0
      elif re.findall(u'(S|s|昭和)', text):
        ago_year = datetime.now().year - 1925 - set_year
        set_year = 0
  #具体的なdateではなく、相対的な時間
  if re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)+(週間|時間|日|[かヶケヵ]?月|年)(間|.*前.*(から|より))',line):
    text = re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)+(週間|時間|日|[かヶケヵ]?月|年)(間|.*前.*(から|より))',line).group(0)
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)時間', text)):
      ago_hour = str2int(re.search(u'([0-9０-９一二三四五六七八九十〇]+|数)時間', text).group(0).split(u'時間')[0])
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)日', text)):
      tmp = re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)日', text).group(0).split(u'日')[0]
      if u'半' in tmp:
        ago_hour = 12
      else:
        ago_day = str2int(tmp)
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)週間', text)):
      ago_week = str2int(re.search(u'([0-9０-９一二三四五六七八九十〇]+|数)週間', text).group(0).split(u'週間')[0])
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)[かヶケヵ]?月', text)):
      tmp = re.split(u'[かヶケヵ]?月', re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)[かヶケヵ]?月', text).group(0))[0]
      if u'半'in tmp:
        ago_day = 15
      else:
        ago_month = str2int(tmp)
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)年', text)):
      tmp = tmp = re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)年', text).group(0).split(u'年')[0]
      if u'半' in tmp:
        ago_month = 6
      else:
        ago_year = str2int(tmp)
  if re.findall(u'(今|去|昨|先|前)(日|週|月|年)', line):
    text = re.search(u'(今|去|昨|先|前)(日|週|月|年)', line).group(0)
    if u'今' in text:
      how_ago = 0
    elif u'去' in text:
      how_ago = 1
    elif u'昨' in text:
      how_ago = 1
    elif u'先' in text:
      how_ago = 1
    elif u'前' in text:
      how_ago = 1

    elif u'日' in text:
      ago_day = how_ago
    elif u'週' in text:
      ago_day = how_ago * 7
    elif u'月' in text:
      ago_month = how_ago
    elif u'年' in text:
      ago_year = how_ago


  if(u'朝' in line):
    set_hour = 7
  elif(u'昼' in line):
    set_hour = 12
  elif(u'日中' in line):
    set_hour = 12
  elif(u'夕' in line):
    set_hour = 17
  elif(u'晩' in line):
    set_hour = 20
  elif(u'深夜' in line):
    set_hour = 0
  elif(u'夜' in line):
    set_hour = 20

  if(u'秋' in line):
    set_month = 10
  elif(u'冬' in line):
    set_month = 1
  elif(u'春' in line):
    set_month = 4
  elif(u'夏' in line):
    set_month = 7


  if ago_day is not None or ago_week is not None or ago_month is not None or ago_year is not None:
    is_since_date = True
    ago_day = none2zero(ago_day)
    ago_week = none2zero(ago_week)
    ago_month = none2zero(ago_month)
    ago_year = none2zero(ago_year)
    base_date -= relativedelta(days = ago_day, weeks = ago_week, months = ago_month, years = ago_year)
  if set_hour:
    if set_hour >= 24:
      set_hour -= 24
    base_date = base_date.replace(hour = set_hour)
  if set_year:
    base_date = base_date.replace(year = set_year)
  if set_month:
    base_date = base_date.replace(month = set_month)
  if set_day and set_day < 32:
    base_date = base_date.replace(day = set_day)
  if set_hour is not None or set_day is not None or set_week is not None or set_month is not None or set_year is not None:
    is_since_date = True
  if is_since_date:
    return base_date
  else:
    return None




g = open('since.csv','wb')
writer = csv.writer(g, lineterminator='\n')
df = pd.read_csv("named_entity_report_csv_20170510_105557.csv")
for key, value in df[df.label_type == "SINCE"].iterrows():
  if(value['ne_text']==value['ne_text']):
    text = str(value['ne_text']).decode('utf-8')
    result = [value['id'],since_age(text), since_date(text), value['ne_text']]
    print(result)
    writer.writerow(result)
g.close()
