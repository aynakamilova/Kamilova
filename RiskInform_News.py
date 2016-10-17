
import os
import urllib.request
import re
#Импортируем нужные модули


def GetArticle(url):
    '''
    Функция читает одну публикацию с сайта газеты.
    Вычленяем сам текст, заголовок, автора, дату публикации
    Если публикацию с таким номером не находим, пишем
    "Нет такого заголовка" и т.п.
    Возвращает кортеж с публикацией: дату, автора, заголовок, собственно текст
    '''
    global regPostTitle, regPostDate, regPostAuthor, regPostArticle
    #Объявляем глобальными переменные со строками шаблонов регулярных выражений
    #Эти переменные формируются в главной части программы
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('cp1251')

    title = regPostTitle.findall(html)
    article = regPostArticle.findall(html)
    author = regPostAuthor.findall(html)
    artdate = regPostDate.findall(html)


    if len(title) == 0:
        title = ['Нет такого заголовка!']
    clean_t = regSpace.sub("", title[0])
    clean_t = regTag.sub("", clean_t)

    if len(author) == 0:
        author = ['Noname']
    clean_auth = regSpace.sub("", author[0])
    clean_auth = regTag.sub("", clean_auth)

    if len(article) == 0:
        article = ['Нет такой статьи!']
    clean_a = regSpace.sub("", article[0])
    clean_a = regTag.sub("", clean_a)

    clean_a = clean_a.replace("<table", "")
    clean_a = clean_a.replace("&ndash;", "")
    clean_a = clean_a.replace("&laquo;", "")
    clean_a = clean_a.replace("&raquo;", "")

    clean_auth =clean_auth.replace("Разместил ", "")
    clean_auth = clean_auth.replace("\n", "")

    artdate[0] = artdate[0].replace('-', '.')

    return artdate[0], clean_auth, clean_t, clean_a

def WriteArticle(author, title, artdate, full_url, f_addr):
    '''
        Функция пишет одну статью в файл по заданному локальному адресу f_addr
        Перед текстом статьи вставляем сводные данные по шаблону:
        @au, @ti, @da, @topic, @url

        '''
    art_f = open(f_addr, 'w', encoding='utf8')
    art_f.write('@au ' + author + '\n')
    art_f.write('@ti ' + title + '\n')
    art_f.write('@da ' + artdate + '\n')
    art_f.write('@topic ' + 'Без категории' + '\n')
    art_f.write('@url ' + full_url + '\n')
    art_f.write(article + '\n')
    art_f.close()


def WriteMeta(meta_f,author, title, artdate, full_url, f_addr):
    '''
         Эта функция пишет одну строчку метаданных.
         Поля заполняем в соответствии с заданием
        '''
    path = f_addr
    author = author
    sex = ' '
    birthday = ' '
    header = title
    created = artdate
    sphere = "публицистика"
    genre_fi = ' '
    type = ' '
    topic = 'Без категории'
    chronotop = ' '
    style = "нейтральный"
    audience_age = "н-возраст"
    audience_level = "н-уровень"
    audience_size = "республиканская"
    source = full_url
    publication = 'Риск'
    publisher = ' '
    publ_year = artdate[6:]
    medium = "газета"
    country = "Россия"
    region = 'Республика Тыва'
    language = "ru"
    meta_f.write(path + '\t' + author + '\t' + sex + '\t' + birthday + '\t' + header + '\t' +
                 created + '\t' + sphere + '\t' + genre_fi + '\t' + type + '\t' +
                 topic + '\t' + chronotop + '\t' + style + '\t' + audience_age + '\t' +
                 audience_level + '\t' + audience_size + '\t' + source + '\t' + publication + '\t'+
                 publisher + '\t' + publ_year + '\t' + medium + '\t' + country + '\t' + region + '\t' + language + '\t' )
    meta_f.write('\n')


# begin Main Body
# Здесь начинается главная часть программы

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'  # хотим притворяться браузером
base_url = 'http://risk-inform.ru/' #основная часть адреса публикации


regPostTitle = re.compile('<h3 class="zgl">.*?</h3>', flags=re.U | re.DOTALL)
regPostArticle = re.compile('<div class="statia">.*?<table', flags=re.U | re.DOTALL)
regPostAuthor = re.compile('<p align=right><i>Разместил.*?</p>', flags=re.U | re.DOTALL)
regPostDate = re.compile('\d\d-\d\d-\d\d\d\d', flags=re.U | re.DOTALL)
regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)



f_news_id = 5 #номер самой ранней публикации
l_news_id = 101 #номер самой поздней публикации
loc_dir = "C:"+os.sep+'Users'+os.sep+'toshiba'+os.sep+'Desktop'+os.sep+'prog'+os.sep+'Газета' + os.sep

metaf = open(loc_dir+os.sep+'metadata.csv', 'w', encoding='utf8')
#файл с метаданными по всем статьям в соответствии с заданием
#каждой статье в метафайле соответствует одна строчка

#Начинаем цикл по всем публикациям
for news_id in range(f_news_id, l_news_id+1):
    end_url = 'news_' + str(news_id)
    full_url = base_url + end_url + '.html'
    artdate, author, title, article = GetArticle(full_url)
    year = artdate[6:]
    month = artdate[3:5]
    f_dir = loc_dir + 'plain'+os.sep + year + os.sep + month + os.sep
    #Прописываем пути к файлу в соответствии с годом и месяцем публикации
    print(end_url, artdate, title, author) #выводим данные в консоль для контроля
    if not os.path.exists(f_dir):
        os.makedirs(f_dir)
    #Создаем вложенные директории,  если они еще не существуют
    struc = list(os.walk(f_dir))
    f_addr = f_dir + 'Статья' + str(len(struc[0][2])+1) + '.txt'
    #считаем кол-во файлов в директории и нумеруем очередной файл
    WriteArticle(author, title, artdate, full_url, f_addr)
    WriteMeta(metaf,author, title, artdate, full_url, f_addr)
#Читаем статью с сайта, формируем локальный адрес для сохранения,
#записываем статью в отдельный файл, пишем строчку в файл метаданных

metaf.close()
#Закрываем файл с метаданными

# end Main Body
#Конец главной части программы

