from datetime import datetime
import pandas as pd
import numpy as np
import yfinance as yf

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
#   Добавь колонки с днями недели и количеством дней для каждого продукта по дням недели.
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
print(df2)

# Cоздает объект Series, где:
# Индексы Series — это уникальные значения из столбца product (группировка выполняется по этому столбцу).
# Значения Series — это суммы значений из столбца revenue для каждой группы (где product имеет одинаковое значение).
total_rev = df2.groupby('product')['revenue'].sum()
days = df2.groupby('product').size()
df4 = pd.DataFrame({
    'tatal_revenue': total_rev,
    'days': days
})

print('# Найди день, когда была максимальная revenue для каждого продукта.')
print(df2.loc[df2.groupby('product')['revenue'].idxmax()])

print('Добавь колонки с днями недели и количеством дней для каждого продукта по дням недели.')
# Добавляем колонку с днями недели в df2
df2['day_of_week'] = df2['date'].dt.day_name()
# print(df2)

# Создаем таблицу с количеством дней для каждого продукта по дням недели
# Метод pd.crosstab в Pandas используется для создания таблицы перекрестной частоты contingency table).
# Он подсчитывает количество уникальных комбинаций значений из двух или более категориальных переменных.
# по умолчанию aggfunc - len (подсчет числа вхождений), можно указать другую функцию агрегации, например 'sum' или 'mean'.

days_count = pd.crosstab(df2['product'], df2['day_of_week'])

# Объединяем с df4
df4 = pd.concat([df4, days_count], axis=1)

print(df4)

print('# Преобразуй колонку date в datetime и установи как индекс.')
df2['date'] = pd.to_datetime(df2['date'])

# Описание: Прямое присваивание столбца date индексу DataFrame.
# Ключевые особенности:
# Столбец date остается в DataFrame как обычный столбец.
# Индекс обновляется, но столбец date не удаляется.
df2.index = df2['date']

# Столбец date больше не будет доступен как столбец, а станет индексом.
df2.set_index('date', inplace=True)


print(df2)

print('# Отфильтруй строки только за март 2021 года.')

# Фильтрация строк по дате
# Т.к. индекс df2 уже является DatetimeIndex (мы это сделали выше), можно использовать строку с датой для фильтрации.
# Python преобразует строку '2021-03' в диапазон дат с 1 по 31 марта 2021 года.
march_data = df2.loc['2021-03']
print(march_data)

print('# Построй скользящее среднее revenue с окном 7 дней.')

# Метод rolling() cоздает объект "скользящего окна" для выполнения операций на подвыборках данных.
# window=7 это размер 1-ой выборки. Выборка скользит по строкам DataFrame. 
# Количество выборок будет равно количеству строк в DataFrame минус 6 (поскольку первая выборка начинается с первой строки и заканчивается на седьмой).
# со скользящим окно мы можем вычеслять разные статистики, например среднее значение.
# Метод mean() вычисляет среднее значение для каждого окна.
print(df2['revenue'].rolling(window=7).mean())

print('# Работа с пропущенными значениями:')
print('# Вставь пропуски (np.nan) в случайные ячейки.')

# Создаем DataFrame с пропущенными значениями
nan_indices = np.random.choice(df2.index, size=10, replace=False) # случайно выбираем 10 индексов из df2
print(f'Indices with NaN values: {nan_indices}')
for idx in nan_indices:
    df2.loc[idx, 'revenue'] = np.nan

print(df2)

print('# Замени пропуски средним по колонке.')
# Метод fillna() используется для заполнения пропущенных значений в DataFrame.

df2['revenue'] = df2['revenue'].fillna(df2['revenue'].mean())
print(df2)

print('# Найди строки, где больше одного пропуска.')
# Метод isna() возвращает DataFrame с булевыми значениями, где True означает пропущенное значение.
# sum(axis=1) суммирует количество пропущенных значений в каждой строке.
# axis=1 указывает, что суммирование выполняется по строкам.

df2['missing_count'] = df2.isna().sum(axis=1)
print(df2[df2['missing_count'] > 1])


# 5

# Создай MultiIndex DataFrame с уровнями year и month.
    # Добавь данные по продажам.
    # Найди среднюю продажу за каждый год.
    # Преобразуй в обычный DataFrame сбросом индекса.

print('5# ------------------------------')

data = {
    'year': [2021, 2021, 2022, 2022],
    'month': [1, 2, 1, 2],
}

df5 = pd.DataFrame(data)
df5.set_index(['year', 'month'], inplace=True)
df5['sales'] = [1000, 1500, 2000, 2500]

print(df5)

print(df5.groupby('year')['sales'].mean())

df5.reset_index(inplace=True)
print(df5)

# Работа с функцией .apply:
    # На DataFrame с колонками name, birthdate, city — создай колонку age, вычисляя её из birthdate.
    # Используй apply с lambda, чтобы определить, в каком городе самая большая доля людей моложе 30.

obj2 = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'birthdate': ['1995-01-01', '1985-02-02', '2000-03-03', '1990-04-04', '1988-05-05'],
    'city': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Chicago']
}

df51 = pd.DataFrame(obj2)
df51['age'] = datetime.now().year - pd.to_datetime(df51['birthdate']).dt.year

print(df51)

# Метод mean() вычисляет среднее значение для каждой группы, созданной методом groupby.
# Почему мы ищем долю, а не абсолютное количество:
# Доля позволяет сравнивать города с разным количеством людей.
# Как выглядит значение этой доли:
# Значение доли — это число от 0 до 1, где 0 означает, что в городе нет людей моложе 30 лет, а 1 означает, что все люди в городе моложе 30 лет.
# Поэтому мы используем mean() для вычисления доли людей моложе 30 лет в каждом городе.
# Как работает idxmax():
# Метод idxmax() возвращает индекс (в данном случае город), для которого значение максимальное.
city_with_max_young_share = df51.groupby('city').apply(lambda x: (x['age'] < 30).mean()).idxmax()
print('Город с наибольшей долей людей моложе 30 лет:', city_with_max_young_share)

# Работа с временными рядами:
    # Сгенерируй Series с датами от 2020 до 2023 с шагом 1 день.
    # В значения запиши случайные данные.
    # Найди:
        # среднее по каждому месяцу,
        # разницу между текущим и предыдущим днём,
        # процентное изменение (pct_change).

print('6# ------------------------------')
date_range = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
random_data = np.random.randint(1,100, size=len(date_range))
series = pd.Series(random_data, index=date_range)

# Для каждого месяца собрать все строки в одну группу,
# а потом для каждой группы (месяца) посчитать среднее по колонкам.

series_monthly_mean = series.resample('M').mean()

print(series_monthly_mean)

# Разница между днями
diff = series_monthly_mean.diff()

print(diff)

# Процентное изменение
# Метод pct_change() вычисляет процентное изменение между текущим и предыдущим значением.
# Он возвращает Series, где каждое значение представляет собой процентное изменение относительно предыдущего значения
pct_change = series_monthly_mean.pct_change()

print(pct_change)

# Посчитать среднее, стандартное отклонение и корреляцию для нескольких акций:

symbols = ['TCS.NS', 'HDFCBANK.NS', 'MARUTI.NS']
weights = [np.array([0.25, 0.35, 0.4])]
start_date = '2010-01-01'  # define start date
end_date = datetime.today().strftime('%Y-%m-%d')  # format the current date as a string in 'YYYY-MM-DD' format

price = yf.download(symbols, start=start_date, end=end_date)['Close']
returns = price.pct_change()

print('Mean')
print(returns.mean())
print('\nStandard Deviation')
print(returns.std())
print('\nCorrelation Table')
print(returns.corr())