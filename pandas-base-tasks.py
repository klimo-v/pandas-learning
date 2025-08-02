import pandas as pd
import numpy as np

# 1

# Создай Series с индексами в виде дат и значениями в виде температуры.
#   Затем выбери все значения, где температура выше 25.
#   Отсортируй по убыванию.
print('1# ------------------------------')

random_numbers = np.random.randint(-20, 35, size=20)
t = pd.Series(random_numbers, index=pd.date_range('2023-01-01', periods=random_numbers.size))
print(t)
sorted_temp = t.sort_values(ascending=False)
print(sorted_temp)

# 2

# Создай DataFrame из словаря:
# {
#     'name': ['Alice', 'Bob', 'Charlie'],
#     'age': [25, 30, 35],
#     'salary': [50000, 60000, 70000]
# }
#   Добавь новый столбец tax = salary * 0.13
#   Удали строку с name == 'Bob'
print('2# ------------------------------')

d = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
}

df = pd.DataFrame(d)
df['tax'] = df['salary'] * 0.13
df = df.loc[df['name'] != 'Bob']
print(df)


# 3

# Прочитай CSV-файл (можно создать вручную):
#   Найди строки, где значения в колонке sales больше среднего.
#   Выведи только те строки, где region = 'North' и sales > 1000.

print('3# ------------------------------')

df1 = pd.read_csv('./assets/d.csv')
average_sales = df1['sales'].mean()


print(df1.loc[df1['sales'] > average_sales])
print(df1.loc[(df1['region'] == 'North') & (df1['sales'] > 1000)])

# 4

# Создай DataFrame с колонками date, product, revenue и quantity.
#   Сгруппируй данные по product и найди сумму revenue.
#   Найди день, когда была максимальная revenue для каждого продукта.
# Преобразуй колонку date в datetime и установи как индекс.
#   Отфильтруй строки только за март 2021 года.
#   Построй скользящее среднее revenue с окном 7 дней.
# Работа с пропущенными значениями:
#   Вставь пропуски (np.nan) в случайные ячейки.
#   Замени пропуски средним по колонке.
#   Найди строки, где больше одного пропуска.

print('4# ------------------------------')

obj = {
    'date': pd.date_range(start='2021-01-01', periods=100, freq='D'),
    'product': np.random.choice(['A', 'B', 'C'], size=100),
    'revenue': np.random.randint(100, 1000, size=100),
    'quantity': np.random.randint(1, 10, size=100)
}
df2 = pd.DataFrame(obj)
total_rev = df2.groupby('product')['revenue'].sum()
days = df2.groupby('product').size()
df4 = pd.DataFrame({
    'tatal_revenue': total_rev,
    'days': days
})
days_of_week = df2['date'].dt.day_name()
print(days_of_week)
