#Готовая программа для обработки корпуса с помощью Mystem
#Запускается ПОСЛЕ Riskinform_News, которая создает
#исходную файловую структуру


import os


def RunMystem(path_in, path_out, fl, key='-cgin', fmt='--format text'):
    '''
    Функция обрабатывает файлы из списка fl, находящиеся в директории path_in
    Результат работы mystem помещается в папку path_out
    mystem вызывается с заданным ключом и пишет файлы в заданном формате
    По умолчанию, key='-cgin', fmt='--format text'
    Если нужно запустить с другими парамметрами, меняем это при вызове
    '''
    os.system(r"mystem.exe " + key + ' ' + fmt + ' ' + path_in + os.sep + fl +
              " " + path_out + os.sep + fl)



#локальный адрес, куда будем складывать статьи
loc_dir = "C:"+os.sep+'Users'+os.sep+'toshiba'+os.sep+'Desktop'+os.sep+'prog'+os.sep+'Газета' + os.sep

contdir = []
for i in os.walk(loc_dir):
    contdir.append(i)
#Получили файловую структуру ниже loc_dir

for i in contdir:
    if len(i[2]) > 0 and len(i[1]) == 0:
        next_path_in = i[0]
        next_path_out = next_path_in.replace('plain', 'mystem-plain')
        flist = i[2]
        print(next_path_in, next_path_out, flist)
        if not os.path.exists(next_path_out):
            os.makedirs(next_path_out)
        for fl in flist:
            RunMystem(next_path_in, next_path_out, fl)
#Создали дерево каталогов с текстами статей, обработанных mystem
#Вывод в простом текстовом формате (mystem-plain)

for i in contdir:
    if len(i[2]) > 0 and len(i[1]) == 0:
        next_path_in = i[0]
        next_path_out = next_path_in.replace('plain', 'mystem-xml')
        flist = i[2]
        print(next_path_in, next_path_out, flist)
        if not os.path.exists(next_path_out):
            os.makedirs(next_path_out)
        for fl in flist:
            RunMystem(next_path_in, next_path_out, fl, key='-cgin', fmt='--format xml')
#Создали еще одно дерево каталогов с текстами статей, обработанных mystem
#Теперь вывод в формате xml (mystem-xml)
