import os
from datetime import date
from fuzzywuzzy import fuzz
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb


# Присвоение введенного имени клиента переменной s_i


def get_content():
    global s_i
    s_i = inp_entry.get()
    print("Вы ввели: ", s_i)
    inp_window.destroy()

# Функция, которая будет подбирать новый индекс и предлагать создать новую папку клиента в папке 001_Перспектива


def create_new_clf(tdlist, parent_fpath):
    global new_clf
    global nf_index
    global new_clf_name
    nf_index = 101
    # Берем первые 2 или 3 символа от каждой папки и формируем из них список индексов
    for _, s in enumerate(tdlist[0]):
        if s[2] == "_":
            indexes_persp.append(int(s[:2]))
        elif s[3] == "_":
            indexes_persp.append(int(s[:3]))

    # Сортируем получившийся список
    indexes_persp.sort()

    for _, v in enumerate(indexes_persp):
        if v-nf_index == 1:
            nf_index += 1
        elif v-nf_index > 1:
            nf_index += 1
            break

    new_clf = mb.askyesno(title="Создание новой папки клиента",
                          message=f'Создать новую папку "{nf_index}_{s_i}" в папке 001_Перспектива?')
    if new_clf:
        new_clf_name = os.path.join(parent_fpath[0], str(nf_index)+"_"+s_i)
        os.makedirs(new_clf_name, exist_ok=True)
        mb.showinfo(title="Создание новой папки клента",
                    message=f'В каталоге //dc/Bim/01_Клиенты/001_Перспектива создана новая папка "{nf_index}_{s_i}"')


# Папка Перспектива = fold_persp
# Папка Завершенные = fold_complete
# Папка Архив = fold_archiv


clients_path = [r'\\dc\Bim\01_Клиенты\001_Перспектива',
                r'\\dc\Bim\01_Клиенты\002_Завершенные', r'\\dc\Bim\01_Клиенты\003_Архив']

# Список, куда будут записываться имена папок
clients_flist = []

# Тот же список, отфильтрованный от плохих имен папок
clients_purelist = [[] for _ in range(3)]

# Создаем список, куда будут записываться индексы из папки 001_Перспектива
indexes_persp = []

# а также список значений ratio
r_list = [[] for _ in range(3)]

# Создаем список, в который будем записывать неверно названные папки
baditems_flist = []

source_folders = ['fold_persp', 'fold_complete', 'fold_archiv']
source_folders_RU = ["001_Перспектива", "002_Завершенные", "003_Архив"]

# Создаём список списков папок
for i in clients_path:
    sf_list = [name for name in os.listdir(
        i) if os.path.isdir(os.path.join(i, name))]
    clients_flist.append(sf_list)

# print("Длина исходного списка", len(sum(clients_flist, [])))

for s in range(len(clients_flist)):
    for i in clients_flist[s]:
        if i[0].isdigit() and i[2] == '_' or i[0].isdigit() and i[3] == '_':
            clients_purelist[s].append(i)
        else:
            baditems_flist.append(i)


# Получаем сегодняшнюю дату в качестве суффикса к имени txt-файла
today = date.today()
formatted_date_str = today.strftime("%d.%m.%y")

# Формируем имена txt файлов
indexed_txtname = 'ВСЕ_КЛИЕНТЫ_' + formatted_date_str + '.txt'


with open(indexed_txtname, 'w', encoding='utf-8') as file:
    for j in range(3):
        file.write(source_folders_RU[j] + '\n')
        file.write(', '.join(clients_purelist[j])+'\n')
        file.write('\n')


# print("Длина отфильтрованного списка", len(sum(clients_purelist, [])))
# print("Длина плохого списка", len(baditems_flist))
# print(baditems_flist)


# GUI ОКНО ВВОДА ИМЕНИ КЛИЕНТА
inp_window = tk.Tk()

# Размеры окна ввода
inp_window_wdth = 394
inp_window_hgt = 180

# Получаем ширину и высоту экрана
scrwdth, scrhgt = inp_window.winfo_screenwidth(), inp_window.winfo_screenheight()

# Пишем формулу для центра экрана
xLeft, yTop = int(scrwdth/2 - inp_window_wdth /
                  2), int(scrhgt/2 - inp_window_hgt/2)

# Задаем свойства окна ввода
inp_window.title("Поиск клиента в существующих папках")
inp_window.geometry(str(inp_window_wdth) + "x" +
                    str(inp_window_hgt) + "+" + str(xLeft) + "+" + str(yTop))

# label - приветственный текст, Entry - окно ввода, Button - кнопка

inp_label = ttk.Label(
    text="Введите название организации клиента:", font=('Segoe UI', 13))
inp_label.grid(row=0, column=0, padx=34, pady=15)

inp_entry = ttk.Entry(font=('Segoe UI', 12))
inp_entry.grid(row=1, column=0, sticky=tk.EW, padx=32)

inp_button = ttk.Button(
    text="Поиск клиента", command=get_content)
inp_button.grid(row=2, column=0, pady=20, ipadx=5, ipady=5)

inp_window.mainloop()


for c in range(len(source_folders)):
    for n in clients_purelist[c]:
        r_list[c].append(fuzz.ratio(s_i, n))


# Создаем словари, в котором ключами будут элементы списка clients_purelist, а значениями - ratio из списка r_list

persp_i = source_folders.index('fold_persp')
dict_persp = {clients_purelist[persp_i][x]: r_list[persp_i][x]
              for x in range(len(clients_purelist[persp_i]))}

comp_i = source_folders.index('fold_complete')
dict_compl = {clients_purelist[comp_i][x]: r_list[comp_i][x]
              for x in range(len(clients_purelist[comp_i]))}

arch_i = source_folders.index('fold_archiv')
dict_arch = {clients_purelist[arch_i][x]: r_list[arch_i][x]
             for x in range(len(clients_purelist[arch_i]))}

# Фильтруем только значения с ratio > 46, и выводим на экран
fdi_persp = {key: value for key, value in dict_persp.items() if value >= 46}
fdi_compl = {key: value for key, value in dict_compl.items() if value >= 46}
fdi_arch = {key: value for key, value in dict_arch.items() if value >= 46}

str_persp = ', '.join(list(fdi_persp.keys()))
str_compl = ', '.join(list(fdi_compl.keys()))
str_arch = ', '.join(list(fdi_arch.keys()))

se_legend_text = [
    "В папке 001_Перпектива найден(ы): ", "В папке 002_Завершенные найден(ы): ", "В папке 003_Архив найден(ы): "]
se_strings = [str_persp, str_compl, str_arch]

se_mes_list = []

for i in range(3):
    if len(se_strings[i]) > 0:
        se_mes_list.append(se_legend_text[i]+se_strings[i])

# Запускаем диалоговое окно 'Да' 'Нет' 'Отмена' с обработкой результатов поиска
if sum(len(s) for s in se_strings) > 0:
    se_result = mb.askyesnocancel(title="Результаты поиска",
                                  message=f'{'\n \n'.join(se_mes_list)} \n \nУдовлетворены ли вы результатом поиска?')
    if se_result is False:
        create_new_clf(clients_purelist, clients_path)
    else:
        pass

else:
    se_result = mb.showerror(title="Результаты поиска",
                             message='Клиентов с таким названием на нашлось. \n \nВ папке с программой создан txt-файл с сегодняшней датой, попробуйте поискать в нем вручную')
    create_new_clf(clients_purelist, clients_path)
