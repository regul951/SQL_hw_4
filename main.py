import sqlalchemy
from pprint import pprint

dbname = input('Введите название базы данных: ')
host = input('Введите host базы данных: ')
user = input('Введите имя пользователя: ')
pswd = input('Введите пароль пользователя: ')
db = f'postgresql://{user}:{pswd}@{host}/{dbname}'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

# Очистка таблиц на время тестов
# query_restart = 'TRUNCATE TABLE ' \
#                 'genre, singer, album, singergenre, singeralbum, track, collection, collectiontrack ' \
#                 'RESTART IDENTITY CASCADE;'
# result_restart = connection.execute(query_restart)

# Заполнение таблиц Singer, Genre, SingerGenre
with open("Singer.txt", "r", encoding='utf-8') as f:
    x = 0
    while True:
        s = (f.readline().rstrip().split(';'))
        if s == ['']:
            break
        query_insert_singer = f'INSERT INTO singer(pseudonym) VALUES(\'{s[0]}\');' \
                              f'INSERT INTO genre(title) VALUES(\'{s[1]}\');'
        result_insert_singer = connection.execute(query_insert_singer)

        singer = connection.execute('SELECT * FROM singer;').fetchall()
        genre = connection.execute('SELECT * FROM genre;').fetchall()

        query_insert_singergenre = f'INSERT INTO singergenre(singer_id, genre_id)' \
                                   f'VALUES({singer[x][0]}, {genre[x][0]});'
        result_insert_singergenre = connection.execute(query_insert_singergenre)
        x += 1

# Заполнение таблиц Album, SingerAlbum
with open("Album.txt", "r", encoding='utf-8') as f:
    while True:
        s = (f.readline().rstrip().split(';'))
        if s == ['']:
            break
        query_insert = f'INSERT INTO album(title, year) VALUES(\'{s[0]}\', {s[1]});'
        result_insert = connection.execute(query_insert)

        singer = connection.execute('SELECT * FROM singer;').fetchall()
        album = connection.execute('SELECT * FROM album;').fetchall()

        for key, val in singer:
            if val == s[2]:
                query_insert = f'INSERT INTO singeralbum(singer_id, album_id)' \
                               f'VALUES({key}, {len(album)});'
                result_insert = connection.execute(query_insert)

# Заполнение таблицы Collection
with open("Collection.txt", "r", encoding='utf-8') as f:
    while True:
        s = (f.readline().rstrip().split(';'))
        if s == ['']:
            break
        query_insert = f'INSERT INTO collection(title, duration, year) VALUES(\'{s[0]}\', {s[1]}, {s[2]});'
        result_insert = connection.execute(query_insert)

# Заполнение таблиц Track, CollectionTrack
with open("Track.csv", "r", encoding='utf-8') as f:
    f.readline()

    while True:
        s = (f.readline().rstrip().split(';'))
        if s == ['']:
            break
        album = connection.execute('SELECT id, title FROM album;').fetchall()
        collection = connection.execute('SELECT id, title FROM collection;').fetchall()
        for id_album, title_album in album:
            if title_album == s[2]:
                query_insert = f'INSERT INTO track(title, duration, album_id) ' \
                               f'VALUES(\'{s[4][:40]}\', {s[6]}, {id_album});'
                result_insert = connection.execute(query_insert)

        track = connection.execute('SELECT id, title FROM track;').fetchall()
        for id_coll, title_coll in collection:
            if title_coll == s[7]:
                for id_track, title_track in track:
                    if title_track == s[4]:
                        query_insert = f'INSERT INTO collectiontrack(collection_id, track_id) ' \
                                       f'VALUES({id_coll}, {id_track});'
                        result_insert = connection.execute(query_insert)


# Запросы:
# название и год выхода альбомов, вышедших в 2018 году
album = connection.execute('SELECT title, year FROM album WHERE year = 2018;').fetchall()
pprint(f'1. Название и год выхода альбомов, вышедших в 2018 году: {album}\n')

# название и продолжительность самого длительного трека
max_track_duration = connection.execute('SELECT title, duration FROM track '
                                        'WHERE duration = (SELECT MAX(duration) FROM track);').fetchall()
pprint(f'2. Название и продолжительность самого длительного трека: {max_track_duration}\n')

# название треков, продолжительность которых не менее 3,5 минуты
track_210_sec = connection.execute('SELECT title FROM track '
                                   'WHERE duration >= 210 LIMIT 10;').fetchall()
pprint(f'3. Название треков, продолжительность которых не менее 3,5 минуты: {track_210_sec}\n')

# названия сборников, вышедших в период с 2018 по 2020 год включительно;
collection_2018_2020 = connection.execute('SELECT title FROM collection '
                                          'WHERE year BETWEEN 2018 AND 2020;').fetchall()
pprint(f'4. Названия сборников, вышедших в период с 2018 по 2020 год включительно: {collection_2018_2020}\n')

# исполнители, чье имя состоит из 1 слова;
singer_name = connection.execute("SELECT pseudonym FROM singer "
                                 "WHERE pseudonym NOT LIKE '%% %%';").fetchall()
pprint(f'5. Исполнители, чье имя состоит из 1 слова: {singer_name}\n')

# название треков, которые содержат слово "мой"/"my"
track_with_my = connection.execute("SELECT title FROM track "
                                   "WHERE title iLIKE '%%my %%' OR title iLIKE '%% my';").fetchall()
pprint(f'6. Название треков, которые содержат слово "my": {track_with_my}\n')
