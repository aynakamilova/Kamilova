import urllib.request, json
import matplotlib.pyplot as plt
from matplotlib import style



def comments(postid):
    req = urllib.request.Request(
        'https://api.vk.com/method/wall.getComments?owner_id=-33374477&post_id='+postid)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    counter = 0
    total_l = 0
    for onecomment in data['response']:
        counter += 1
        if counter < 2:
            continue
        #print('Комментатор', onecomment['from_id'])
        one_l =len(onecomment['text'].split())
        total_l += one_l
        #print('>>>>' , len(onecomment['text'].split()),onecomment['text'])
        fout.write('++++' + onecomment['text'] + '\n')
    average_com = total_l/(counter-1)
    #print('Средняя длина комментария', average_com)
    return average_com

def users(user):
    req = urllib.request.Request(
        'https://api.vk.com/method/users.get?user_ids={}&fields=home_town,bdate'.format(str(user)))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    if not data['response']:
        return None, None
    #if ('bdate' not in (data['response'][0])) and ('home_town' not in (data['response'][0])):
    if not (data['response'][0].get('bdate') and data['response'][0].get('home_town')):
        return None, None
    return data['response'][0]['bdate'], data['response'][0]['home_town']


###Здесь начинается главная часть программы ####


all_posts = []
fout = open('printout.txt', 'w', encoding='utf-8')

for offset in range(0,2000, 100):
    req = urllib.request.Request('https://api.vk.com/method/wall.get?domain=dormitory8hse&count=100&offset='+str(offset))
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    data = json.loads(result)

    skip = 0
    #для пропуска первого элемента

    for item in data['response']:
        skip += 1
        if skip < 2:
            continue
        #Первый (нулевой) элемент списка не несет информации. Это - число, кол-во постов в блоке данных
        idpost = item['id']
        ncom = item['comments']['count']
        if ncom>0:
            datebirth, hometown = users(item['from_id'])
            if not hometown and not datebirth:
                continue
            elif datebirth.count('.') == 1:
                continue
            #print('\nАвтор поста:', item['from_id'])
            fout.write('\nАвтор поста: ' + str(item['from_id']) + '\n')
            #print('Дата рождения:', bdate, 'Город:', hometown)
            fout.write('Дата его рождения: ' + datebirth + ' Его город: ' + hometown + '\n')
            #print(item['text'])
            fout.write(item['text']+'\n')
            post_l = len(item['text'].split())
            #print('Длина поста:', post_l)
            av_com = comments(str(idpost))
            #print('Соотношение', post_l, '/', av_com)
            city = item['from_id']
            all_posts.append((city, datebirth, hometown, post_l, av_com))

fout.close()

cities = {item[2]:(0, 0, 0) for item in all_posts}
for item in all_posts:
    tot_pos_l = cities[item[2]][0] + item[3]
    tot_com_l = cities[item[2]][1] + item[4]
    nposts =  cities[item[2]][2] + 1
    cities[item[2]] = (tot_pos_l, tot_com_l ,nposts )
for city in cities:
    tot_pos_l, tot_com_l, nposts = cities[city]
    cities[city] = (tot_pos_l/nposts, tot_com_l/nposts)


ages = {2017- int(item[1].split('.')[-1]):(0, 0, 0) for item in all_posts}
for item in all_posts:
    age = 2017 - int(item[1].split('.')[-1])
    tot_pos_l = ages[age][0] + item[3]
    tot_com_l = ages[age][1] + item[4]
    nposts = ages[age][2] + 1
    ages[age] = (tot_pos_l, tot_com_l ,nposts )
for age in ages:
    tot_pos_l, tot_com_l, nposts = ages[age]
    ages[age] = (tot_pos_l/nposts, tot_com_l/nposts)

style.use('ggplot')

#По постам
Xaxis = [post[3] for post in all_posts] #средняя длина поста
Yaxis = [post[4] for post in all_posts] #средняя длина комментария
plt.scatter(Xaxis,Yaxis)
plt.title('Данные по постам')
plt.ylabel('Средняя длина комментария')
plt.xlabel('Средняя длина поста')
plt.show()


#По городам
Xaxis = [cities[city][0] for city in cities] #средняя длина поста
Yaxis = [cities[city][1] for city in cities] #средняя длина комментария
plt.scatter(Xaxis,Yaxis)
plt.title('Данные по городам')
plt.ylabel('Средняя длина комментария')
plt.xlabel('Средняя длина поста')
plt.show()

#По возрастам
Xaxis = [ages[age][0] for age in ages] #средняя длина поста
Yaxis = [ages[age][1] for age in ages] #средняя длина комментария
plt.scatter(Xaxis,Yaxis)
plt.title('Данные по возрастам авторов')
plt.ylabel('Средняя длина комментария')
plt.xlabel('Средняя длина поста')
plt.show()

#Средняя длина поста по возрастам
Xaxis = [age for age in ages] #значения возрастов
Yaxis = [ages[age][0] for age in ages] #средняя длина комментария
plt.scatter(Xaxis,Yaxis)
plt.title('Возраст / средняя длина поста')
plt.ylabel('Средняя длина поста')
plt.xlabel('Возраст в годах')
plt.show()


city_nums = [cities[city][0] for city in cities]
city_labs = [city for city in cities]
plt.bar(range(len(city_labs)), city_nums)

plt.title('Города / средняя длина поста')
plt.ylabel('Средняя длина поста')
plt.xlabel('Город')
plt.xticks(range(len(city_labs)), city_labs, rotation=90)
plt.legend()
plt.show()

