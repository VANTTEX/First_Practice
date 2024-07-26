import matplotlib.pyplot as plt
import glob
import re
import sys
import pandas as pd
from transliterate import translit

# Функция, улучшающая процесс считывания файлов (помогает программе считывать числа в названиях файлов отдельно)
numbers = re.compile(r"(\d+)")


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# Считывается название города и года, нозвание города транслитирируется на английский и прокладывается путь к файлам, связанным с этим городом и годом
city_year = input("Введите название города и год через пробел: ").split(" ")
city_trans = (
    translit(city_year[0], "ru", reversed=True).replace("'", "").replace("zh", "g")
)
try:
    city = city_year[0]
    year = int(city_year[1])
    path = (
        "C:/Users/bonda/Desktop/Практика 2024/Practice/meteo"  # Путь к файлу с данными
    )
    filenames = glob.glob(
        path + "/" + city_trans + "/" + city_trans + "_" + str(year) + "*.csv"
    )
    filenames = sorted(filenames, key=numericalSort)  # Сортировка по дате
    day_pres = []
    even_pres = []
    months = []
# Проверка на правильность введеных пользователем данных
except:
    print("Неправильный формат данных")
    sys.exit()
# Проверка на существование файлов по запросу пользователя
if not filenames:
    print("Неправильное название города или год")
    sys.exit()
# Цикл проходит по всем файлам с данным названием города и годом и считает средние показатели давления
for filename in filenames:
    month = filename.replace(path, "").replace(str(year), "")
    month = re.sub(r"\D", "", month)
    # Если данных за какой-либо месяц отсутсвуют, то программа выводит ошибку
    try:
        pres = pd.read_csv(
            filename,
            usecols=["Давление вечером", "Давление днём"],
        )
        days = int(pres["Давление днём"].mean())
        evening = int(pres["Давление вечером"].mean())
        day_pres.append(days)
        even_pres.append(evening)
        months.append(month)
    except Exception:
        print("Данные за", month, "месяц отсутсвуют")
# Вывод графика
plt.title("График среднего атмосферного давления днём и вечером")
plt.xlabel("Месяцы")
plt.ylabel("Давление(мм рт. ст.)")
plt.plot(months, day_pres, "D-g", label="День")
plt.plot(months, even_pres, "D-m", label="Ночь")
plt.grid(which="major")
plt.legend(fontsize=14)
plt.show()
