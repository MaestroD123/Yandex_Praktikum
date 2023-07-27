#!/usr/bin/env python
# coding: utf-8

# # Исследование рынка заведений общественного питания Москвы

# В данном исследовании необходимо подготовить данные для анализа рынка Москвы, найти особенности, которые в будущем помогут в выборе подходящего инвесторам места.
# В ходе исследования будет анализироваться датасет с заведениями общественного питания Москвы, составленный на основе данных сервисов Яндекс Карты и Яндекс Бизнес на лето 2022 года. Информация носит исключительно справочный характер.

# ## Описание данных:
#  - name — название заведения;
#  - address — адрес заведения;
#  - category — категория заведения, например «кафе», «пиццерия» или «кофейня»;
#  - hours — информация о днях и часах работы;
#  - lat — широта географической точки, в которой находится заведение;
#  - lng — долгота географической точки, в которой находится заведение;
#  - rating — рейтинг заведения по оценкам пользователей в Яндекс Картах (высшая оценка — 5.0);
#  - price — категория цен в заведении, например «средние», «ниже среднего», «выше среднего» и так далее;
#  - avg_bill — строка, которая хранит среднюю стоимость заказа в виде диапазона, например:
#    - «Средний счёт: 1000–1500 ₽»;
#    - «Цена чашки капучино: 130–220 ₽»;
#    - «Цена бокала пива: 400–600 ₽».
#  - middle_avg_bill — число с оценкой среднего чека, которое указано только для значений из столбца avg_bill, начинающихся с подстроки «Средний счёт»:
#    - Если в строке указан ценовой диапазон из двух значений, в столбец войдёт медиана этих двух значений.
#    - Если в строке указано одно число — цена без диапазона, то в столбец войдёт это число.
#    - Если значения нет или оно не начинается с подстроки «Средний счёт», то в столбец ничего не войдёт.
#  - middle_coffee_cup — число с оценкой одной чашки капучино, которое указано только для значений из столбца avg_bill, начинающихся с подстроки «Цена одной чашки капучино»:
#    - Если в строке указан ценовой диапазон из двух значений, в столбец войдёт медиана этих двух значений.
#    - Если в строке указано одно число — цена без диапазона, то в столбец войдёт это число.
#    - Если значения нет или оно не начинается с подстроки «Цена одной чашки капучино», то в столбец ничего не войдёт.
#  - chain — число, выраженное 0 или 1, которое показывает, является ли заведение сетевым (для маленьких сетей могут встречаться ошибки):
#    - 0 — заведение не является сетевым
#    - 1 — заведение является сетевым
#  - district — административный район, в котором находится заведение, например Центральный административный округ;
#  - seats — количество посадочных мест.

# ## План работ:
# 
# <b>Предобработка данных:</b>
# - Импорт данных;
# - Обработка пропусков;
# - Удаление дубликатов;
# - Создание столбца street с названиями улиц из столбца с адресом;
# - Создание столбца is_24/7 с обозначением, что заведение работает ежедневно и круглосуточно (24/7):
#    - логическое значение True — если заведение работает ежедневно и круглосуточно;
#    - логическое значение False — в противоположном случае.
#    
# <b>Анализ данных</b>
#  - Исследовать количество объектов общественного питания по категориям: рестораны, кофейни, пиццерии, бары и так далее. Построение визуализации.
#  - Исследовать количество посадочных мест в местах по категориям: рестораны, кофейни, пиццерии, бары и так далее. Построение визуализации.
#  - Рассмотреть соотношение сетевых и несетевых заведений в датасете.
#  - Определить топ-15 популярных сетей в Москве. Под популярностью понимается количество заведений этой сети в регионе. 
#  - Отобразить общее количество заведений и количество заведений каждой категории по районам.
#  - Визуализировать распределение средних рейтингов по категориям заведений.
#  - Построение фоновой картограммы (хороплет) со средним рейтингом заведений каждого района.
#  - Отобразить все заведения датасета на карте с помощью кластеров средствами библиотеки folium.
#  - Определить топ-15 улиц по количеству заведений.
#  - Построение фоновой картограммы (хороплет) с полученными значениями для каждого района.
#  
# <b>Дополнительный анализ данных</b>
#  
# <b>Детализация исследования по кофейням</b>
# 
# <b>Итоговые выводы</b>
# 
# <b>Презентация</b>

# ## Предобработка данных

# ### Импорт библиотек и данных

# In[1]:


get_ipython().system(' pip install folium')


# In[2]:


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from plotly import graph_objects as go
from folium import Map, Choropleth
from folium import Map, Marker
from folium.plugins import MarkerCluster


# In[3]:


# загружаем JSON-файл с границами округов Москвы
state_geo = 'https://code.s3.yandex.net/data-analyst/admin_level_geomap.geojson'
# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)


# In[4]:


try:
    data = pd.read_csv('moscow_places.csv')
except:
    data = pd.read_csv('moscow_places.csv')
    
display(data)


# ### Подготовка данных

# In[5]:


data.info()


# In[6]:


# Проверка на пропуски
display(data.isna().sum())
#Добавляем информирование по процентам пропусков с тепловым обозначением
pd.DataFrame(round(data.isna().mean()*100,)).style.background_gradient('coolwarm')


# <b>Вывод</b>
# 
# В данных имеются пропуски:
# 
#  - Пропуски заменить на что-то логичное нет возможности, удалять данные пропуске нельзя, так как будет потерян значимый процент данных.

# In[7]:


display(data.isna().sum())


# In[8]:


# Проверка на явные дубликаты
display(data.duplicated().sum())


# In[9]:


# Проверка на неявыне дубликаты
display(data['category'].nunique())
display(data['category'].unique().tolist())


# In[10]:


display(data['name'].nunique())


# In[11]:


# Перевод в верхний регистр 
data['name'] = data['name'].str.upper()
# Удаление пробелов по краям
data['name'] = data['name'].str.strip()


# In[12]:


data['name'] = data['name'].str.replace('Ё','Е')


# In[13]:


display(data['name'].nunique())


# <b>Вывод</b>
# 
# После проверки явных и неявных дубликатов уменьшили кол-во уникальных названий заведений с 5614 до 5506 (т.е. удалили неявные дубли, которые могли бы внести корректировки в финальные результаты). Для итогового анализа нам не важно в каком регистре названия.
# 

# In[14]:


display(data)


# ### Добавление столбцов

# In[15]:


# Создание столбца street с названиями улиц из столбца с адресом;

data['street'] = data['address'].apply(
    lambda x: x.split(',')[1].strip()
)


# In[16]:


display(data)


# In[17]:


# Создание столбца is_24/7 с обозначением, что заведение работает ежедневно и круглосуточно (24/7)
data['is_24/7'] = data['hours'].apply(
    lambda x: True if x == 'ежедневно, круглосуточно' 
    else False
)


# In[18]:


display(data)


# <b>Вывод</b>
# 
# Предобработка выполнена, столбцы добавлены

# ## Анализ данных

# ### Анализ кол-ва заведений по категориям

# In[19]:


data_cat = (data.groupby('category').agg(count=('lat','count')).reset_index().sort_values('count', ascending=False))
display(data_cat)


# In[20]:


fig = px.bar(data_cat, x='category', y='count',text='count')
fig.update_xaxes(tickangle=45)
fig.update_layout(title='Заведения по категориям',
                   xaxis_title='Категория',
                   yaxis_title='Кол-во заведений')
fig.show() 


# <b>Вывод</b>
# 
# Наиболее популярные категории заведений в Москве - Кафе (2003) и Рестораны (1969), меньше всего - Столовая(306) и Булочная (249)

# ### Анализ кол-ва посадочных мест по категориям

# In[21]:


data.groupby('category')['seats'].median().sort_values(ascending=False)


# In[22]:


plt.figure(figsize=(15, 10))
fig = sns.violinplot(x='category', y='seats', data=data, palette='rainbow') 
fig.set_ylabel('Кол-во мест', fontsize=15)
fig.set_xlabel('Категория', fontsize=15)
fig.set_title('Кол-во посадочных мест по категориям', fontsize=15);


# In[23]:


plt.figure(figsize=(15, 10))
fig = sns.stripplot(x='category', y='seats', data=data) 
fig.set_ylabel('Кол-во мест', fontsize=15)
fig.set_xlabel('Категория', fontsize=15)
fig.set_title('Кол-во посадочных мест по категориям', fontsize=15);


# In[24]:


seats_med = data.groupby('category').agg(median=('seats','median')).reset_index().sort_values('median', ascending=False)


# In[25]:


fig = px.bar(seats_med, x='category', y='median',text='median')
fig.update_xaxes(tickangle=45)
fig.update_yaxes(range=[40, 90])
fig.update_layout(title='Заведения по категориям',
                   xaxis_title='Категория',
                   yaxis_title='Кол-во заведений'
                   )
fig.show() 


# <b>Вывод</b>
# 
# Наибольшее медианное значение у категории ресторан - 86 (выглядит логично в ресторане - стоять такая себе история), а вот наименьший показатель у категории булочная - 50 (логично тут много работает на вынос или просто перекусить часто можно и стоя)

# ### Соотношение сетевых и несетевых заведений

# In[26]:


# Посчитаем кол-во по группам и подготовим к визуализации
data_chain = (data.groupby('chain').agg(count=('lat','count')).reset_index())
data_chain['chain'] = data_chain['chain'].map({1: 'Сетевое', 0: 'Несетевое'})
display(data_chain)


# In[27]:


fig = go.Figure(data=[go.Pie(values=data_chain['count'], labels=data_chain['chain'], pull = [0.1, 0])])
fig.update_layout(title='Соотношение сетевых и несетевых заведений',
                   uniformtext_mode='hide')
fig.show()


# <b>Вывод</b>
# 
# В анализируемых данных больше всего несетевых заведений - 5201 или 61.9%

# ### Исследование сетевых заведений

# In[28]:


# Создадим данныне только по сетевым заведениям
chain_rest = data.query('chain == 1')
display(chain_rest)


# In[29]:


chain_rest_cat = (chain_rest.groupby('category').agg(count=('name','count')).reset_index().sort_values('count', ascending=False))
display(chain_rest_cat)


# In[30]:


fig = px.bar(chain_rest_cat, x='category', y='count',text='count')
fig.update_xaxes(tickangle=45)
fig.update_layout(title='Сетевые заведения по категориям',
                   xaxis_title='Категория',
                   yaxis_title='Кол-во заведений')
fig.show() 


# In[31]:


chain_rest_all = chain_rest_cat.merge(data_cat, how='inner', on='category')
chain_rest_all.columns = [ 'category', 'count_chain', 'count_all']
chain_rest_all['ratio'] = (chain_rest_all['count_chain']/chain_rest_all['count_all'] * 100).round(2)
chain_rest_all = chain_rest_all.sort_values('ratio', ascending=False)
display(chain_rest_all)


# In[32]:


fig = px.bar(chain_rest_all, x='category', y='ratio',text='ratio')
fig.update_xaxes(tickangle=45)

fig.update_layout(title='Процент сетевых заведений по категориям',
                   xaxis_title='Категория',
                   yaxis_title='Процент сетевых заведений'
                   )
fig.show() 


# <b>Вывод</b>
# 
# Наибольшее кол-во сетевых заведений относится к категориям: кофейня, ресторан, кафе (логично, так как на рынке много франшиз в этих категориях), самый же низкий показатель у столовых (сеть столовых - это интересно)
# Булочные пиццерии и кофейни чаще всего являются сетевыми (более 50% заведений - сетевые)

# ### Топ-15 популярных сетей в Москве

# In[33]:


rest_top = chain_rest.groupby('name').agg(count=('lat','count')).reset_index().sort_values('count', ascending=False).head(15)
display(rest_top)


# In[34]:


# Составим датасет по топ 15 сетевым заведениям
rest_top_data = data.merge(rest_top, how='inner', on='name')
display(rest_top_data)


# In[35]:


rest_top_cat = (rest_top_data.groupby('category').agg(count=('name','count')).reset_index().sort_values('count', ascending=False))
display(rest_top_cat)


# In[36]:


fig = px.bar(rest_top_cat, x='category', y='count',text='count')
fig.update_xaxes(tickangle=45)
fig.update_layout(title='Топ 15 сетевых заведения по категориям',
                   xaxis_title='Категория',
                   yaxis_title='Кол-во заведений')
fig.show() 


# In[37]:


fig = px.bar(rest_top, x='name', y='count',text='count')
fig.update_xaxes(tickangle=45)
fig.update_layout(title='Топ 15 сетевых заведения по сетям',
                   xaxis_title='Сеть',
                   yaxis_title='Кол-во заведений')
fig.show() 


# <b>Вывод</b>
# 
# Большая часть сетевых заведений относится к категории "Кофейня" и самая популярная сеть в данной категории - Шоколадница
# Самая малочисленная категория в сетевых - это столовая и бар,паб, что логично

# ### Анализ по административным районам

# In[38]:


print(data['district'].nunique())
print(data['district'].unique())


# In[39]:


data_dist = (data.groupby(['district','category']).agg(count=('name','count')).reset_index().sort_values('count', ascending=False))
display(data_dist)


# In[40]:


fig = px.sunburst(data_dist, path=['district', 'category'], values='count')
fig.update_layout(title='Заведения по округам')

fig.show()


# Неинформативно, но оставим для себя

# In[41]:


fig = px.bar(data_dist, x='district', y='count', color='category', text=data_dist['count'])
fig.update_xaxes(tickangle=45)
fig.update_layout( title='Категории заведений по округам',
                   xaxis={'categoryorder':'total descending'},
                   xaxis_title='Округ',
                   yaxis_title='Кол-во заведений',
                   width=1000, # указываем размеры графика
                   height=900,)

fig.show() 


# <b>Вывод</b>
# 
# Наибольшее количество заведений находится в Центральнов округе (больше всего там ресторанов - свойственно для более дорогого района и центра города, куда приезжают погулять). Меньше всего заведений в Северо-Западном округе.
# Интересное наблюдение что рестораны самая популярная категория только в центре и на Северо-Западе, в остальных округах наиболее популярны кафе.

# ### Анализ по средним рейтингам

# In[42]:


rating_mean = data.groupby('category', as_index=False)['rating'].mean().round(2).sort_values(by='rating', ascending=False)
rating_mean.columns = ['category', 'rating_mean']
rating_mean


# In[43]:


fig = px.bar(rating_mean, x='category', y= 'rating_mean',text='rating_mean')
fig.update_xaxes(tickangle=45)
fig.update_yaxes(range=[4, 4.5])
fig.update_layout(title='Рейтинг оценок по категориям',
                   xaxis_title='Категория',
                   yaxis_title='Средняя оценка')
fig.show()


# In[44]:


plt.figure(figsize=(15, 10))
fig = sns.violinplot(x='category', y='rating', data=data, palette='rainbow') 
fig.set_ylabel('Оценки', fontsize=15)
fig.set_xlabel('Категория', fontsize=15)
fig.set_title('Оценки по категориям', fontsize=15);


# <b>Вывод</b>
# 
# Средняя оценка по всем категориям превышает 4, что выглядит довольно неплохо, но имеются выбросы. Усреднение - это хорошо но если смотреть по района то картина может быть разнообразна.

# ### Карта по районам и рейтенгам заведений в них

# In[45]:


distr_rating_mean = data.groupby('district', as_index=False)['rating'].mean().round(2).sort_values(by='rating', ascending=False)
distr_rating_mean.columns = ['district', 'rating_mean']
distr_rating_mean


# In[46]:


# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=distr_rating_mean,
    columns=['district', 'rating_mean'],
    key_on='feature.name',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    legend_name='Средний рейтинг заведений по районам',
).add_to(m)

# выводим карту
m


# <b>Вывод</b>
# 
# Самый высокий средний рейтинг заведений в центральном округе - ожидаемо. Самый низкий рейтинг в Юго-Восточном округе (там и заведений меньше чем в центральном и ресторанов, которые собирают высокие рейтинги тоже меньше).

# ### Все анализируемые заведения

# In[47]:


# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)
# создаём пустой кластер, добавляем его на карту
marker_cluster = MarkerCluster().add_to(m)

# пишем функцию, которая принимает строку датафрейма,
# создаёт маркер в текущей точке и добавляет его в кластер marker_cluster
def create_clusters(row):
    Marker(
        [row['lat'], row['lng']],
        popup=f"{row['name']} {row['rating']}",
    ).add_to(marker_cluster)

# применяем функцию create_clusters() к каждой строке датафрейма
data.apply(create_clusters, axis=1)

# выводим карту
m


# ### Топ улиц по кол-ву заведений

# In[48]:


street_top = data.groupby('street').agg(count=('name','count')).reset_index().sort_values('count', ascending=False).head(15)
display(street_top)


# In[49]:


street_top_cat = data.groupby(['street','category']).agg(count=('name','count')).reset_index().sort_values('count', ascending=False)
display(street_top_cat)


# In[50]:


street_cat = street_top_cat.merge(street_top, how='inner', on='street')
street_cat.columns = ['street', 'category', 'count_cat', 'count_street']
street_cat = street_cat.sort_values('count_street', ascending=False)
display(street_cat)


# In[51]:


street_cat['street'].nunique()


# In[52]:


fig = px.sunburst(street_cat, path=['street', 'category'], values='count_cat')
fig.update_layout(title='Заведения по улицам')

fig.show()


# In[53]:


fig = px.bar(street_cat, x='street', y='count_cat', color='category', text=street_cat['count_cat'])
fig.update_xaxes(tickangle=45)
fig.update_layout( title='Категории заведений по топ 15 улицам',
                   xaxis_title='Улица',
                   yaxis_title='Кол-во заведений',
                   width=1000, # указываем размеры графика
                   height=1000,)

fig.show()


# <b>Вывод</b>
# 
# Больше всего заведений на проспекте Мира - длинная улица и много привлекательных для людей мест (ВДНХ, Аптекарский огород и много станций метро). Также интересно, что в топе присутствует МКАД - скорее всего попадание обусловленно именно протяженностью. 

# ### Улицы с одним заведением

# In[54]:


street_all = data.groupby('street').agg(count=('name','count')).reset_index().sort_values('count', ascending=False)
display(street_all)


# In[55]:


# Создадим данныне только по 1 заведению на улице
street_one = street_all.query('count == 1')
display(street_one)


# In[56]:


# Составим датасет по данным улицам и заведениям на них
street_one_data = data.merge(street_one, how='inner', on='street')
display(street_one_data)


# In[57]:


street_data = (street_one_data.groupby('district').agg(count=('name','count')).reset_index().sort_values('count', ascending=False))
display(street_data)


# In[58]:


# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)

# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=street_data,
    columns=['district', 'count'],
    key_on='feature.name',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    legend_name='Кол-во заведений по районам',
).add_to(m)

# выводим карту
m


# In[59]:


# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)
# создаём пустой кластер, добавляем его на карту
marker_cluster = MarkerCluster().add_to(m)

# пишем функцию, которая принимает строку датафрейма,
# создаёт маркер в текущей точке и добавляет его в кластер marker_cluster
def create_clusters(row):
    Marker(
        [row['lat'], row['lng']],
        popup=f"{row['name']} {row['rating']}",
    ).add_to(marker_cluster)

# применяем функцию create_clusters() к каждой строке датафрейма
street_one_data.apply(create_clusters, axis=1)

# выводим карту
m


# <b>Вывод</b>
# 
# Больше всего улиц с 1-м заведением находится в центральном округе, скорее всего это вызвано тем, что в центре больше маленьких улочек/переулков и т.д и практически на каждой улице есть какое-то заведение.

# ### Анализ среднего чека

# In[60]:


avg_bill = data.groupby('district').agg(median=('middle_avg_bill','median')).reset_index().sort_values('median', ascending=False)

display(avg_bill)


# In[61]:



# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)

# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=avg_bill,
    columns=['district', 'median'],
    key_on='feature.name',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    legend_name='Средний рейтинг заведений по районам',
).add_to(m)

# выводим карту
m


# <b>Вывод</b>
# 
# Наибольший средний чек зафиксирован в центральном и западном округах, за ними идет север и северо-запад. В целом видна небольшая зависимость от рейтинга округов (за исключением западного), но тут мы смотрели медиану, а на рейтинге - среднее.

# ### Выводы этапа анализа

# По итогам проведенного анализа, можно сказать что открытие кофейни выглядит логично, так как их много на рынке и можно подсмотреть фишки у конкурентов. Открытие кофейни будет стоить гораздо меньше, чем ресторан. Рейтинг у кофеен средний по категории. Ориентируясь на средние чеки логичнее открываться в западном округе (чек высокий, а аренда скорее всего дешевле чем в центре). Для кофеен нужно меньше посадочных мест чем для ресторанов и пабов.

# ## Дополнительный анализ данных

# ### Соотношение круглосуточных к обычным заведениям

# In[62]:


# Посчитаем кол-во по группам и подготовим к визуализации
data_is_24 = (data.groupby(['category','is_24/7']).agg(count=('name','count')).reset_index())
data_is_24['is_24/7'] = data_is_24['is_24/7'].map({True: 'Круглосуточно', False: 'Обычно'})
display(data_is_24)


# In[63]:


fig = go.Figure(data=[go.Pie(labels=data_is_24['is_24/7'], values=data_is_24['count'], pull = [0.1, 0])])
fig.update_layout(
    title='Процент обычных и круглосуточных заведений')
fig.show()


# In[64]:


fig = px.sunburst(data_is_24, path=['is_24/7','category'], values='count')
fig.update_layout(
    title='Категории обычных и круглосуточных заведений')

fig.show()


# <b>Вывод</b>
# 
# Круглосуточно и ежедневно работающих заведений меньше 10% от общего числа заведений.

# ### Анализ категории цен

# In[65]:


price_cat = (data.groupby('price').agg(count=('name','count')).reset_index().sort_values('count', ascending=False))
display(price_cat)


# <b>Вывод</b>
# 
# Больше всего заведений со средним ценником, самыми малочисленными являются заведения с низким ценником, что соответствует реальности для Московы.

# In[66]:


data_dist_price = (data.groupby(['district','price']).agg(count=('name','count')).reset_index().sort_values('count', ascending=False))
display(data_dist_price)


# In[67]:


fig = px.bar(data_dist_price, x='district', y='count', color='price', text=data_dist_price['count'])
fig.update_xaxes(tickangle=45)
fig.update_layout( title='Категории заведений по округам',
                  xaxis={'categoryorder':'total descending'},
                   xaxis_title='Округ',
                   yaxis_title='Кол-во заведений',
                   width=1000, # указываем размеры графика
                   height=900,)

fig.show() 


# <b>Вывод</b>
# 
# Больше всего заведений в центре среди которых заведений с низким ценником всего 34.

# ## Детализируем исследование: открытие кофейни

# In[68]:


coffe = data.query('category == "кофейня"')
display(coffe)


# In[69]:


print(coffe['name'].count())


# In[70]:


coffe_distr_data = (coffe.groupby('district').agg(count=('name','count')).reset_index().sort_values('count', ascending=False))
display(coffe_distr_data)


# In[71]:


# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)

# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=coffe_distr_data,
    columns=['district', 'count'],
    key_on='feature.name',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    legend_name='Расположение кофеен',
).add_to(m)

# выводим карту
m


# <b>Вывод</b>
# 
# Всего в датасете присутствует 1398 кофеен. Самым популярным местом для кофеен является центральный округ, меньше всего кофеен на северо-западе. То что в центре много кофеен обуславливается офисами, большим потоком людей и мест для прогулок (а так же для красивых и "деловых" фоточек с кофе).

# In[72]:


coffe_is_24 = (coffe.groupby(['category','is_24/7']).agg(count=('name','count')).reset_index())
coffe_is_24['is_24/7'] = coffe_is_24['is_24/7'].map({True: 'Круглосуточно', False: 'Обычно'})
display(coffe_is_24)


# In[73]:


fig = go.Figure(data=[go.Pie(labels=coffe_is_24['is_24/7'], values=coffe_is_24['count'], pull = [0.1, 0])])
fig.update_layout(
    title='Процент обычных и круглосуточных заведений')
fig.show()


# <b>Вывод</b>
# 
# Круглосуточно работает всего 59 или 4.22% кофеен. Кто будет пить кофе ночью? А за электричество и за ночные смены кто будет платить?

# In[74]:


coffe_dist_rating = coffe.groupby('district', as_index=False)['rating'].mean().round(2).sort_values(by='rating', ascending=False)
coffe_dist_rating.columns = ['district', 'rating_mean']
coffe_dist_rating


# In[75]:



# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)

# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=coffe_dist_rating,
    columns=['district', 'rating_mean'],
    key_on='feature.name',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    legend_name='Средний рейтинг кофеен по районам',
).add_to(m)

# выводим карту
m


# <b>Вывод</b>
# 
# Рейтинг самый высокий у кофеен в центр (логично их там больше и посетителей больше). Но зависимости между остальными районами и рейтингом особо не прослеживается (делайте хороший кофе и будут хорошие отзывы, но это не точно...)

# In[76]:


avg_bill_coffe = coffe.groupby('district').agg(mean=('middle_coffee_cup','mean')).reset_index().sort_values('mean', ascending=False).round(2)

display(avg_bill_coffe)


# In[77]:



# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)

# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=avg_bill_coffe,
    columns=['district', 'mean'],
    key_on='feature.name',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    legend_name='Средняя цена чашки кофе',
).add_to(m)

# выводим карту
m


# In[78]:


median_bill_coffe = coffe.groupby('district').agg(median=('middle_coffee_cup','median')).reset_index().sort_values('median', ascending=False).round(2)

display(median_bill_coffe)


# In[79]:



# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)

# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=median_bill_coffe,
    columns=['district', 'median'],
    key_on='feature.name',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    legend_name='Медианная цена чашки кофе',
).add_to(m)

# выводим карту
m


# <b>Вывод</b>
# 
# Самые высокие цены на кофе в центральном, западном и юго-западном округах. Более логично ориентироваться на медианное значение цены в рамках защиты от выблосов. При открытии кофейни стоит ориентироваться на чек в районе и для начал в рамках создания конкуренции снизить его, а потом постепенно наращивать и выходить на средний по округу или кайону (в случае если будут данные в детализации по районам).

# ### Выводы этапа анализа кофеен

# Не стоит открывать круглосуточную кофейню, так как это принесет лишние затраты, а кофе по ночам пьют мало людей. Наиболее логичным выглядит открытие кофейни на западе, средний рейтинг ниже чем в центре (можно составить конкуренцию если давать хорошее качество и интересные предложения, а также работать с клиентом), при этом ценник за чашку находится на уровне центра, следовательно имеется потенциал хорошей прибыли, так как скорее всего цена аренды помещения на западе ниже, но для подтверждения этой гепотезы нужно расширить данные.

# ## Выводы и рекомендации

# <b>Вывоы</b>
# 
# В процессе анализа были исследованы данные по заведениям Москвы ('кафе', 'ресторан', 'кофейня', 'пиццерия', 'бар,паб', 'быстрое питание', 'булочная', 'столовая').
# После очистки и предварительной обработки данных для анализа была взята информация по 7870 заведений.
# Юыли добавлены столбцы street с названиями улиц из столбца с адресом и is_24/7 с обозначением, что заведение работает ежедневно и круглосуточно (24/7).
# В анализируемых данных по категориям было соедующее распределение:
#  - кафе	2003
#  - ресторан	1969
#  - кофейня	1398
#  - бар,паб	747
#  - пиццерия	628
#  - быстрое питание	570
#  - столовая	306
#  - булочная	249
# 
#  - По результатам анализ распределения посадочных мест было определено, чтор наибольшее медианное значение у категории ресторан - 86 (выглядит логично в ресторане все сидят), а вот наименьший показатель у категории булочная - 50 (логично тут много работает на вынос или просто перекусить часто можно и стоя).
#  - В исследуемых данных имеется распределение на Несетевое заведение -	4781 и Сетевое - 3089. Наибольшее кол-во сетевых заведений относится к категориям: кофейня, ресторан, кафе (логично, так как на рынке много франшиз в этих категориях), самый же низкий показатель у столовых. Для сетевых заведений большая часть относится к категории "Кофейня" и самая популярная сеть в данной категории - Шоколадница. Самая малочисленная категория в сетевых - "быстрое питание" и самая большая сеть там - "Крошка картошка".
# 
#  - В анализируемых данных представлена информация по 9 округам ('Северный административный округ' 'Северо-Восточный административный округ' 'Северо-Западный административный округ' 'Западный административный округ' 'Центральный административный округ' 'Восточный административный округ' 'Юго-Восточный административный округ' 'Южный административный округ' 'Юго-Западный административный округ')
#  - Наибольшее количество заведений находится в Центральнов округе (больше всего там ресторанов - свойственно для более дорогого района и центра города, куда приезжают погулять). Меньше всего заведений в Северо-Западном округе. Интересное наблюдение что рестораны самая популярная категория только в центре и на Северо-Западе, в остальных округах наиболее популярны кафе. 
#  - Средняя оценка по всем категориям заведений превышает 4, что выглядит довольно неплохо, но имеются выбросы. Усреднение - это хорошо но если смотреть по района то картина может быть разнообразна.
#  - Больше всего заведений на проспекте Мира - длинная улица и много привлекательных для людей мест (ВДНХ, Аптекарский огород и много станций метро). Также интересно, что в топе присутствует МКАД - скорее всего попадание обусловленно именно протяженностью.
#  - Наибольший средний чек зафиксирован в центральном и западном округах, за ними идет север и северо-запад. В целом видна небольшая зависимость от рейтинга округов (за исключением западного), но тут мы смотрели медиану, а на рейтинге - среднее.
#  - Отдельно была проанализированна категория "кофейня", всего в датасете присутствует 1398 кофеен. Самым популярным местом для кофеен является центральный округ, меньше всего кофеен на северо-западе. То что в центре много кофеен обуславливается офисами, большим потоком людей и мест для прогулок (а так же для красивых и "деловых" фоточек с кофе). Круглосуточно работает всего 59 или 4.22% кофеен. Рейтинг самый высокий у кофеен в центр (логично их там больше и посетителей больше). Но зависимости между остальными районами и рейтингом особо не прослеживается.
# 
# <b>Рекомендации</b>
#  - По итогам проведенного анализа, можно сказать что открытие кофейни выглядит логично, так как их много на рынке и можно подсмотреть фишки у конкурентов. Открытие кофейни будет стоить гораздо меньше, чем ресторан. Рейтинг у кофеен средний по категории. Ориентируясь на средние чеки логичнее открываться в западном округе (чек высокий, а аренда скорее всего дешевле чем в центре). Для кофеен нужно меньше посадочных мест чем для ресторанов и пабов.
#  - Не стоит открывать круглосуточную кофейню, так как это принесет лишние затраты, а кофе по ночам пьют мало людей. Наиболее логичным выглядит открытие кофейни на западе, средний рейтинг ниже чем в центре (можно составить конкуренцию если давать хорошее качество и интересные предложения, а также работать с клиентом), при этом ценник за чашку находится на уровне центра, следовательно имеется потенциал хорошей прибыли, так как скорее всего цена аренды помещения на западе ниже, но для подтверждения этой гепотезы нужно расширить данные.
#  - Для более углубленного анализа, было бы неплохо получить данные в детализации по районам, а также данные по площади и чене аренды помещений, чтобы понимать стоит ли открывать заведение в том или ином районе и будет ли прибыль в итоге.
#   
# <b>Презентация:</b> <https://cloud.mail.ru/public/BuFM/mkfvzLYTS>
# 
# <b>Презентация 2:</b> https://cloud.mail.ru/public/gXkv/AD4BXcXYf
