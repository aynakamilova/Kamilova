# Сканирование страниц и создание тайско-английского словаря
import re
from bs4 import BeautifulSoup
import pickle

import os
import glob

thaidict = {}

os.chdir("/Users/student/Desktop/ThaiPages-master/ThaiPages-master")
for file in glob.glob("*.html"):
        f = open(file)
        html = f.read()
        f.close()

        bsObj = BeautifulSoup(html, 'html.parser')

        wordtable = bsObj.find("table", {"class":"gridtable"})

        for row in wordtable.tr.next_siblings:
            try:
                key = row.find('a', href=re.compile('^/id/.*')).get_text()
            except AttributeError:
                continue
            strings = []
            for item in row.td.next_siblings:
                try:
                    text = item.get_text()
                    strings.append(text)
                except AttributeError:
                    continue
            thaidict[key] = strings[-1]

print('The dictionary')
print('There are', len(thaidict), 'items')
f = open('ThaiDict.dic', 'wb')
pickle.dump(thaidict, f)
f.close()
# for key, value in thaidict.items():
#     print(key, ' : ', value)
