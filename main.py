import csv
import json
import random
import time
import datetime
from docxtpl import DocxTemplate

# Считываем файл и выбираем случайную строку
with open('cars.txt', encoding='utf-8') as file:
    cars = []
    for row in file:
        cars.append(row)
cars_info = (cars[random.randint(0, len(cars) - 1)]).split(',')

# Функция формирования словаря для шаблона отчета
def get_context(car_info):
    return {
        'brand': car_info[0],
        'model': car_info[1],
        'fuel_cons': car_info[2],
        'price': car_info[3]
    }

'''
Функция наполнения данных для отчета P.S. время, затраченное (и записанное в файл)
на формирование отчета, расчитано не совем корректно, 
т.к. не учитывает render и сохранение файла, но в данном случае можно пренебречь.
Можно было вынести за "пределы" файла и "принтить" в коносли, но тогда не удалось бы
записать время в файл 
'''
def from_template(car_info_list, template):
    start = time.perf_counter()
    template = DocxTemplate(template)
    context = get_context(car_info_list)
    all_time = time.perf_counter() - start
    context['all_time'] = all_time
    template.render(context)
    template.save(car_info_list[0] + '_' + str(datetime.datetime.now().date()) + '_report.docx')

# Функция формирования отчета по шаблону
def generate_report(car_info_list):
    template = 'сar_template.docx'
    from_template(car_info_list, template)

# Формирование отчета
generate_report(cars_info)


# Считывание файла в массив
cars_list = []
with open('cars.txt', 'r', encoding='utf-8') as file:
    for row in file:
        cars_list.append([x.strip() for x in row.split(',')])

# заголовки для csv, напишем отдельно
columns = [['brand', 'model', 'fuel_cons', 'price']]

# Формирование и запись csv с затраченным временем
start = time.perf_counter()
with open('cars.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(columns)
    writer.writerows(cars_list)
    all_time = time.perf_counter() - start
    add_info = [[f'Script_time - {all_time} sec']]
    writer.writerows(add_info)

# Формирование и запись json с затраченным временем
start = time.perf_counter()
with open('cars.json', 'w') as f:
    json.dump(str(cars_list), f)
    all_time = time.perf_counter() - start
    add_info = [[f'Script_time - {all_time} sec']]
    json.dump(str(add_info), f)
