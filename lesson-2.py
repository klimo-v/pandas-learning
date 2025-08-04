from datetime import datetime
import pandas as pd
import numpy as np

# ✅ Мини-проект: Анализ продаж за 3 года
# 📁 Дано:
# Сгенерируй DataFrame со следующими столбцами:
    # date: случайные даты с 01.01.2021 по 31.12.2023
    # product: одно из ['Laptop', 'Phone', 'Tablet']
    # units_sold: количество продаж (распределение Пуассона)
    # unit_price: цена продажи (случайное число от 100 до 1000)
    # revenue: units_sold * unit_price
# Добавь пропуски:
    # ~100 пропусков в units_sold
    # ~50 пропусков в unit_price

data = {
    'date': pd.date_range(start='2021-01-01', end='2023-12-31', freq='D').to_series().sample(1000, replace=True).reset_index(drop=True),
    'product': np.random.choice(['Laptop', 'Phone', 'Tablet'], size=1000),
    'units_sold': np.random.poisson(lam=5, size=1000),
    'unit_price': np.random.uniform(100, 1000, size=1000)
}

df = pd.DataFrame(data)
df['revenue'] = df['units_sold'] * df['unit_price']

indexes = np.random.choice(df.index, 100, replace=False)
df.loc[indexes, 'units_sold'] = np.nan

indexes = np.random.choice(df.index, 50, replace=False)
df.loc[indexes, 'unit_price'] = np.nan

# 📌 Часть 1. Предобработка
# Заполни пропуски:
    # В units_sold — медианным значением по всей колонке.
    # В unit_price — средним значением по всей колонке.
# Преобразуй колонку date в формат datetime.
# Добавь колонку month — месяц в формате Period (например, '2022-04').

df['units_sold'].fillna(df['units_sold'].median(), inplace=True)
df['unit_price'].fillna(df['unit_price'].mean(), inplace=True)

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')

# 📌 Часть 2. Анализ выручки
# Вычисли суммарную выручку по каждому продукту (product) и выведи в порядке убывания.
# Построй таблицу: средняя выручка по каждому продукту за каждый месяц (month x product).
# Найди 5 дней с максимальной суммарной выручкой по всем продуктам.
# Найди 5 дней с минимальной ненулевой выручкой.

sum_revenue =  df.groupby('product')['revenue'].sum().sort_values(ascending=False)
print('Суммарная выручка по продуктам:\n', sum_revenue)

# unstack позволяет преобразовать Series в DataFrame с колонками по продуктам + создает матрицу (месяцы / продукты) из multiиндекса.
avg_revenue = df.groupby(['month', 'product'])['revenue'].mean().unstack()

print('Средняя выручка по продуктам за каждый месяц:\n', avg_revenue)

print(df)

max5days =  df.groupby('date')['revenue'].sum().nlargest(5)
print('5 дней с максимальной выручкой:\n', max5days)

min5days = df[df['revenue'] > 0].groupby('date')['revenue'].sum().nsmallest(5)
print('5 дней с минимальной ненулевой выручкой:\n', min5days)

# 📌 Часть 3. Скользящее среднее
# Построй Series, где:
    # Индекс — date
    # Значения — суммарная выручка по всем продуктам
# Построй скользящее среднее по этой серии с окном 30 дней.
# Построй график:
    # Серая линия: ежедневная выручка
    # Красная линия: 30-дневное скользящее среднее

daily_revenue = df.groupby('date')['revenue'].sum()
rolling_avg = daily_revenue.rolling(window=30).mean()
print('Суммарная выручка по всем продуктам:\n', rolling_avg)

import matplotlib.pyplot as plt
plt.figure(figsize=(14, 7))
plt.plot(daily_revenue.index, daily_revenue, color='gray', label='Ежедневная выручка')
plt.plot(rolling_avg.index, rolling_avg, color='red', label='30-дневное скользящее среднее')
plt.title('Ежедневная выручка и 30-дневное скользящее среднее')
plt.xlabel('Дата')
plt.ylabel('Выручка')
plt.legend()
plt.show()
