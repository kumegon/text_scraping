#coding:utf-8

import csv   #csvモジュールをインポートする
import re
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


#since_dateメソッド内のbase_dateに登校時の時間を入れる
g = open('since.csv','wb')#出力先のcsv
writer = csv.writer(g, lineterminator='\n')
df = pd.read_csv("named_entity_report_csv_20170510_105557.csv")#入力csv

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
    kizami_dic = {u'十':10
                , u'百':100}
    # 10進数の数字0～9に当たる全文字に対する整数値の辞書
    knum_dic = {  '0':0, '1':1, '2':2, '3':3, '4':4
                , '5':5, '6':6, '7':7, '8':8, '9':9
                , u'０':0, u'１':1, u'２':2, u'３':3, u'４':4
                , u'５':5, u'６':6, u'７':7, u'８':8, u'９':9
                #漢数字
                , u'〇':0, u'一':1, u'二':2, u'三':3, u'四':4
                , u'五':5, u'六':6, u'七':7, u'八':8, u'九':9
                , u'〇':0, u'壱':1, u'弐':2, u'参':3, u'数':3, u'何':3
                }
    r = reverse(s)                          #末尾文字から解釈するので文字列を反転
    ketaage = k3  = 1                   #各桁上げ変数を1に初期化
    n = 0                                   #桁刻みの数の計算用
    p = ''                                  #次の処理の為一つ前の文字の区分を記録
    for i in r:                             #末尾より一文字ずつ
        if i in knum_dic:                   #  漢数字0～9なら
            if p=='n':                      #    もし、一つ前もそうなら
                ketaage *= 10               #      kizamiに依存せず一桁上げ
                n += (k3 * ketaage     #      拾百千の桁刻みが省かれているものとして
                            * knum_dic[i])  #      一桁桁上げして加算
            else:                           #    でないなら
                n += k3 * knum_dic[i]  #      万以上の位と千以下の刻みをかけて加算
            p = 'n'                         #    次の処理の為一つ前が数字文字だったと記録
        elif i in kizami_dic:               #  千百十の刻みなら
            k3 = kizami_dic[i]              #    千以下の刻み桁数を代入: 千=1000, 百=100, 拾=10
            ketaage = 1                     #    漢数字0～9連続時の桁上げをクリア
            p = 'z'                         #    次の処理の為一つ前が千以下の刻み文字だったと記録                  #    次の処理の為一つ前が万以上の位文字だったと記録
        else:                               #  それ以外は
            return -1        #    取り敢えず、画面表示してpassしておく …(2)
    if p=='z':                    #最後の未処理分は
        n += k3                       #  頭の一が省略されたものと看做し処理     …(1)
    return n                                #結果を返す

def reverse(s):
    """Unicode文字列用の降順並替関数(python2.x系のunicode型にはreverse()メソッドがない)"""
    st = list(s)      #いきなりlist化
    st.reverse()
    return u''.join(st)




def get_number(str):
  return str.replace(u'代', u'').replace(u'歳', u'').replace(u'才', u'')

def get_grade(str):
  number = u'[1-6１-６一二三四五六]'
  if re.findall(number, str):
    return str2int(re.findall(number, str)[0]) - 1
  else:
    return -1

def get_range_grade(str):
  if re.findall(u'低', str):
    return 2
  elif re.findall(u'中', str):
    return 4
  elif re.findall(u'高', str):
    return 6
  else:
    return 0


def since_age(line):
  age = None
  h_school = u'高([校]|[1-3１-３一二三])'
  j_h_school = u'中([学]|[1-3１-３一二三])'
  e_scool = u'小([学]|[1-6１-６一二三四五六])'
  if re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]?代', line):
    age = str2int(get_number(re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]?代',line)[0]))
    if re.findall(u'前', line):
      age += 3
    elif re.findall(u'後', line):
      age += 8
    elif re.findall(u'半', line):
      age += 5
    else:
      age += 5
  elif re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]', line):
    age = str2int(get_number(re.findall(u'[0-9０-９一二三四五六七八九十〇]+[歳才]',line)[0]))
  elif re.search(h_school,line):
    age = 16
    grade = get_grade(re.search(h_school,line).group(0))
    if grade >= 0:
      age += grade
    else:
      age += 1
  elif re.search(j_h_school,line):
    age = 13
    grade = get_grade(re.search(j_h_school,line).group(0))
    if grade >= 0:
      age += grade
    else:
      age += 1
  elif re.search(e_scool,line):
    age = 7
    grade = get_grade(re.search(e_scool,line).group(0))
    range_grade = get_range_grade(re.search(e_scool,line).group(0))
    if grade >= 0:
      age += grade
    elif range_grade > 0:
      age += range_grade
    else:
      age += 3
  elif re.findall(u'幼稚園|保育園|幼|小さ|物心',line):
    age = 4
  elif re.findall(u'生後.*[0-9０-９一二三四五六七八九十〇]+[かヶケヵカ]月',line) or (re.findall(u'[生産]まれ', line) and not re.findall(u'が.?[生産]まれ', line)):
    age = 0

  #elif re.findall(u'[1-6１-６一二三四五六]年[生]?', line):
  #  if(re.findall(u'[1-6１-６一二三四五六]', line)):
  #    grade = str2int(re.findall(u'[1-6１-６一二三四五六]', line)[0])
  #    age = 6 + grade
  #  else:
  #    age = -1
  elif re.findall(u'少[年女]|子供|子ども|こども', line) and not re.findall(u'(子供|子ども|こども)[がを]', line):
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
  base_date = datetime(2017, 5, 19, 8, 15, 15, 945411) #ここに相談日時を入れる
  yobi = {u"月":0, u"火":1 , u"水":2 , u"木":3, u"金":4, u"土":5, u"日":6}
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
  slash = u'[0-9０-９一二三四五六七八九十〇]+/[0-9０-９一二三四五六七八九十〇]+'
  text = re.search(slash,line)
  if re.search(slash,line):
    text = re.search(slash,line).group(0).split('/')
    set_month = str2int(text[0])
    set_day = str2int(text[1])
  #16年10月みたいな表記
  if re.findall(u'([0-9０-９]{2,4}年)?([0-9０-９]{1,2}月)?' , line):
    if re.findall(u'[0-9０-９]{2,4}年', line):
      set_year = str2int(re.search(u'[0-9０-９]{2,4}年', line).group(0).replace(u'年',u''))
    if re.findall(u'[0-9０-９]{1,2}月', line):
      set_month = str2int(re.search(u'[0-9０-９]{1,2}月', line).group(0).replace(u'月',u''))
  #平成28年６月頃からみたいな表記



  if u'年' in line:
    ago = u'(H|h|S|s|平成|昭和)?(?P<number>[0-9０-９一二三四五六七八九十〇]+|数|何)+年(間|.*(まえ|前).*(から|より))'
    ago2 = u'こ[のこ].*(?P<number>[0-9０-９一二三四五六七八九十〇]+|数|何)+年(間|.*(から|より))'
    since_time = u'(H|h|S|s|平成|昭和)?(?P<number>[0-9０-９一二三四五六七八九十〇]+)年.*(頃|ころ|ごろ)?.*(から|より)'
    if re.search(ago,line):
      text = re.search(ago,line)
      ago_year = str2int(text.group('number'))
    elif re.search(ago2,line):
      text = re.search(ago2,line)
      ago_year = str2int(text.group('number'))
    elif re.search(since_time, line) and not(u'高校' in line or u'中学' in line or u'小学' in line):
      text = re.search(since_time, line)
      set_year = str2int(text.group('number'))
      if re.findall(u'(H|h|平成)', text.group(0)):
        set_year = 1988 + set_year
      elif re.findall(u'(S|s|昭和)', text.group(0)):
        set_year = 1925 + set_year
    elif re.findall(u'(今|去|一昨々|一昨|昨|先|前)年', line):
      text = re.search(u'(今|去|一昨々|一昨|昨|先|前)年', line).group(0)
      if u'今' in text:
        ago_year = 0
      elif u'去' in text:
        ago_year = 1
      elif u'一昨々' in text:
        ago_year = 3
      elif u'一昨' in text:
        ago_year = 2
      elif u'昨' in text:
        ago_year = 1
      elif u'先' in text:
        ago_year = 1
      elif u'前' in text:
        ago_year = 1


  if (u'前' not in line or u'前半' in line) and re.findall(u'(H|h|S|s|平成|昭和)?([0-9０-９一二三四五六七八九十〇]+(時|日|月|年).*).*(|頃|ころ|ごろ)?.*(から|より)',line):
    not_ago_year = False
    text = re.search(u'(H|S|平成|昭和)?([0-9０-９一二三四五六七八九十〇]+(時|日|月|年).*).*(|頃|ころ|ごろ)?.*(から|より)',line).group(0)
    if u'高校' in line or u'中学' in line or u'小学' in line:
      not_ago_year = True
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)時', text)):
      set_hour = str2int(re.search(u'[0-9０-９一二三四五六七八九十〇]+時', text).group(0).replace(u'時',u''))
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)日', text)):
      set_day = str2int(re.search(u'[0-9０-９一二三四五六七八九十〇]+日', text).group(0).replace(u'日',u''))
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)月', text)):
      set_month = str2int(re.search(u'[0-9０-９一二三四五六七八九十〇]+月', text).group(0).replace(u'月',u''))
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)年', text) and not not_ago_year):
      set_year = str2int(re.search(u'[0-9０-９一二三四五六七八九十〇]+年', text).group(0).replace(u'年',u''))
      if re.findall(u'(H|h|平成)', text):
        set_year = 1988 + set_year
      elif re.findall(u'(S|s|昭和)', text):
        set_year = 1925 + set_year
  #具体的なdateではなく、相対的な時間
  if re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)+(週間|時間|日|[かヶケヵカ]?月|年)(間|.*(まえ|前).*(から|より))|こ[のこ].*([0-9０-９一二三四五六七八九十〇]+|数|半|何)+(週間|時間|日|[かヶケヵカ]?月|年)(間|.*(から|より))',line):
    text = re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)+(週間|時間|日|[かヶケヵカ]?月|年)(間|.*(まえ|前).*(から|より))|こ[のこ].*([0-9０-９一二三四五六七八九十〇]+|数|半|何)+(週間|時間|日|[かヶケヵカ]?月|年)(間|.*(から|より))',line).group(0)
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)時間', text)):
      ago_hour = str2int(re.search(u'([0-9０-９一二三四五六七八九十〇]+|数)時間', text).group(0).replace(u'時間',u''))
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)日', text)):
      tmp = re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)日', text).group(0).replace(u'日',u'')
      if u'半' in tmp:
        ago_hour = 12
      else:
        ago_day = str2int(tmp)
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数)週間', text)):
      ago_week = str2int(re.search(u'([0-9０-９一二三四五六七八九十〇]+|数)週間', text).group(0).replace(u'週間',u''))
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)[かヶケヵカ]?月', text)):
      tmp = re.split(u'[かヶケヵカ]?月', re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)[かヶケヵカ]?月', text).group(0))[0]
      if u'半'in tmp:
        ago_day = 15
      else:
        ago_month = str2int(tmp)
    if(re.findall(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)年', text)):
      tmp = tmp = re.search(u'([0-9０-９一二三四五六七八九十〇]+|数|半|何)年', text).group(0).replace(u'年',u'')
      if u'半' in tmp:
        ago_month = 6
      else:
        ago_year = str2int(tmp)

  if re.findall(u'(今|去|一昨々|一昨|昨|先|前)(日|週|月|年)', line):
    text = re.search(u'(今|去|一昨々|一昨|昨|先|前)(日|週|月|年)', line).group(0)
    if u'今' in text:
      how_ago = 0
    elif u'去' in text:
      how_ago = 1
    elif u'一昨々' in text:
      how_ago = 3
    elif u'一昨' in text:
      how_ago = 2
      print(123123123)
    elif u'昨' in text:
      how_ago = 1
    elif u'先' in text:
      how_ago = 1
    elif u'前' in text:
      how_ago = 1

    if u'日' in text:
      ago_day = how_ago
    elif u'週' in text:
      ago_day = how_ago * 7
    elif u'月' in text:
      ago_month = how_ago
    elif u'年' in text:
      ago_year = how_ago

  if re.findall(u'月.*(上旬|前半|初旬|明け|始め|初め|はじめ|末|暮れ|終わり|下旬|後半|中旬|半ば)', line) and not re.findall(u'[かヶケヵカ]月.*(上旬|前半|初旬|明け|始め|初め|はじめ|末|暮れ|終わり|下旬|後半|中旬|半ば)', line):
    if re.findall(u'(上旬|前半|初旬|明け|始め|初め|はじめ)', line):
      set_day = 5
    elif(re.findall(u'(下旬|後半|末|暮れ|終わり)', line)):
      set_day = 25
    elif(re.findall(u'月.*(中旬|半ば)', line)):
      set_day = 15
  elif re.findall(u'年.*(上旬|前半|初旬|明け|始め|初め|はじめ|末|暮れ|終わり|下旬|後半|中旬|半ば)', line):
    if re.findall(u'(明け|始め|初め|はじめ)', line):
      set_month = 1
    elif re.findall(u'前半', line):
      set_month = 3
    elif re.findall(u'半ば', line):
      set_month = 6
    elif re.findall(u'後半', line):
      set_month = 9
    elif(re.findall(u'(末|暮れ|終わり)', line)):
      set_month = 12



  if re.findall(u'月半', line) and u'半ば' not in line:
    ago_day = 15
  if re.findall(u'年半', line) and u'半ば' not in line:
    ago_month = 6

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
  elif(u'正月' in line):
    set_month = 1

  if u'曜日' in line:
    ago_day = (base_date.weekday() - yobi[re.search(u'(.)曜日', line).group(1)]) % 7




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
    if set_year <= base_date.year - 2000:
      set_year += 2000
    elif set_year < 100:
      set_year += 1900
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





for key, value in df[df.label_type == "SINCE"].iterrows():
  if(value['ne_text']==value['ne_text']):
    text = str(value['ne_text']).decode('utf-8')
    age = since_age(text)
    date = since_date(text)
    event = None
    if not (age is not None or date is not None):
      event = value['ne_text'].replace('\n', '')
    result = [value['id'], age, date, event, value['ne_text'].replace('\n', '')]
    print(result)
    writer.writerow(result)
g.close()
