#!/usr/bin/python
# coding: UTF-8
import re

f = open("person.txt")
lines = f.readlines()
f.close()

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


for line in lines:
  which_rel(line)
